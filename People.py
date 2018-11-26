from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy

import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

db = sqlalchemy.SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

base_url = '/api/'

@app.route(base_url + 'people')
def index():
    query = Person.query.all()

    result = []
    for row in query:
        result.append(
            row_to_obj(row)
        )

    return jsonify({"People": result, "result": 1})

@app.route(base_url + 'people/<int:id>', methods=["GET"])
def show(id):
    row = Person.query.filter_by(id=id).first()
    return jsonify({"person": row_to_obj(row), "status": 1}), 200


@app.route(base_url + 'person', methods=['POST'])
def create():
    person = Person(**request.json)
    db.session.add(person)
    db.session.commit()

    db.session.refresh(person)

    return jsonify({"status": 1, "person": row_to_obj(person)}), 200


def row_to_obj(row):
    row = {
            "id": row.id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "phone_number": row.phone_number,
            "address": row.address,
            "created_at": row.created_at,
            "updated_at": row.updated_at
        }

    return row

def main():
    db.create_all()
    app.run()

if __name__ == '__main__':
    app.debug = True
    main()
