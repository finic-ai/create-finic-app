import requests
from typing import Dict
from models import InputSchema
from playwright.sync_api import sync_playwright, Playwright
import os
from finicapi import Finic
from dotenv import load_dotenv

load_dotenv(override=True)
FINIC_API_KEY = os.getenv("FINIC_API_KEY")
finic = Finic(
    api_key=FINIC_API_KEY,
)


@finic.workflow_entrypoint
def main(input: Dict):
    validated_input = InputSchema(**input)
    secrets = finic.secrets_manager.get_credentials(validated_input.user_id)

    html_element = None

    print("Running the Playwright script")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the website and login
        page.goto("https://practicetestautomation.com/practice-test-login/")
        page.fill('input[name="username"]', "student")
        page.fill('input[name="password"]', "Password123")
        page.click('button[id="submit"]')

        # Wait for the home page to load
        page.wait_for_load_state("networkidle", timeout=10000)

        # Get the <p> tag
        html_element = page.inner_html("p")
        browser.close()

    return {"html_element": html_element}
