from MT.setup import db
from MT.utils.utils import upsert
from MT.config import arxivCategories
from MT.config import uri
from MT.models.models import Paper

import arxiv
from arxiv import SortCriterion
from arxiv import SortOrder
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import insert, select
from sqlalchemy import MetaData
import pypdf
import os
import tempfile



def fetch_latest():
    currentWeekday = dt.datetime.today().weekday()
    if currentWeekday == 5:
        TDELT = 2
    elif currentWeekday == 6:
        TDELT = 3
    elif currentWeekday == 0:
        TDELT = 3
    else:
        TDELT = 1
    i = 0
    log = list()
    for cat in arxivCategories:
        r = arxiv.Search(
            query = f"cat:{cat}",
            id_list = [],
            max_results = 300,
            sort_by = SortCriterion.SubmittedDate,
            sort_order = SortOrder.Descending,
        )

        engine = create_engine(uri)

        with engine.connect() as connection:
            metadata = MetaData()
            metadata.reflect(connection)
            arxivsummary = metadata.tables['arxivsummary']
            for result in r.results():

                if result.published.date() == dt.datetime.today().date() - dt.timedelta(TDELT):
                    ID = result.get_short_id()

                    rs = connection.execute(text(f"SELECT COUNT(id) FROM arxivsummary WHERE arxiv_id = '{ID}'"))
                    count = rs.fetchone()[0]

                    if count == 0:
                        i += 1
                        log.append(f"Adding {ID} to database")
                        enroll_paper_short(result, arxivsummary, connection)
                    else:
                        log.append(f"Skipping {ID} because it's already in the database")

                else:
                    break
    return {'statusCode': 200, 'numAdded': i, 'log': log}


def fetch_arxix_id(arxivID):
        r = arxiv.Search(
            id_list = [arxivID],
            max_results = 1,
        )
        singlePaper = next(r.results())
        engine = create_engine(uri)

        with engine.connect() as connection:
            metadata = MetaData()
            metadata.reflect(connection)
            arxivsummary = metadata.tables['arxivsummary']

            ID = singlePaper.get_short_id()

            rs = connection.execute(text(f"SELECT COUNT(id) FROM arxivsummary WHERE arxiv_id = '{ID}'"))
            count = rs.fetchone()[0]

            if count == 0:
                enroll_paper_short(singlePaper, arxivsummary, connection)
                return {'statusCode': 200, 'message': f"Added {ID} to database"}
            return {'statusCode': 200, 'message': f"Skipping {ID} because it's already in the database"}


def enroll_paper_short(paper, table, connection):
    ID = paper.get_short_id()
    title = paper.title
    authors = ', '.join([x.name for x in paper.authors])
    published = paper.published.date()
    firstAuthor = paper.authors[0].name
    pdf_url = paper.pdf_url
    summary = paper.summary
    comments = paper.comment
    doi = paper.doi
    journal_ref = paper.journal_ref
    subject = paper.categories[0]
    today = dt.datetime.today().date()

    stmt = insert(table).values(arxiv_id = ID, title = title, author_list = authors, published_date = published, first_author = firstAuthor, url = pdf_url, abstract = summary, comments = comments, doi = doi, added_date = today, subjects = subject)
    compiled = stmt.compile()
    InputResult = connection.execute(stmt)
    connection.commit()

    stmt = select(table).where(table.c.arxiv_id == ID)
    rs = connection.execute(stmt)
    paper = rs.fetchone()

    vecInput = "Title: " + paper.title + "\n" + " Authors: " + paper.author_list + "\n" +  " Published: " + str(paper.published_date) + "\n" +  " URL: " + paper.url + "\n" + " ID: " + ID + "\n" + "Abstract: " + paper.abstract

    upsert(ID, vecInput, subject)

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
