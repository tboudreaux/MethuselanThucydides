from MT.setup import db

import uuid
from sqlalchemy.dialects.postgresql import TEXT, ARRAY, JSON
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.sql import func
import bcrypt
from sqlalchemy.dialects.postgresql import UUID
import datetime as dt
import secrets
import hashlib
import pytz

authors_papers = db.Table('authors_papers',
    db.Column('author_uuid', UUID(as_uuid=True), db.ForeignKey('authors.uuid'), primary_key=True),
    db.Column('paper_uuid', UUID(as_uuid=True), db.ForeignKey('papers.uuid'), primary_key=True)
)

papers_categories = db.Table('papers_categories',
    db.Column('paper_uuid', UUID(as_uuid=True), db.ForeignKey('papers.uuid'), primary_key=True),
    db.Column('category_uuid', UUID(as_uuid=True), db.ForeignKey('categories.uuid'), primary_key=True)
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
    categories = db.relationship("Category", secondary="papers_categories")

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

    @hybrid_property
    def published_today(self):
        return is_paper_posted_today(self.published_date)

    @published_today.expression
    def published_today(cls):
        return is_paper_posted_today(cls.published_date)

class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    display_name = db.Column(TEXT)
    ui_settings = db.Column(JSON)
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
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True)

    def __init__(self, username, email, password, ip=None, user_agent=None, country=None, city=None, timezone=None, admin=False, enabled=True):
        self.update_username(username)
        self.email = email
        self.password, self.salt = self.hash_plain_password(password)
        self.last_ip = ip
        self.last_user_agent = user_agent
        self.last_country = country
        self.last_city = city
        self.last_timezone = timezone
        self.admin = admin
        self.enabled = enabled

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'username': self.username,
            'display_name': self.display_name,
            'ui_settings': self.ui_settings,
            'email': self.email,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'last_ip': self.last_ip,
            'last_user_agent': self.last_user_agent,
            'last_country': self.last_country,
            'last_city': self.last_city,
            'last_timezone': self.last_timezone,
            'num_logins': self.num_logins,
            'num_queries': self.num_queries,
            'can_query': self.can_query,
            'enabled': self.enabled,
            'admin': self.admin
        }

    def hash_plain_password(self, plain_password, salt=None):
        if not salt:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedPass = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedPass, salt

    def check_password(self, plain_password):
        return self.hash_plain_password(plain_password, salt=self.salt)[0] == self.password

    def update_password(self, plain_password, new_password):
        if self.check_password(plain_password):
            self.password, self.salt = self.hash_plain_password(new_password)
            return True
        return False

    def update_last_login(self, ip, user_agent, country, city, timezone):
        self.last_login = func.now()
        self.last_ip = ip
        self.last_user_agent = user_agent
        self.last_country = country
        self.last_city = city
        self.last_timezone = timezone
        self.num_logins += 1

    def update_username(self, new_username):
        # Check if any other users have the same username
        checkUser = User.query.filter_by(username=new_username).first()
        if checkUser:
            return False
        self.username = new_username
        return True

    def update_display_name(self, new_display_name):
        self.display_name = new_display_name
        return True

    def update_email(self, new_email):
        self.email = new_email
        return True

    def update_enabled(self, new_enabled):
        self.enabled = new_enabled
        return True

    def disable(self):
        return self.update_enabled(False)

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

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'full_name': self.full_name,
            'first_name': self.first_name
        }

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

class Category(db.Model):
    __tablename__ = 'categories'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = db.Column(db.String(100), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)
    category_field = db.Column(db.String(100), nullable=False)
    summary = db.relationship('Summary', backref='category', lazy=True)

    def __init__(self, category_id, category_name, category_field):
        self.category_id = category_id
        self.category_name = category_name
        self.category_field = category_field

    # @staticmethod
    # def todays_summary(category_id):
    #     today = dt.date.today()
    #     return db.Session.query(Category).filter_by(category_id==category_id, date=today).first()
    #
    def __repr__(self):
        return f'<Category: {self.category_id}, UUID: {self.uuid}>'

class Summary(db.Model):
    __tablename__ = 'summaries'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.uuid'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    summary_text = db.Column(TEXT, nullable=False)

    def __init__(self, category_uuid, date, summary_text):
        self.category_uuid = category_uuid
        self.date = date
        self.summary_text = summary_text

    def __repr__(self):
        return f'<Summary: {self.uuid}, Date: {self.date}, Category: {self.category_uuid}>'


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

class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    paper_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('papers.uuid'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __init__(self, user_uuid, paper_uuid):
        self.user_uuid = user_uuid
        self.paper_uuid = paper_uuid
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return f'<Bookmark: {self.uuid}, user: {self.user_uuid}, paper: {self.paper_uuid}>'
