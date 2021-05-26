import os

from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_graphql import GraphQLView

from admin import init_admin, init_login
from crawler import crawl_new_card, crawl_new_umamusume
from database import Base, engine, db_session
from schema import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)
app.secret_key = os.environ['SECRET_KEY']
CORS(app)

root_password = os.environ['ROOT_PASSWORD']
Base.metadata.create_all(engine)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)


@app.route('/ops/new/card', methods=['POST'])
def new_support_card():
    params = request.get_json()
    uri = params.get('new_card_uri')
    input_password = params.get('root_password')
    if not input_password == root_password:
        return 'field: root_password is missing or do not correct', 401
    if not uri:
        return 'field: new_card_uri need.', 400
    if crawl_new_card(uri):
        return 'ok', 201
    else:
        return 'crawl failed', 202


@app.route('/ops/new/uma', methods=['POST'])
def new_umamusume():
    params = request.get_json()
    uri = params.get('new_card_uri')
    input_password = params.get('root_password')
    if not input_password == root_password:
        return 'field: root_password is missing or do not correct', 401
    if not uri:
        return 'field: new_card_uri need.', 400
    if crawl_new_umamusume(uri):
        return 'ok', 201
    else:
        return 'crawl failed', 202


@app.route('/health-check')
def health_check():
    return 'ok', 200


@app.route('/ops/update/card', methods=['POST'])
def update_support_card():
    params = request.get_json()
    uri = params.get('new_card_uri')
    input_password = params.get('root_password')
    if not input_password == root_password:
        return 'field: root_password is missing or do not correct', 401
    if not uri:
        return 'field: new_card_uri need.', 400
    if crawl_new_card(uri, True):
        return 'ok', 201
    else:
        return 'crawl failed', 202


@app.route('/ops/update/uma', methods=['POST'])
def update_umamusume():
    params = request.get_json()
    uri = params.get('new_card_uri')
    input_password = params.get('root_password')
    if not input_password == root_password:
        return 'field: root_password is missing or do not correct', 401
    if not uri:
        return 'field: new_card_uri need.', 400
    if crawl_new_umamusume(uri, True):
        return 'ok', 201
    else:
        return 'crawl failed', 202


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    init_login(app)
    init_admin(app, db_session)
    app.run(host='0.0.0.0', debug=True, port=5000)
