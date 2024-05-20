import json
from datetime import datetime
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://meteo.comisionriodelaplata.org"


def get_norden_data():
    session = requests.Session()

    # Get the main page to get the session cookie
    session.get(BASE_URL)

    endpoint = BASE_URL + "/ecsCommand.php"

    data = "p=1&p1=2&p2=1&p3=1"

    params = {"c": "telemetry/updateTelemetry"}

    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

    res = session.post(endpoint, data=data, params=params, headers=headers)

    # Remove the prefix from the response
    data = json.loads(res.text.split("|JSON**")[-1])

    table = unquote(data.get("wind").get("latest"))

    soup = BeautifulSoup(table, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if cells:
            # Add the timezone offset to the date string
            date_string = cells[0].text + "-03:00"

            return [
                int(datetime.fromisoformat(date_string).timestamp()),
                float(cells[1].text),
                float(cells[2].text),
                float(cells[4].text),
            ]
