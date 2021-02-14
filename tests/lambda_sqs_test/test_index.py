##############################################################################
#  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.   #
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License").           #
#  You may not use this file except in compliance                            #
#  with the License. A copy of the License is located at                     #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  or in the "license" file accompanying this file. This file is             #
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  #
#  KIND, express or implied. See the License for the specific language       #
#  governing permissions  and limitations under the License.                 #
##############################################################################
from moto import (
    mock_s3
)
import json
import os
import boto3


os.environ["LOG_LEVEL"] = "DEBUG"



@mock_s3
def test_lambda_handler():
    session = boto3.session.Session()
    event = {}
    from lambda_sqs_test import (
        index
    )
    resp_data = index.lambda_handler(event, {})
    expected_resp = "{\"statusCode\": 200, \"body\": {\"message\": \"success\"}}"
    assert json.dumps(resp_data) == json.dumps(expected_resp)



