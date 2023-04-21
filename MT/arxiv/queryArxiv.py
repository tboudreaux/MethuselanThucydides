from MT.setup import db, TDELTLOOKUP
from MT.utils.utils import upsert
from MT.config import arxivCategories
from MT.models.models import Paper
from MT.models.models import Author
from MT.models.models import Category
from MT.arxiv.taxonomy import IDNAMES, SUBJECTNAMES

import arxiv
from arxiv import SortCriterion
from arxiv import SortOrder
import datetime as dt
import pypdf
import os
import tempfile

def embed_single_paper(paper, result):
    inputVector = [
            "Title: " + paper.title,
            "First_author: " + paper.first_author,
            "Published: " + str(paper.published_date),
            "ID: " + paper.arxiv_id,
            "Abstract: " + paper.abstract,
            "Comments: " + str(paper.comments),
            "Subjects: " + ', '.join(paper.subjects),
            "URL" + paper.url,
            ]
    upsert(paper.arxiv_id, '\n'.join(inputVector), result.categories[0])

def enroll_single_paper(result):
    newPaper = Paper(
        result.title,
        result.authors[0].name,
        len(result.authors),
        result.pdf_url,
        result.summary,
        result.comment,
        result.published.date(),
        dt.datetime.today().date(),
        None,
        result.get_short_id(),
        None,
        result.primary_category,
        False,
        None,
        None,
        None,
    )
    for author in result.authors:
        authorNames = author.name.split()
        newAuthor = Author(
                authorNames,
                authorNames[0]
                )
        newPaper.authors.append(newAuthor)
    for subject in result.categories:
        checkCategory = Category.query.filter_by(category_id=subject).first()
        if checkCategory is None:
            HLCat = subject.split('.')[0]
            subjectName = SUBJECTNAMES[HLCat]
            catName = IDNAMES[subjectName][subject]
            newCategory = Category(subject, catName, subjectName)
            newPaper.categories.append(newCategory)
    db.session.add(newPaper)
    db.session.commit()
    embed_single_paper(newPaper, result)


def fetch_latest():
    currentWeekday = dt.datetime.today().weekday()
    TDELT = TDELTLOOKUP[currentWeekday]
    initNumPapers = Paper.query.count()
    for cat in arxivCategories:
        print("Fetching category: " + cat)
        r = arxiv.Search(
            query = f"cat:{cat}",
            id_list = [],
            max_results = 1000,
            sort_by = SortCriterion.SubmittedDate,
        )
        # check if paper is already in database
        for result in r.results():
            checkPaper = Paper.query.filter_by(arxiv_id = result.get_short_id()).first()
            if checkPaper is not None:
                break # skip paper if it's already in the database
            enroll_single_paper(result)
    finalPaperCount = Paper.query.count()
    i = finalPaperCount - initNumPapers
    return i


def fetch_arxix_id(arxivID):
        checkPaper = Paper.query.filter_by(arxiv_id = arxivID).first()
        if checkPaper is not None:
            return 0
        r = arxiv.Search(
            id_list = [arxivID],
            max_results = 1,
        )
        singlePaper = next(r.results())
        enroll_single_paper(singlePaper)

        return 1

def load_full_text(arxiv_id):
    """
    Load the full text of a paper from arxiv and store it in the database.

    Parameters
    ----------
        arxiv_id : str

    Returns
    -------
        None
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if not paper.full_page_text:
        tmpDir = tempfile.TemporaryDirectory()
        locatePaper = arxiv.Search(
            id_list = [arxiv_id],
            max_results = 1,
            )
        singlePaper = next(locatePaper.results())
        singlePaper.download_pdf(tmpDir.name, "paper.pdf")

        reader = pypdf.PdfReader(os.path.join(tmpDir.name, "paper.pdf"))
        text = "Paper Title: " + paper.title + "\n"
        for page in reader.pages:
            text += page.extract_text()
        cleanText = text.replace("\x00", "")
        paper.full_page_text = cleanText
        upsert(arxiv_id, cleanText, paper.subjects)
        db.session.commit()
    else:
        print("Already have full text")
