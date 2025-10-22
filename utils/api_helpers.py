import requests, time, base64, json, secrets, re
import pytest
import json
import base64
import uuid


def make_session(session_cookie):
    session = requests.Session()
    session.cookies.set("GBSESS", session_cookie, domain="goodbudget.com", path="/")
    return session


def get_envelope_uuid(session_cookie,credentials, envelope_name):

    session = make_session(session_cookie)

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

def get_transactions_by_envelope_uuid(session_cookie, credentials, value_envelope_uuid):
    session = make_session(session_cookie)

    time.sleep(2)

    response = session.get(
        f"{credentials["base_url"]}/api/transactions",
        params={"count": 20, "page": 1, "envelopeUuid": value_envelope_uuid},
        timeout=10
    )
    transactions = response.json()
    return transactions


def add_transactions_by_envelope_uuid(session_cookie, credentials, transaction_name, value_envelope_uuid):
    session = make_session(session_cookie)

    transaction_uuid = str(uuid.uuid4())
    # transaction_name = "Some API Transaction"

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
    time.sleep(2)
    return {"name": transaction_name, "uuid": transaction_uuid}

def get_existing_transaction_data(transaction_uuid, credentials, session_cookie):
    session = make_session(session_cookie)
    get_response = session.get(
        f'{credentials["base_url"]}/api/transactions/get/{transaction_uuid}',
        timeout=15
    )
    get_response.raise_for_status()
    transaction_data = get_response.json()
    return transaction_data


def delete_transaction_by_uuid(session_cookie, credentials, transaction_uuid):
    session = make_session(session_cookie)
    transaction_data = get_existing_transaction_data(transaction_uuid, credentials, session_cookie)

    data_json = {
        "created":transaction_data.get("created", ""),
        "uuid": transaction_data["uuid"],
        "receiver": transaction_data.get("receiver", ""),
        "status": "DEL",
        "note": transaction_data.get("note", ""),
        "envelope": transaction_data.get("envelope", ""),
        "account": transaction_data.get("account", ""),
        "amount": transaction_data.get("amount", "0.00"),
        "nonce": transaction_data.get("nonce", ""),
        "type": transaction_data.get("type", "DEB"),
        "check_num": transaction_data.get("check_num", ""),
    }

    form = {
        "id": transaction_data["uuid"],
        "household_id": credentials["household_id"],
        "n": transaction_data.get("nonce", ""),
        "o": "transaction",
        "d": base64.b64encode(json.dumps(data_json).encode()).decode(),
    }


    del_resp = session.post(
        f'{credentials["base_url"]}/api/transactions/save',
        params={"cltVersion": "web"},
        data=form,
        timeout=15,
    )
    return del_resp

