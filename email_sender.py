import json
import os
from datetime import UTC, datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def send_failure_email(recipients, exception):
    client = boto3.client(
        "ses",
        region_name=os.getenv("SES_REGION"),
        aws_access_key_id=os.getenv("SES_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("SES_SECRET_ACCESS_KEY"),
    )

    templates = client.list_templates()["TemplatesMetadata"]

    template_name = os.getenv("EMAIL_TEMPLATE_NAME")

    for t in templates:
        if t["Name"] == template_name:
            break
    else:
        with open("email_template.html") as f:
            html = f.read()

        template = {
            "TemplateName": template_name,
            "SubjectPart": "PILOTE NORDEN | Script Execution Failure Alert",
            "TextPart": "",
            "HtmlPart": html.replace("\n", "").replace("  ", ""),
        }

        response = client.create_template(Template=template)

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("Failed to create email template")

    stats = client.get_send_statistics()

    # Get last email sent
    last_datapoint = stats["SendDataPoints"][-1]
    last_datapoint_datetime = last_datapoint["Timestamp"]

    time_diff = datetime.now(UTC) - last_datapoint_datetime

    # Avoid spamming the recipient
    if time_diff > timedelta(days=1):
        try:
            response = client.send_templated_email(
                Source=f"Pilote Norden <{os.getenv("EMAIL_SENDER")}>",
                Template=os.getenv("EMAIL_TEMPLATE_NAME"),
                Destination={"ToAddresses": recipients},
                TemplateData=json.dumps({"exception": exception}),
            )

        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])

