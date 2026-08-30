"""
Script automatization Mega.nz : connexion + document import.

Must have :
    pip install selenium

Environment variables to be set before execution :
    MEGA_EMAIL         -> email of the account Mega.nz
    MEGA_PASSWORD       -> password of Mega.nz
    MEGA_UPLOAD_FILE    -> (optionnel) path of the file you want to upload

Exemple (Linux/macOS) :
    export MEGA_EMAIL="your@email.com"
    export MEGA_PASSWORD="yourpassword"
    export MEGA_UPLOAD_FILE="/path/to/document.txt"
    python mega_upload.py

Exemple (PowerShell) :
    $env:MEGA_EMAIL="your@email.com"
    $env:MEGA_PASSWORD="yourpassword"
    $env:MEGA_UPLOAD_FILE="C:\\path\\to\\document.txt"
    python mega_upload.py

IMPORTANT NOTE :
    The CSS selectors below (input[name=“login”], .fm-file-upload, etc.)
    corresponded to the Mega.nz interface in 2022. Mega regularly updates
    its DOM: if the script fails with a TimeoutException, open your browser’s
    developer tools at mega.nz/login and check/adjust these
    selectors before doing anything else.
"""

import logging
import os
import sys
from contextlib import contextmanager
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 20  # secondes


def build_driver(headless: bool = True) -> webdriver.Chrome:
    """Configures and returns a Chrome WebDriver instance.

    Selenium 4+ includes Selenium Manager: it automatically downloads and manages
    the correct Chrome WebDriver; you no longer need to specify a path manually.
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


@contextmanager
def mega_session(headless: bool = True):
    """A context manager that ensures the driver is closed properly."""
    driver = build_driver(headless=headless)
    try:
        yield driver
    finally:
        driver.quit()


def login_to_mega(
    driver: webdriver.Chrome,
    email: str,
    password: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> None:
    """Connects to Mega.nz. Throws a TimeoutException if an expected item does not appear."""
    driver.get("https://mega.nz/login")

    email_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="login"]'))
    )
    email_input.clear()
    email_input.send_keys(email)

    password_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
    )
    password_input.clear()
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login-button, #login-button"))
    )
    login_button.click()

    # We expect something specific to the file system (proof of a successful connection),
    # not just “an input file exists somewhere on the page.”
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".fm-file-upload input[type='file']"))
    )
    logger.info("Successfully connected to Mega.nz.")


def import_document(
    driver: webdriver.Chrome,
    file_path: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> None:
    """Imports a document into the connected Mega.nz account."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found : {file_path}")

    file_input = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".fm-file-upload input[type='file']"))
    )
    file_input.send_keys(str(path.resolve()))

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".fm-tree-panel .tranfer-filetype-txt"))
    )
    logger.info("Document '%s' imported sucessfully", path.name)


def main() -> int:
    email = os.environ.get("MEGA_EMAIL")
    password = os.environ.get("MEGA_PASSWORD")
    file_path = os.environ.get("MEGA_UPLOAD_FILE", "/path/to/document.txt")

    if not email or not password:
        logger.error(
            "MEGA_EMAIL and MEGA_PASSWORD must be set as environment variables."
        )
        return 1

    try:
        with mega_session(headless=True) as driver:
            login_to_mega(driver, email, password)
            import_document(driver, file_path)
    except TimeoutException:
        logger.error(
            "Timeout: An expected element did not appear. "
            "The Mega.nz DOM may have changed since this script was written."
        )
        return 1
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1
    except WebDriverException as e:
        logger.error("Erreur WebDriver : %s", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
