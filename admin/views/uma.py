from flask_admin.contrib import sqla


import flask_login as login


class UmaView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['uma_name', 'gamewith_wiki_id']
    column_filters = ['rare_degree']


class UmaEventView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['title', 'umamusume.uma_name', 'umamusume.gamewith_wiki_id']
    column_filters = ['title']


class UmaEventChoiceView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['title', 'event.title', 'event.umamusume.gamewith_wiki_id']
    column_filters = ['effect', 'effect_kr']
