import json
import os
from datetime import datetime

from email_sender import send_failure_email
from norden import get_norden_data
from windguru import get_station_current_data, upload_data


def lambda_handler(event, context):
    try:
        uid = os.getenv("STATION_UID")
        password = os.getenv("STATION_API_PASSWORD")

        data = get_norden_data()

        timestamp = data.get("timestamp")

        station_data = get_station_current_data(uid, password)

        if timestamp < station_data.get("unixtime"):
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "status": "success",
                        "message": f"No new data since {datetime.fromtimestamp(timestamp)}",
                    }
                ),
            }

        upload_data(
            uid, password, data.get("wind"), data.get("gust"), data.get("direction")
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"status": "success", "message": "Data uploaded successfully"}
            ),
        }

    except Exception as e:
        send_failure_email(os.getenv("EMAIL_RECIPIENT"), os.getenv("RECIPIENT_NAME"))
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"status": "error", "message": f"Failed to upload data: {str(e)}"}
            ),
        }
