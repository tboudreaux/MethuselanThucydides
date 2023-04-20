from MT.models.models import Category
from MT.setup import db

from sqlalchemy import and_
import datetime as dt

def todays_summary(category_id):
    today = dt.date.today()
    correctCategory = Category.query.filter_by(category_id=category_id).all()
    for category in correctCategory:
        for summary in category.summary:
            if summary.date == today:
                return summary.summary_text
    return None

# TODO: get this working to query the summary for today for the given category_id
