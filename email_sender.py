import json
import os
from datetime import UTC, datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def send_failure_email(recipient, name):
    client = boto3.client(
        "ses",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    stats = client.get_send_statistics()

    last_datapoint = stats["SendDataPoints"][-1]
    last_datapoint_datetime = last_datapoint["Timestamp"]

    time_diff = datetime.now(UTC) - last_datapoint_datetime

    if time_diff > timedelta(seconds=1):
        try:
            response = client.send_templated_email(
                Source=f"Pilote Norden <{os.getenv("EMAIL_SENDER")}>",
                Template="norden-windguru-station",
                Destination={"ToAddresses": [recipient]},
                TemplateData=json.dumps({"name": name}),
            )

        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])
