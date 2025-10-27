import os
from pydantic import BaseModel

class LocalConfig(BaseModel):
    appium_url: str = "http://127.0.0.1:4723"
    device_name: str = "emulator-5554"
    app_path: str = os.path.abspath("resources/apk/base.apk")

class BSConfig(BaseModel):
    user: str = os.getenv("BROWSERSTACK_USERNAME")
    key: str = os.getenv("BROWSERSTACK_ACCESS_KEY")
    app_id: str = os.getenv("BROWSERSTACK_APP_ID")
    device_name: str = "Google Pixel 8"
    platform_version: str = "14.0"

def get_local_config() -> LocalConfig:
    return LocalConfig()

def get_bs_config() -> BSConfig:
    return BSConfig()