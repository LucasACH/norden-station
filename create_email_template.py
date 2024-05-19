import os

import boto3

client = boto3.client(
    "ses",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

with open("email_template.html") as f:
    html = f.read()

template = {
    "TemplateName": "norden-windguru-station",
    "SubjectPart": "AWS Lambda | Script Execution Failure Alert",
    "TextPart": "",
    "HtmlPart": html.replace("\n", "").replace("  ", ""),
}

response = client.create_template(Template=template)

print(response)
