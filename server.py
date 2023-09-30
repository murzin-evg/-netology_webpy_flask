import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
import schema
from models import Session, Ad


app = flask.Flask("Ad_app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"status": "error", "description": er.message})
    response.status_code = er.status_code
    return response


def get_ad(session, id):
    ad = session.get(Ad, id)
    if ad is None:
        raise HttpError(404, "Ad not found")
    return ad


class AdView(MethodView):
    def get(self, id):
        with Session() as session:
            ad = get_ad(session, id)
            try:
                return jsonify(
                    {
                        "id": ad.id,
                        "header": ad.header,
                        "description": ad.description,
                        "creation_time": ad.creation_time.isoformat(),
                        'owner': ad.owner
                    }
                )
            except:
                return ad

    def post(self):

        validated_json = validate(schema.CreateAd, request.json)

        with Session() as session:
            ad = Ad(**validated_json)
            session.add(ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "Ad already exists")
            return jsonify({"id": ad.id})

    def delete(self, id):
        with Session() as session:
            ad = get_ad(session, id)
            session.delete(ad)
            session.commit()
            return jsonify({"status": "success"})


ad_view = AdView.as_view("ads")

app.add_url_rule(
    "/ad/<int:id>", view_func=ad_view, methods=["GET", "DELETE"]
)

app.add_url_rule(
    "/ad/", view_func=ad_view, methods=["POST"]
)

if __name__ == "__main__":
    app.run()
