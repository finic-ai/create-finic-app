import requests
from typing import Dict
from models import InputSchema
from playwright.sync_api import sync_playwright, Playwright
import os
from finicapi import Finic

FINIC_API_KEY = os.environ.get("FINIC_API_KEY")
finic = Finic(FINIC_API_KEY)


@finic.workflow_entrypoint
def main(input: Dict):
    validated_input = InputSchema(**input)
    secrets = finic.secrets_manager.get_credentials(validated_input.user_id)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://app.godealwise.com/")

        # Navigate to login page and login
        page.click("text=Already have an account? Sign in")
        page.fill('input[name="email"]', "email")
        page.fill('input[name="password"]', "password")
        page.click('button[type="submit"]')

        # Wait for the home page to load
        page.wait_for_load_state("networkidle", timeout=10000)

        # Take a screenshot and close the browser
        page.screenshot(path="example.png")
        browser.close()

    return {"message": "Screenshot taken successfully!"}
