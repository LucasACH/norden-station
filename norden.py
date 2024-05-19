import json
from datetime import datetime, timezone
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup


def get_norden_data():
    session = requests.Session()

    url = "http://meteo.comisionriodelaplata.org"

    session.get(url)

    endpoint = f"{url}/ecsCommand.php"

    data = "p=1&p1=2&p2=1&p3=1"

    params = {"c": "telemetry/updateTelemetry"}

    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

    res = session.post(endpoint, data=data, params=params, headers=headers)

    data = json.loads(res.text.split("|JSON**")[-1])

    table = unquote(data.get("wind").get("latest"))

    soup = BeautifulSoup(table, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        if cells:
            return {
                "timestamp": int(
                    datetime.fromisoformat(cells[0].text + "-03:00").timestamp()
                ),
                "wind": float(cells[1].text),
                "gust": float(cells[2].text),
                "direction": float(cells[4].text),
            }
