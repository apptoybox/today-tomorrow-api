from datetime import datetime, timedelta

import pytz
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Today Tomorrow API",
    description="A simple API that returns today's and tomorrow's dates",
    version="1.0.0",
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Return a simple HTML page with links to other endpoints"""
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Today Tomorrow API</title>
            <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 0 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #333;
                }
                .links {
                    margin: 20px 0;
                }
                a {
                    color: #0066cc;
                    text-decoration: none;
                    margin-right: 20px;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Today Tomorrow API</h1>
            <div class="links">
                <a href="/today">Today's Date</a>
                <a href="/tomorrow">Tomorrow's Date</a>
                <a href="/docs">API Documentation</a>
            </div>
        </body>
    </html>
    """
    return html_content


@app.get("/today")
async def get_today():
    """Return today's date in PDT timezone"""
    pdt = pytz.timezone("America/Los_Angeles")
    today = datetime.now(pdt)
    return {"date": today.strftime("%a %b %d %H:%M:%S %Z, %Y")}


@app.get("/tomorrow")
async def get_tomorrow():
    """Return tomorrow's date in PDT timezone"""
    pdt = pytz.timezone("America/Los_Angeles")
    tomorrow = datetime.now(pdt) + timedelta(days=1)
    return {"date": tomorrow.strftime("%a %b %d, %Y")}
