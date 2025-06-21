from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def login_instagram():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/accounts/login/")
        page.fill("input[name='username']", "your_username_here")
        page.fill("input[name='password']", "your_password_here")
        page.click("button[type='submit']")
        page.wait_for_timeout(10000)
        context.storage_state(path="insta_state.json")
        print("✅ Login complete")

@app.route('/')
def index():
    return "AI Agent is Live 🚀"

@app.route('/login_instagram')
def trigger_login():
    login_instagram()
    return "Login script triggered!"

scheduler = BackgroundScheduler()
scheduler.add_job(login_instagram, 'cron', hour=1)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
