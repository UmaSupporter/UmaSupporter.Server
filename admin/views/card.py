import flask_login as login


from flask_admin.contrib import sqla


class CardView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_searchable_list = ['card_name', 'gamewith_wiki_id']
    column_filters = ['rare_degree']


class CardEventView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['title', 'support_card.card_name', 'support_card.gamewith_wiki_id']
    column_filters = ['title']


class CardEventChoiceView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_searchable_list = ['title', 'event.title', 'event.support_card.gamewith_wiki_id']
    column_filters = ['effect', 'effect_kr']
