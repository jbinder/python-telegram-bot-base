from datetime import datetime

from pony.orm import commit, db_session, select, ObjectNotFound

from components.feedback.models import Feedback
from common.decorators.retry_on_error import retry_on_error


class FeedbackService:
    @db_session
    @retry_on_error
    def add(self, user_id, text):
        Feedback(user_id=user_id, text=text, created=datetime.utcnow())
        commit()

    @db_session
    @retry_on_error
    def get(self, feedback_id):
        try:
            return Feedback[feedback_id]
        except ObjectNotFound:
            return None

    @db_session
    @retry_on_error
    def set_resolved(self, feedback_id):
        Feedback[feedback_id].done = datetime.utcnow()
        commit()

    @db_session
    @retry_on_error
    def get_all(self):
        # noinspection PyTypeChecker
        return select(feedback for feedback in Feedback)[:]

    @db_session
    @retry_on_error
    def get_stats(self):
        # noinspection PyTypeChecker
        return {
            'count': select(feedback for feedback in Feedback).count(False)
        }
