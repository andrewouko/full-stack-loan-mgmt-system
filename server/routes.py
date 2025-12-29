from flask import Flask, jsonify, request
import strawberry
from strawberry.flask.views import GraphQLView

from container import Container


def home():
    return "Welcome to the Loan Application API"


def add_loan_payment():
    try:
        payload = request.get_json()
        loan_service = Container.loan_service()
        loan_payment_input = loan_service.validate_and_format_loan_payment_request(
            payload)
        payment = loan_service.add_loan_payment(loan_payment_input)
        return payment.to_dict(), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def register_routes(app: Flask, schema: strawberry.Schema):
    app.add_url_rule("/", view_func=home)
    app.add_url_rule("/payment", view_func=add_loan_payment, methods=["POST"])
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql_view",
            schema=schema,
            graphiql=True,
        ),
    )
