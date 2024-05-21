import json
import logging
import os

from email_sender import send_failure_email
from norden import get_norden_data
from windguru import get_station_current_data, upload_data

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s: %(asctime)s: %(message)s"
)

ENV_VARIABLES = ["STATION_UID", "STATION_API_PASSWORD", "EMAIL_SENDER"]

for var in ENV_VARIABLES:
    if var not in os.environ:
        raise Exception(f"Missing environment variable: {var}")


def execution_response(status_code, message):
    return {
        "statusCode": status_code,
        "body": json.dumps({"status": "success", "message": message}),
    }


def lambda_handler(event, context):
    try:
        uid = os.getenv("STATION_UID")
        password = os.getenv("STATION_API_PASSWORD")

        data = get_norden_data()

        timestamp, wind, gust, direction = data

        station_data = get_station_current_data(uid, password)

        if timestamp < station_data.get("unixtime"):
            return execution_response(200, "Data is up to date")

        upload_data(uid, password, wind, gust, direction)

        return execution_response(200, "Data uploaded successfully")

    except Exception as e:
        with open("recipients.txt") as f:
            recipients = f.read().splitlines()

        send_failure_email(os.getenv("EMAIL_SENDER"), recipients, str(e))

        return execution_response(500, f"Failed to upload data: {str(e)}")
