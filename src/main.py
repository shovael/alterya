import os
import json

from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

from const.covalent_api import CONVALENT_API_URL
from convalent_api_utils.wallet_actions import query_wallet

CONVALENT_API_KEY: str = os.getenv("CONVALENT_API_KEY")
PORT: int = 5000
app = Flask(__name__)


@app.route("/wallet_assets", methods=["GET"])
def get_assets():
    wallet_address: str = request.args.get("walletAddress")
    chain_name: str = request.args.get("chainName")
    if not wallet_address or not chain_name:
        return (
            jsonify(
                {
                    "error": f"missing arguments, walletAddress={wallet_address}, chainName={chain_name}"
                }
            ),
            400,
        )

    balance = query_wallet(CONVALENT_API_KEY, chain_name, wallet_address)

    if not balance.error:
        tokens_list = [
            token.contract_display_name or token.contract_address
            for token in balance.data.items
            if token.quote
        ]
        return jsonify({"tokens": tokens_list})
    else:
        return jsonify({"error from information server": balance.error}), 400


@app.route("/wallet_usd_total_value", methods=["GET"])
def get_wallet_usd_total_value():
    wallet_address: str = request.args.get("walletAddress")
    chain_name: str = request.args.get("chainName")
    if not wallet_address or not chain_name:
        return (
            jsonify(
                {
                    "error": f"missing arguments, walletAddress={wallet_address}, chainName={chain_name}"
                }
            ),
            400,
        )

    balance = query_wallet(
        CONVALENT_API_KEY, chain_name, wallet_address, quote_currency="USD"
    )
    if not balance.error:
        tokens_list = sum([token.quote or 0 for token in balance.data.items])
        return jsonify({"total value": tokens_list})
    else:
        return jsonify({"error from information server": balance.error}), 400


@app.route("/wallet_transactions", methods=["GET"])
def get_wallet_transactions():
    wallet_address: str = request.args.get("walletAddress")
    chain_name: str = request.args.get("chainName")
    page: int = int(request.args.get("page", 0))
    if not wallet_address or not chain_name:
        return (
            jsonify(
                {
                    "error": f"missing arguments, walletAddress={wallet_address}, chainName={chain_name}"
                }
            ),
            400,
        )

    url = f"{CONVALENT_API_URL}/{chain_name}/address/{wallet_address}/transactions_v3/page/{page}/?"
    headers = {
        "accept": "application/json",
    }
    basic = HTTPBasicAuth(CONVALENT_API_KEY, "")

    response = requests.get(url, headers=headers, auth=basic)

    if response.status_code == 200:
        result = json.loads(response.text)
        return jsonify(result["data"])
    else:
        result = json.loads(response.text)
        return jsonify(result["'error_message'"]), response.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=os.getenv("DEBUG", False), port=PORT)
