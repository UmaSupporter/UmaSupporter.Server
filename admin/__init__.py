from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import scoped_session

from admin.views.card import CardView, CardEventView, CardEventChoiceView
from admin.views.skill import SkillView, UmaSkillRelationView, CardSkillRelationView
from admin.views.uma import UmaView, UmaEventView, UmaEventChoiceView
from models import Umamusume, Skill, SupportCard, UmaEvent, UmaEventChoice, CardEvent, CardEventChoice, UmaSkill, \
    CardSkill


def init_admin(app: Flask, db_session: scoped_session):

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='UmaSupporter', template_mode='bootstrap3')

    admin.add_view(UmaView(Umamusume, db_session, category='Umamusume'))
    admin.add_view(UmaEventView(UmaEvent, db_session, category='Umamusume'))
    admin.add_view(UmaEventChoiceView(UmaEventChoice, db_session, category='Umamusume'))

    admin.add_view(CardView(SupportCard, db_session, category='Card'))
    admin.add_view(CardEventView(CardEvent, db_session, category='Card'))
    admin.add_view(CardEventChoiceView(CardEventChoice, db_session, category='Card'))

    admin.add_view(SkillView(Skill, db_session, category='Skill'))
    admin.add_view(UmaSkillRelationView(UmaSkill, db_session, category='Skill'))
    admin.add_view(CardSkillRelationView(CardSkill, db_session, category='Skill'))

    return admin
