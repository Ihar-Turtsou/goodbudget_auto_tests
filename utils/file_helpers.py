import csv, requests, os


CURRENT_FILE = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir, os.pardir))
DOWNLOAD_DIR = os.path.join(PROJECT_ROOT, "resources", "downloads")


def ensure_download_dir_exists():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    return DOWNLOAD_DIR


def get_download_path(filename="history.csv"):
    ensure_download_dir_exists()
    return os.path.join(DOWNLOAD_DIR, filename)


def download_file_from_url(url, session_cookie, path):
    content = requests.get(url, cookies={'GBSESS': session_cookie}).content
    with open(path, "wb") as file:
        file.write(content)
    return path


def assert_csv_contains(path, transaction_name):
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        assert any(
            transaction_name in row
            for row in reader
        ), f"Transaction '{transaction_name}' not found in exported CSV"