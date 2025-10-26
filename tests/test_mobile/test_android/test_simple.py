import pytest
import time

@pytest.mark.mobile
def test_install_and_launch_app(mobile_driver):
    time.sleep(5)

    print(f"Current activity: !!!!!!!!!!!!!!!!!!!!!!!!!!!")
