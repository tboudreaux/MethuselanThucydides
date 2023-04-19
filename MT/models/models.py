from MT.setup import db

import uuid
from sqlalchemy.dialects.postgresql import TEXT, ARRAY
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.sql import func
import bcrypt
from sqlalchemy.dialects.postgresql import UUID
import datetime as dt
import secrets
import hashlib

authors_papers = db.Table('authors_papers',
    db.Column('author_uuid', UUID(as_uuid=True), db.ForeignKey('authors.uuid'), primary_key=True),
    db.Column('paper_uuid', UUID(as_uuid=True), db.ForeignKey('papers.uuid'), primary_key=True)
)

class Paper(db.Model):
    __tablename__ = 'papers'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    queries = db.relationship("Query", backref="paper", lazy=True)
    authors = db.relationship("Author", secondary="authors_papers")

    def __init__(self, title, first_author, num_authors, url, abstract, comments, published_date, added_date, last_used, arxiv_id, doi, subjects, hastex, gpt_summary_short, gpt_summary_long, full_page_text):
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

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'first_author': self.first_author,
            'num_authors': self.num_authors,
            'url': self.url,
            'abstract': self.abstract,
            'comments': self.comments,
            'published_date': self.published_date,
            'added_date': self.added_date,
            'last_used': self.last_used,
            'arxiv_id': self.arxiv_id,
            'doi': self.doi,
            'subjects': self.subjects,
            'hastex': self.hastex,
            'gpt_summary_short': self.gpt_summary_short,
            'gpt_summary_long': self.gpt_summary_long,
            'full_page_text': self.full_page_text
        }

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

    queries = db.relationship('Query', backref='user', lazy=True)
    keys = db.relationship('Key', backref='user', lazy=True)

    def __init__(self, username, email, password, ip=None, user_agent=None, country=None, city=None, timezone=None, admin=False, enabled=True):
        checkUser = User.query.filter_by(username=username).first()
        if checkUser:
            raise EnvironmentError('Username already exists')
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

    def hash_plain_password(self, plain_password, salt=None):
        if not salt:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedPass = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedPass, salt

    def check_password(self, plain_password):
        return self.hash_plain_password(plain_password, salt=self.salt)[0] == self.password

    def __repr__(self):
        return f'<User: {self.username}>'


class Author(db.Model):
    __tablename__ = 'authors'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(ARRAY(TEXT), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)

    def __init__(self, full_name, first_name):
        self.full_name = full_name
        self.first_name = first_name

    def __repr__(self):
        return f'<Author: {" ".join(self.full_name)}>'

class Query(db.Model):
    __tablename__ = 'queries'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    paper_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('papers.uuid'), nullable=False)
    query = db.Column(TEXT, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    response = db.Column(TEXT, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __init__(self, user_uuid, paper_uuid, query, response):
        self.user_uuid = user_uuid
        self.paper_uuid = paper_uuid
        self.query = query
        self.response = response

        # get the order_id
        last_query = db.session.query(Query).filter_by(user_uuid=user_uuid, paper_uuid=paper_uuid).count()
        self.order_id = last_query + 1

        self.created_at = dt.datetime.now()

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'user_uuid': str(self.user_uuid),
            'paper_uuid': str(self.paper_uuid),
            'query': self.query,
            'response': self.response,
            'order_id': self.order_id,
            'created_at': self.created_at
        }


    def __repr__(self):
        return f'<Query: {self.query}, user: {self.user_uuid}>'


class Key(db.Model):
    __tablename__ = "keys"
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(32), nullable=False)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    last_used = db.Column(db.DateTime(timezone=True))
    uses = db.Column(db.Integer, default=0)
    salt = db.Column(db.String(100), nullable=False)
    max_uses = db.Column(db.Integer, default=2147483647)

    def __init__(self, user_uuid, key, max_uses=2147483647):
        self.user_uuid = user_uuid
        self.max_uses = max_uses
        self.key, self.salt = self._hash_key(key)

    @staticmethod
    def _hash_key(key, salt=None):
        print(key, salt)
        if salt is None:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedKey = bcrypt.hashpw(key.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedKey, salt

    def check_key(self, key):
        return self._hash_key(key, salt=self.salt)[0] == self.key


    def __repr__(self):
        return f'<Key: {self.key}, user: {self.user_uuid}>'

