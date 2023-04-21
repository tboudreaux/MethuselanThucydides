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
import pytz

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
        result.published,
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
        print(subject)
        checkCategory = Category.query.filter_by(category_id=subject).first()
        if checkCategory is None:
            HLCat = subject.split('.')[0]
            if HLCat not in SUBJECTNAMES:
                continue
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
    lenResults = 0
    for cat in arxivCategories:
        print("Fetching category: " + cat)
        r = arxiv.Search(
            query = f"cat:{cat}",
            id_list = [],
            max_results = 100,
            sort_by = SortCriterion.SubmittedDate,
        )
        todays_papers = filter(lambda x: is_paper_posted_today(x.published), r.results())
        for result in todays_papers:
            lenResults += 1
            checkPaper = Paper.query.filter_by(arxiv_id = result.get_short_id()).first()
            if checkPaper is not None:
                print("\tAlready have paper")
                continue
            enroll_single_paper(result)
    print("Done fetching, total result " + str(lenResults))
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

def is_paper_posted_today(published) -> bool:
    eastern = pytz.timezone('US/Eastern')
    current_datetime = dt.datetime.now(eastern)
    current_datetime = current_datetime.astimezone(eastern)

    # Calculate the start and end datetimes of the current visibility window
    days_delta = (current_datetime.weekday() - 2) % 5
    start_datetime = current_datetime - dt.timedelta(days=days_delta, hours=current_datetime.hour - 14, minutes=current_datetime.minute, seconds=current_datetime.second, microseconds=current_datetime.microsecond)
    end_datetime = start_datetime + dt.timedelta(days=1)

    # If it's Sunday, adjust the start and end datetimes
    if current_datetime.weekday() == 6:
        start_datetime -= dt.timedelta(days=2)
        end_datetime -= dt.timedelta(days=2)
    elif current_datetime.weekday() == 0 and current_datetime.time() < dt.time(20, 0):
        start_datetime -= dt.timedelta(days=3)
        end_datetime -= dt.timedelta(days=3)

    # Convert the start and end datetimes to UTC
    start_datetime_utc = start_datetime.astimezone(pytz.UTC)
    end_datetime_utc = end_datetime.astimezone(pytz.UTC)

    # Filter papers that fall within the visibility window
    # print(f"current_datetime: {current_datetime}")
    # print(f"start_datetime_utc: {start_datetime_utc}")
    # print(f"published: {published}")
    # print(f"end_datetime_utc: {end_datetime_utc}")
    return start_datetime_utc <= published < end_datetime_utc

