import requests, time, base64, json, secrets, re
import pytest
import json
import base64
import uuid

def get_envelope_uuid(session_cookie,credentials, envelope_name):

    session = requests.Session()
    session.cookies.set("GBSESS", session_cookie, domain="goodbudget.com", path="/")

    response = session.get(f"{credentials["base_url"]}/api/envelopes", timeout=10)
    response.raise_for_status()

    envelopes_data = response.json()

    for envelope_group in envelopes_data:
        for category in envelope_group.get("nodes", []):
            if "nodes" in category:
                for envelope in category["nodes"]:
                    if envelope.get("Name") == envelope_name:
                        return envelope.get("Uuid")
    return None

def get_transactions_by_uuid(session_cookie,credentials, value_envelope_uuid):
    session = requests.Session()
    session.cookies.set("GBSESS", session_cookie, domain="goodbudget.com", path="/")

    time.sleep(2)

    response = session.get(
        f"{credentials["base_url"]}/api/transactions",
        params={"count": 20, "page": 1, "envelopeUuid": value_envelope_uuid},
        timeout=10
    )
    transaction = response.json()
    return transaction


def add_transactions_by_envelope_uuid(session_cookie, credentials, value_envelope_uuid):
    session = requests.Session()
    session.cookies.set("GBSESS", session_cookie, domain="goodbudget.com", path="/")

    transaction_uuid = str(uuid.uuid4())
    transaction_name = "Some API Transaction"

    d_json = {
        "created": "2025-10-14 23:59:59",
        "uuid": transaction_uuid,
        "receiver": transaction_name,
        "note": "",
        "envelope": value_envelope_uuid,
        "account": credentials["account_uuid"],
        "amount": "100.00",
        "type": "DEB",
        "check_num": ""
    }

    form_data = {
        "id": transaction_uuid,
        "household_id": credentials["household_id"],
        "n": "",
        "o": "transaction",
        "d": base64.b64encode(json.dumps(d_json).encode()).decode()
    }

    response = session.post(
        f"{credentials["base_url"]}/api/transactions/save?cltVersion=web",
        data=form_data,
        timeout=10
    )