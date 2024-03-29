import logging
from datetime import datetime

from ask_sdk_core.handler_input import HandlerInput


def is_api_request(handler_input: HandlerInput, api_name: str) -> bool:
    try:
        request = handler_input.request_envelope.request
        return request.object_type == "Dialog.API.Invoked" and request.api_request.name == api_name
    except Exception as ex:
        logging.error(ex)
        return False

def get_person(handler_input: HandlerInput):
    try:
        return handler_input.request_envelope.context.System.person;
    except Exception as ex:
        logging.error(ex)
        return False

def get_person_id(handler_input: HandlerInput):
    person = get_person(handler_input)
    if person:
        return person.personId

def get_day_and_period(handler_input: HandlerInput):
    service_client_factory = handler_input.service_client_factory
    device_id = handler_input.request_envelope.context.system.device.device_id

    user_timezone = None

    try:
        ups_service_client = service_client_factory.get_ups_service()
        user_timezone = ups_service_client.get_system_time_zone(device_id)
    except Exception as e:
        print('error', e)
    

    datetime.strptime(user_timezone)
    print("User's timezone: {}".format(user_timezone))

    return {
        "period": "dinner",
        "day": ""
    }

def get_api_arguments(handler_input: HandlerInput):
    try: 
        arguments = handler_input.request_envelope.request.api_request.arguments
        return arguments
    except Exception as e:
        print(e)
        return {}

def get_api_slots(handler_input: HandlerInput):
    try:
        slots = handler_input.request_envelope.request.api_request.slots
        return slots
    except Exception as e:
        print("Error occurred while getting api request entity:", e)
        raise e
