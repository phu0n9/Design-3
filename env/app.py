import json

from flask import request, jsonify
from flask import Flask,render_template

app = Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]
data = [{}]

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html",data = data)
    else:
        req = request.json
        data.append(req)
        print(data)
        return jsonify(data)

@app.route('/hi',methods=['GET'])
def hi():
    return jsonify(data)


if __name__ == "__app__":
    app.run(host='0.0.0.0', port=80, debug=True)

