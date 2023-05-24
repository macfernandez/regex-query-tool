import flask

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "CHICHO"

app.run(debug=True)

# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# https://realpython.com/flask-connexion-rest-api-part-2/#check-your-flask-project