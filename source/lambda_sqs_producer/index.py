#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.   #
#                                                                            #
#  Licensed under the Amazon Software License (the "License"). You may not   #
#  use this file except in compliance with the License. A copy of the        #
#  License is located at                                                     #
#                                                                            #
#      http://aws.amazon.com/asl/                                            #
#                                                                            #
#  or in the "license" file accompanying this file. This file is distributed #
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,        #
#  express or implied. See the License for the specific language governing   #
#  permissions and limitations under the License.                            #
##############################################################################

import logging
import json
import os
import traceback
import sys
import string
import random
import datetime
import boto3
from botocore.config import Config

config = Config(
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    }
)
sqs_client = boto3.client('sqs', config=config)
queue_url = str(os.environ.get('QUEUE_URL'))


def lambda_handler(event, context):
    timeout = context.get_remaining_time_in_millis()
    logging.debug(event)
    count = int(event['count'])
    response = generate_messages(count, context, timeout / 5)

    status = '200'
    if 'Failed' in response and len(response['Failed']) > 0:
        status = '500'
    result = {
        'statusCode': status,
        'body': {
            'Successful': len(response['Successful']) if 'Successful' in response else 0,
            'Failed': len(response['Failed']) if 'Failed' in response else 0
        }
    }
    return json.dumps(result)


def generate_messages(count, context, max_timeout):
    messages = []
    i = 0
    response = {
        'Successful': [],
        'Failed': []
    }
    while context.get_remaining_time_in_millis() > max_timeout and i < count:
        i += 1
        messages.append({
            'Id': f"{i}",
            'MessageBody': ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=random.randint(8, 128))),
            'MessageAttributes': {
                'Timestamp': {
                    'StringValue': f"{datetime.datetime.now()}",
                    'DataType': 'String'
                },
                'Id': {
                    'StringValue': f"{i}",
                    'DataType': 'String'
                }
            }
        })
        if len(messages) % 10 == 0:
            response = send_messages(messages, response)
            messages = []
    if len(messages) > 0:
        response = send_messages(messages, response)
    return response


def send_messages(messages, response):
    logging.info(f"Sending {len(messages)} to sqs")
    local_response = sqs_client.send_message_batch(QueueUrl=queue_url, Entries=messages)
    response['Successful'] = response['Successful'] + local_response['Successful']
    if 'Failed' in local_response:
        response['Failed'] = response['Failed'] + local_response['Failed']
    return response


def init_logger():
    global log_level
    log_level = str(os.environ.get('LOG_LEVEL')).upper()
    if log_level not in [
        'DEBUG', 'INFO',
        'WARNING', 'ERROR',
        'CRITICAL'
    ]:
        log_level = 'ERROR'
    logging.getLogger().setLevel(log_level)


init_logger()
