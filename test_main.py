from datetime import datetime

import pytz
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint returns HTML with expected links"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    # Check for presence of our links
    html_content = response.text
    assert "/today" in html_content
    assert "/tomorrow" in html_content
    assert "/docs" in html_content
    assert "Today Tomorrow API" in html_content


def test_read_today():
    """Test the /today endpoint returns correct date format"""
    response = client.get("/today")
    assert response.status_code == 200

    data = response.json()
    assert "date" in data

    # Verify the date format matches expected pattern
    date_str = data["date"]
    # Should look like: "Sun Mar 10 21:25:05 PDT, 2024"
    try:
        # Parse the date to verify format
        pdt = pytz.timezone("America/Los_Angeles")
        current = datetime.now(pdt)

        # Basic format checks
        assert len(date_str.split()) == 6  # Should have 6 parts
        assert date_str.endswith(str(current.year))  # Should end with current year
        assert "PDT" in date_str or "PST" in date_str  # Should have timezone
    except Exception as e:
        assert False, f"Date format is incorrect: {date_str}, {e}"


def test_read_tomorrow():
    """Test the /tomorrow endpoint returns correct date format"""
    response = client.get("/tomorrow")
    assert response.status_code == 200

    data = response.json()
    assert "date" in data

    # Verify the date format matches expected pattern
    date_str = data["date"]
    # Should look like: "Mon Mar 11, 2024"
    try:
        # Parse the date to verify format
        pdt = pytz.timezone("America/Los_Angeles")
        tomorrow = datetime.now(pdt).date()

        # Basic format checks
        assert len(date_str.split()) == 4  # Should have 4 parts
        assert date_str.endswith(str(tomorrow.year))  # Should end with current year
        assert "," in date_str  # Should have a comma
    except Exception as e:
        assert False, f"Date format is incorrect: {date_str}, {e}"
