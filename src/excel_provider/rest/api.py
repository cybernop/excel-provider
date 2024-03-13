from typing import Dict

from flask import Flask, jsonify

from excel_provider.rest.handler import RestHandler


def create_app(config: Dict):
    app = Flask(__name__)

    handler = RestHandler(config.get("handler"))
    handler.read_data()

    setattr(app, "handler", handler)

    @app.route("/sheets", methods=["GET"])
    def get_sheets():
        return jsonify(app.handler.get_sheet_names())

    @app.route("/sheet/<id>", methods=["GET"])
    def get_sheet(id):
        try:
            return jsonify(app.handler.get_data(id))
        except ValueError as e:
            return {"error": str(e)}, 404

    @app.route("/refresh", methods=["POST"])
    def post_refresh():
        app.handler.read_data()
        return jsonify({"message": "Data refreshed"})

    return app
