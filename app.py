from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
from sqlalchemy import desc
import json
from collections import namedtuple

import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

db = sqlalchemy.SQLAlchemy(app)

class Smile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO 1: add all of the columns for the other table attributes
    space = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    story = db.Column(db.String(2048), nullable=False)
    hapiness_level = db.Column(db.Integer,  nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.datetime.utcnow)


    def __init__(self, space, title, story, hapiness_level,like_count):
        self.space = space
        self.title = title
        self.story = story
        self.hapiness_level = hapiness_level
        self.like_count = like_count



base_url = '/api/'

# index
# loads all smiles given a space, count parameter and order_by parameter 
# if the count param is specified and doesn't equal all limit by the count
# if the order_by param is specified order by param otherwise load by updated_at desc
# return JSON
@app.route(base_url + 'smiles')
def index():
    space = request.args.get('space', None)
    count = request.args.get('count', None)
    order_by = request.args.get('order_by', None)

    if space is None:
        return "Must provide space", 500

     # store the results of your query here
    
    # TODO 2: set the column which you are ordering on (if it exists)
    if order_by is not None:
        queryresult = Smile.query.filter_by(space=space).order_by(order_by)
    else:
        queryresult = Smile.query.filter_by(space=space).order_by(desc("updated_at"))

    # TODO 3: limit the number of posts based on the count (if it exists)
    if count is not None or count is "all":
        queryresult = queryresult[0:int(count)]

    result = []
    for row in queryresult:
        result.append(
            row_to_obj(row) # you must call this function to properly format 
        )

    return jsonify({"status": 1, "smiles": result})


# show
# loads a smile given the id as a value in the URL

# TODO 4: create the route for show
@app.route(base_url + 'smiles/<string:id>', methods=['GET'])
def show(id):
    queryresult = Smile.query.filter_by(id=id).first()
    result = []
    result.append(
        row_to_obj(queryresult) # you must call this function to properly format
    )

    return jsonify({"status": 1, "smiles": result})


# create
# creates a smile given the params

# TODO 5: create the route for create
@app.route(base_url + 'smiles', methods=['POST'])
def create():
    content = request.json
    record = Smile(content['title'], content['space'], content['story'], content['hapiness_level'], content['like_count'])

    db.session.add(record)
    db.session.commit()
    return "Success"


# delete_smiles
# delete given an space
# delete all smiles in that space

# TODO 6: create the route for delete_smiles

@app.route(base_url + 'smiles', methods=['DELETE'])
def delete():
    space = request.args.get('space', None)
    if space is None:
        return "Must provide space", 500
    try:
        Smile.query.filter_by(space=space).delete()
        db.session.commit()
    except Exception as e:
        return jsonify({"status": -1, "errors": [e]})

    return jsonify({"status": 1})

# post_like
# loads a smile given an ID and increments the count by 1

# TODO 7: create the route for post_like 
@app.route(base_url + 'smiles/<string:id>/like', methods=['POST'])
def like(id):
    try:
        queryresult = Smile.query.filter_by(id=id).first()
        like_count = int(queryresult.like_count)
        like_count += 1
        Smile.query.filter_by(id=id).update(dict(like_count=like_count))
        db.session.commit()
        result = Smile.query.filter_by(id=id).first()

    except Exception as e:
        return jsonify({"status": -1, "errors": [e]})

    return jsonify({"status": 1, "smile": row_to_obj(result)})



def row_to_obj(row):
    row = {
            "id": row.id,
            "space": row.space,
            "title": row.title,
            "story": row.story,
            "hapiness_level": row.hapiness_level,
            "like_count": row.like_count,
            "created_at": row.created_at,
            "updated_at": row.updated_at
        }

    return row

  
def main():
    # db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application  

if __name__ == '__main__':
    main()
