from MT.models.models import User, Paper, Category, Query, Summary, Author

from sqlalchemy import or_
from sqlalchemy import func
import re

import asyncio

async def search_user(plainTextQuery):
    result = User.query.filter(or_(
            func.lower(User.username).match(func.lower(plainTextQuery)),
            func.lower(User.email).match(func.lower(plainTextQuery)),
        )).all()
    return result

async def search_paper(plainTextQuery):
    result = Paper.query.filter(or_(
            func.lower(Paper.title).match(func.lower(plainTextQuery)),
            func.lower(Paper.abstract).match(func.lower(plainTextQuery)),
            func.lower(Paper.first_author).match(func.lower(plainTextQuery)),
        )).all()
    return result

async def search_author(plainTextQuery):
    result = Author.query.filter(or_(
            Author.first_name.match(plainTextQuery),
            # re.search(plainTextQuery, ' '.join(Author.full_name)) != None,
        )).all()
    return result

async def distribute_search(plainTextQuery):
    result = await asyncio.gather(
            search_user(plainTextQuery),
            search_paper(plainTextQuery),
            search_author(plainTextQuery))
    return result
