from flask_admin.contrib import sqla


import flask_login as login


class SkillView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['name', 'name_kr']
    column_filters = ['grade.name', 'buff_type.name', 'distance_type.name', 'operation_type.name']


class CardSkillRelationView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['card.card_name', 'skill.name']
    column_filters = ['skill.buff_type', 'card.rare_degree']


class UmaSkillRelationView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['uma.uma_name', 'skill.name']
    column_filters = ['skill.buff_type', 'uma.rare_degree']
