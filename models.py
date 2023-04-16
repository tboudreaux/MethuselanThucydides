from setup import db
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.sql import func

class Paper(db.Model):
    __tablename__ = 'arxivsummary'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    first_author = db.Column(db.String(100))
    author_list = db.Column(db.String(5000))
    url = db.Column(db.String(100))
    abstract = db.Column(db.String(5000))
    comments = db.Column(db.String(5000))
    published_date = db.Column(db.DateTime(timezone=True))
    added_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_used = db.Column(db.DateTime(timezone=True), default=func.now())
    arxiv_id = db.Column(db.String(30))
    doi = db.Column(db.String(100))
    subjects = db.Column(db.String(200))
    hastex = db.Column(db.Boolean, default=False)
    gpt_summary_short = db.Column(TEXT)
    gpt_summary_long = db.Column(TEXT)
    full_page_text = db.Column(TEXT)

    def __repr__(self):
        return f'<Paper {self.title}>'

