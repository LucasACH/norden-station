#!/bin/bash

cd .venv/lib/python3.12/site-packages/
zip -r ../../../../deployment.zip .
cd ../../../../
zip deployment.zip lambda_function.py
zip deployment.zip email_sender.py \
               email_template.html \
                lambda_function.py \
                         norden.py \
                    recipients.txt \
                       windguru.py
