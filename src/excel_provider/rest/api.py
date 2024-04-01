from typing import Dict

from flask import Flask, jsonify
from flask_swagger import swagger

from excel_provider.provider import PROVIDER_TYPES
from excel_provider.rest.handler import RestHandler


def create_app(config: Dict):
    app = Flask(__name__)

    provider_config = config["provider"]
    provider_type = PROVIDER_TYPES[provider_config["type"]]
    provider = provider_type(provider_config["config"])
    provider.initialize()

    handler = RestHandler(provider)

    setattr(app, "handler", handler)

    @app.route("/sheets", methods=["GET"])
    def get_sheets():
        """
        Get all sheets
        Returns a list of all sheets with their name and ID
        ---
        definitions:
          - schema:
              id: SheetShort
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
              required:
                - id
                - name
          - schema:
              id: SheetsOverview
              type: object
              properties:
                sheets:
                  type: array
                  items:
                    $ref: '#/definitions/SheetShort'
              required:
                - sheets
        responses:
          200:
            description: A list of all sheets
            schema:
              $ref: '#/definitions/SheetsOverview'
        """
        return jsonify(app.handler.get_sheet_names())

    @app.route("/sheet/<id>", methods=["GET"])
    def get_sheet(id):
        """
        Get detail of a sheet
        Returns the data of a sheet
        ---
        definitions:
          - schema:
              id: SheetDetail
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                column:
                  type: string
                rows:
                  type: object
                  additionalProperties:
                    type: string
              required:
                - id
                - name
                - column
                - rows
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: The ID of the sheet
        responses:
          200:
            description: The data of the sheet
            schema:
              $ref: '#/definitions/SheetDetail'
          404:
            description: Sheet not found
            schema:
              type: object
              properties:
                error:
                  type: string

        """
        result = app.handler.get_data(id)
        if result is None:
            return "", 404
        else:
            return result

    @app.route("/refresh", methods=["POST"])
    def post_refresh():
        """
        Refresh the data
        Reads the data from the Excel file again
        ---
        responses:
          200:
            description: Data refreshed
        """
        provider.initialize()
        return jsonify({"message": "Data refreshed"})

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0"
        swag["info"]["title"] = "Excel Provider"
        return jsonify(swag)

    return app
