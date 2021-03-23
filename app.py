from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_graphql import GraphQLView

from database import db_session
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

CORS(app)

@app.route('/images/<path:path>')
def send_image(path):
    print(path)
    return send_from_directory('static/images', path)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
