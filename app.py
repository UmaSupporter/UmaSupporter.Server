import os
import secrets

from flask import Flask, send_from_directory, request, flash, redirect, url_for
from flask_cors import CORS
from flask_graphql import GraphQLView

from admin import init_admin, init_login
from crawler import crawl_new_card, crawl_new_umamusume
from database import Base, engine, db_session
from schema import schema

app = Flask(__name__)
app.debug = True

CORS(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

root_password = os.environ['ROOT_PASSWORD']
Base.metadata.create_all(engine)

init_login(app)
init_admin(app, db_session)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)


@app.route('/upload', methods=['POST'])
def get_image():
    params = request.get_json()
    input_password = request.headers.get('Authorization')
    if not input_password == root_password:
        return 'field: root_password is missing or do not correct', 401

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))


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
    app.run(host='0.0.0.0', debug=True, port=5000)
