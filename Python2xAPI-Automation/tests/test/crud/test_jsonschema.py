#Get Response
#Create the JSON schema - https://www.jsonschema.net/app/schemas
#After that save the schema into json.file
#if you want to validate the json schema - https://www.jsonschemavalidator.net/

import json
import os
import allure
import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from src.constants.api_constants import APIConstants
from src.helpers.api_requests_wrapper import post_request
from src.helpers.common_verification import verify_http_status_code, verify_json_key_for_not_null
from src.helpers.payload_manager import payload_create_booking
from src.utils.utils import Util

class TestCreateBookingJSONSchema(object):
    def load_schema(self, file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    @pytest.mark.positive
    @allure.title("Verify the create booking schema file is fetched from the path")
    @allure.description("Create booking schema should be fetched ")
    def test_create_booking_schema(self):
        response = post_request(url=APIConstants.url_create_booking(),
                                auth=None,
                                headers=Util().common_headers_json(),
                                payload=payload_create_booking(),
                                in_json=False)
        booking_id = response.json()["bookingid"]
        verify_http_status_code(response_data=response, expect_data=200)
        verify_json_key_for_not_null(booking_id)
        # response with schema.json stored
        file_path =os.getcwd()+"\create_booking_schema.json"
        schema = self.load_schema(file_name=file_path)

        try:
            validate(instance=response.json(), schema=schema)
        except ValidationError as e:
            print(e.message)
            pytest.fail("Failed : JSON schema error") #givem command to fail the test case even though error is caught in exception