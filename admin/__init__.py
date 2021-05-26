import os

from flask import Flask
from flask_admin import Admin
import flask_login as login
from sqlalchemy.orm import scoped_session

from admin.views.auth import AdminIndexView, AdminUserModelView, AdminIndexNoRegView
from admin.views.card import CardView, CardEventView, CardEventChoiceView
from admin.views.skill import SkillView, UmaSkillRelationView, CardSkillRelationView
from admin.views.uma import UmaView, UmaEventView, UmaEventChoiceView
from models import Umamusume, Skill, SupportCard, UmaEvent, UmaEventChoice, CardEvent, CardEventChoice, UmaSkill, \
    CardSkill, User


def init_admin(app: Flask, db_session: scoped_session):

    app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
    register = os.getenv('ALLOW_REGISTER', False).lower()
    if register == "true":
        admin = Admin(app, name='UmaSupporter', index_view=AdminIndexView(), template_mode='bootstrap3')
    else:
        admin = Admin(app, name='UmaSupporter', index_view=AdminIndexNoRegView(), template_mode='bootstrap3')

    admin.add_view(UmaView(Umamusume, db_session, category='Umamusume'))
    admin.add_view(UmaEventView(UmaEvent, db_session, category='Umamusume'))
    admin.add_view(UmaEventChoiceView(UmaEventChoice, db_session, category='Umamusume'))

    admin.add_view(CardView(SupportCard, db_session, category='Card'))
    admin.add_view(CardEventView(CardEvent, db_session, category='Card'))
    admin.add_view(CardEventChoiceView(CardEventChoice, db_session, category='Card'))

    admin.add_view(SkillView(Skill, db_session, category='Skill'))
    admin.add_view(UmaSkillRelationView(UmaSkill, db_session, category='Skill'))
    admin.add_view(CardSkillRelationView(CardSkill, db_session, category='Skill'))


    admin.add_view(AdminUserModelView(User, db_session))

    return admin


def init_login(app: Flask):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

