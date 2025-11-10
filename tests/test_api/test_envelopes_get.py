import allure
import pytest


@pytest.mark.api
@pytest.mark.regression
@allure.label("layer", "API Tests")
@allure.tag("api", "envelopes")
@allure.feature("[API] Envelopes API")
@allure.story("Get all envelopes")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/api/envelopes", name="GET /api/envelopes")
def test_get_all_envelopes_api(api_logger, api_steps, session_cookie, credentials):

    response = api_steps.get_all_envelopes_data(session_cookie, credentials)
    api_logger.commit_log()
    api_steps.validate_schema(response, "envelopes_response.json")
