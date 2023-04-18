from setup import db
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

    def hash_plain_password(self, plain_password, salt=None):
        if not salt:
            salt = bcrypt.gensalt().decode('utf-8')
        hashedPass = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        return hashedPass, salt

    def check_password(self, plain_password):
        return self.hash_plain_password(plain_password, salt=self.salt)[0] == self.password

    def __repr__(self):
        return f'<User: {self.username}>'

def enroll_user(username, email, plain_password, ip=None, user_agent=None, country=None, city=None, timezone=None, admin=False, enabled=True):
    print(f'enrolling user: {admin}, {enabled}')
    user = User()
    user.username = username
    user.email = email
    user.password, user.salt = user.hash_plain_password(plain_password)
    user.last_ip = ip
    user.last_user_agent = user_agent
    user.last_country = country
    user.last_city = city
    user.last_timezone = timezone
    user.admin = admin
    user.enabled = enabled
    return user






    def __repr__(self):
        return f'<Paper {self.title}>'

