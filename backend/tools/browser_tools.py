from playwright.sync_api import sync_playwright


class BrowserSession:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        print("[Browser] Launching browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        context = self.browser.new_context(ignore_https_errors=True)
        self.page = context.new_page()

    def navigate(self, url):
        print(f"[Browser] Navigating to {url}")
        self.page.goto(url)

    def click(self, selector):
        print(f"[Browser] Clicking: {selector}")
        self.page.click(selector)

    def fill(self, selector, value):
        print(f"[Browser] Filling: {selector} → {value}")
        self.page.fill(selector, value)

    def wait_for(self, selector):
        print(f"[Browser] Waiting for: {selector}")
        self.page.wait_for_selector(selector)