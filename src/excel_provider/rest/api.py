from typing import Dict

from flask import Flask, jsonify
from flask_swagger import swagger

from excel_provider.rest.handler import RestHandler


def create_app(config: Dict):
    app = Flask(__name__)

    handler = RestHandler(config.get("handler"))
    handler.read_data()

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
                series:
                  type: array
                  items:
                    $ref: '#/definitions/Series'
              required:
                - id
                - name
                - series
          - schema:
              id: Series
              type: object
              properties:
                name:
                  type: string
                rows:
                  type: object
                  additionalProperties:
                    type: string
              required:
                - name
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
        try:
            return jsonify(app.handler.get_data(id))
        except ValueError as e:
            return {"error": str(e)}, 404

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
        app.handler.read_data()
        return jsonify({"message": "Data refreshed"})

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0"
        swag["info"]["title"] = "Excel Provider"
        return jsonify(swag)

    return app
