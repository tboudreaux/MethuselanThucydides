from MT.setup import db

import uuid
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.sql import func
import bcrypt
from sqlalchemy.dialects.postgresql import UUID

class Paper(db.Model):
    __tablename__ = 'arxivsummary'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    first_author = db.Column(db.String(100))
    num_authors = db.Column(db.Integer)
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

    def init(self, title, first_author, num_authors, url, abstract, comments, published_date, added_date, last_used, arxiv_id, doi, subjects, hastex, gpt_summary_short, gpt_summary_long, full_page_text):
        self.title = title
        self.first_author = first_author
        self.num_authors = num_authors
        self.url = url
        self.abstract = abstract
        self.comments = comments
        self.published_date = published_date
        self.added_date = added_date
        self.last_used = last_used
        self.arxiv_id = arxiv_id
        self.doi = doi
        self.subjects = subjects
        self.hastex = hastex
        self.gpt_summary_short = gpt_summary_short
        self.gpt_summary_long = gpt_summary_long
        self.full_page_text = full_page_text

    def __repr__(self):
        return f'<Paper: {self.title}, arxiv_id: {self.arxiv_id}>'

class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    last_login = db.Column(db.DateTime(timezone=True), default=func.now())
    last_ip = db.Column(db.String(100))
    last_user_agent = db.Column(db.String(1000))
    last_country = db.Column(db.String(1000))
    last_city = db.Column(db.String(1000))
    last_timezone = db.Column(db.String(1000))

    num_logins = db.Column(db.Integer, default=0)
    num_queries = db.Column(db.Integer, default=0)

    can_query = db.Column(db.Boolean, default=True)

    enabled = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    salt = db.Column(db.String(100), nullable=False)

    def init(self, username, email, password, ip=None, user_agent=None, country=None, city=None, timezone=None, admin=False, enabled=True):
        checkUser = User.query.filter_by(username=username).first()
        if checkUser:
            return False
        self.username = username
        self.email = email
        self.password, self.salt = self.hash_plain_password(password)
        self.last_ip = ip
        self.last_user_agent = user_agent
        self.last_country = country
        self.last_city = city
        self.last_timezone = timezone
        self.admin = admin
        self.enabled = enabled
        return True

    def hash_plain_password(self, plain_password, salt=None):
        if not salt:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedPass = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedPass, salt

    def check_password(self, plain_password):
        return self.hash_plain_password(plain_password, salt=self.salt)[0] == self.password

    def __repr__(self):
        return f'<User: {self.username}>'

class author(db.Model):
    __tablename__ = 'authors'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)

    def init(self, full_name, first_name):
        self.full_name = full_name
        self.first_name = first_name

    def __repr__(self):
        return f'<Author: {self.name}>'

class author_papers(db.Model):
    __tablename__ = 'authorpapers'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paper_id = db.Column(db.Integer, db.ForeignKey('arxivsummary.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.uuid'))

    def init(self, paper_id, author_id):
        self.paper_id = paper_id
        self.author_id = author_id

    def __repr__(self):
        return f'<PaperAuthor: {self.paper_id}, {self.author_id}>'







