from typing import List

from sqlalchemy import select

from models.user import FoodCategory
from schemas.common import MetaSchema


class MetaService:
    def __init__(self, session):
        self.session = session

    def get_all_food_categories(self):
        stmt = select(FoodCategory)
        data: List[FoodCategory] = self.session.execute(stmt).scalars().all()

        res = MetaSchema.from_orm_list(data)
        return res

    def get_list_of_obj(self, data):
        return list(map(lambda obj: {'id': obj.id, 'name': obj.value, 'name_fr': obj.value_fr}, data))
    #
    # def get_meeting_note_actions(self):
    #     meeting_note_actions = self.session.query(MeetingNoteAction).all()
    #     return self.get_list_of_obj(meeting_note_actions)
    #
    # def get_meeting_note_goals(self):
    #     meeting_note_goals = self.session.query(MeetingNoteGoal).all()
    #     return self.get_list_of_obj(meeting_note_goals)
    #
    # def get_meeting_note_feelings(self):
    #     meeting_note_feelings = self.session.query(MeetingNoteFeeling).all()
    #     return self.get_list_of_obj(meeting_note_feelings)
    #
    # def get_meeting_note_behaviors(self):
    #     meeting_note_behaviors = self.session.query(MeetingNoteBehavior).all()
    #     return self.get_list_of_obj(meeting_note_behaviors)
    #
    # def get_meeting_note_categories(self):
    #     meeting_note_categories = self.session.query(MeetingNoteCategory).all()
    #     return self.get_list_of_obj(meeting_note_categories)
