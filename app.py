from flask import Flask, request, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS

import sys
import traceback

from user_interests import UserInterests
import properties
from get_stories import get_stories

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/user/recommendations', methods=['GET'])
def get_interests():
    try:
        query_parameters = request.args

        id = query_parameters.get('id')
        type = query_parameters.get('type')

        stories = get_stories(id, type)
        data = {}
        data['stories'] = stories
        return jsonify(data)
    except Exception:
        print(traceback.format_exc())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)