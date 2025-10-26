import requests, time, json, base64, uuid
from utils.schema import validate_transaction_save_request


def make_session(session_cookie):
    session = requests.Session()
    session.cookies.set("GBSESS", session_cookie, domain="goodbudget.com", path="/")
    return session

def api_url(credentials, endpoint):
    base_url = credentials["base_url"].rstrip("/")
    return f"{base_url}{endpoint}"

def get_all_envelopes(session_cookie,credentials):
    session = make_session(session_cookie)
    url = api_url(credentials, "/api/envelopes")
    response = session.get(url, timeout=10)
    return response


def get_envelope_uuid(session_cookie,credentials, envelope_name):
    env_resp = get_all_envelopes(session_cookie,credentials)
    envelopes_data = env_resp.json()
    for envelope_group in envelopes_data:
        for category in envelope_group.get("nodes", []):
            if "nodes" in category:
                for envelope in category["nodes"]:
                    if envelope.get("Name") == envelope_name:
                        return envelope.get("Uuid")
    return None



def get_transactions_by_envelope_uuid(session_cookie, credentials, value_envelope_uuid):
    session = make_session(session_cookie)
    url = api_url(credentials, "/api/transactions")
    time.sleep(2)

    response = session.get(
        url,
        params={"count": 20, "page": 1, "envelopeUuid": value_envelope_uuid},
        timeout=10
    )

    return response

def add_transactions_by_envelope_uuid(session_cookie, credentials, transaction_name, value_envelope_uuid):
    session = make_session(session_cookie)
    url = api_url(credentials, "/api/transactions/save?cltVersion=web")
    transaction_uuid = str(uuid.uuid4())


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

    validate_transaction_save_request(form_data)

    request = {
        "method":"POST",
        "url":url,
        "body": form_data,
        "cookies": session_cookie
    }


    response = session.post(url, data=form_data, timeout=10)

    time.sleep(2)

    return {"name": transaction_name,
            "uuid": transaction_uuid,
            "response": response,
            "request": request
            }

def get_existing_transaction_data(transaction_uuid, credentials, session_cookie):
    session = make_session(session_cookie)

    url = api_url(credentials, f"/api/transactions/get/{transaction_uuid}")

    get_response = session.get(url, timeout=15 )

    return get_response

def delete_transaction_by_uuid(session_cookie, credentials, transaction_uuid):
    session = make_session(session_cookie)
    url = api_url(credentials, "/api/transactions/save?cltVersion=web")
    resp = get_existing_transaction_data(transaction_uuid, credentials, session_cookie)
    txn_data = resp.json()


    data_json = {
        "created":txn_data.get("created", ""),
        "uuid": txn_data["uuid"],
        "receiver": txn_data.get("receiver", ""),
        "status": "DEL",
        "note": txn_data.get("note", ""),
        "envelope": txn_data.get("envelope", ""),
        "account": txn_data.get("account", ""),
        "amount": txn_data.get("amount", "0.00"),
        "nonce": txn_data.get("nonce", ""),
        "type": txn_data.get("type", "DEB"),
        "check_num": txn_data.get("check_num", ""),
    }

    form_data = {
        "id": txn_data["uuid"],
        "household_id": credentials["household_id"],
        "n": txn_data.get("nonce", ""),
        "o": "transaction",
        "d": base64.b64encode(json.dumps(data_json).encode()).decode(),
    }

    validate_transaction_save_request(form_data)

    del_request = {
        "method": "POST",
        "url": url,
        "body": form_data,
        "cookies": session_cookie
    }

    del_response = session.post(
        url,
        data=form_data,
        timeout=15,
    )
    return {"del_response":del_response, "del_request": del_request}

