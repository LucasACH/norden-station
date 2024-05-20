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


data = [
    [1716117840000, "8.97"],
    [1716120000000, "9.01"],
    [1716121080000, "9.31"],
    [1716121440000, "8.88"],
    [1716136200000, "1.70"],
    [1716144840000, "3.04"],
    [1716148080000, "2.17"],
    [1716151320000, "0.61"],
    [1716152400000, "0.22"],
    [1716152760000, "1.27"],
    [1716153480000, "1.10"],
    [1716155280000, "0.46"],
    [1716157800000, "3.56"],
    [1716172200000, "9.83"],
    [1716175440000, "11.28"],
    [1716180120000, "12.23"],
    [1716180480000, "11.84"],
    [1716181560000, "11.91"],
    [1716181920000, "11.39"],
    [1716183720000, "12.37"],
    [1716185160000, "13.70"],
    [1716186600000, "14.07"],
    [1716193800000, "13.84"],
    [1716196320000, "14.30"],
    [1716199560000, "14.97"],
    [1716199920000, "15.94"],
]

for d in data:
    print(datetime.fromtimestamp(d[0] / 1000))
