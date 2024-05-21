import json
import logging
from datetime import UTC, datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def send_failure_email(
    sender, recipients, exception, template_name="norden-station-failure"
):
    client = boto3.client("ses")

    templates = client.list_templates()["TemplatesMetadata"]

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
                Source=f"Pilote Norden <{sender}>",
                Template=template_name,
                Destination={"ToAddresses": recipients},
                TemplateData=json.dumps({"exception": exception}),
            )

        except ClientError as e:
            logging.error(e.response["Error"]["Message"])
        else:
            logging.info(f"Email sent! Message ID: {response['MessageId']}")
