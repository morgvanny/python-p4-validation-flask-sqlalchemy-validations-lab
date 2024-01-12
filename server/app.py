from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Author, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "Validations lab"


class Authors(Resource):
    def post(self):
        data = request.get_json()
        author = Author()
        try:
            for attr in data:
                setattr(author, attr, data[attr])
            author.name = data.get("name")
            db.session.add(author)
            db.session.commit()
            return make_response(author.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": e.__str__()}, 400)


api.add_resource(Authors, "/authors")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
