import json
import logging
from datetime import datetime
from typing import Union

import ask_sdk_core.utils as ask_utils
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (AbstractExceptionHandler,
                                              AbstractRequestHandler,
                                              AbstractRequestInterceptor)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.dialog import DelegateRequestDirective
from ask_sdk_model.ui import AskForPermissionsConsentCard

import menu
import resources
import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

STATES = { 
    "PROMPTED_FOR_DAILY_SPECIALS": 'PROMPTED_FOR_DAILY_SPECIALS',
    "PROMPTED_TO_ORDER_DAILY_SPECIAL": 'PROMPTED_TO_ORDER_DAILY_SPECIAL',
    "PROMPTED_TO_CUSTOMIZE" : 'PROMPTED_TO_CUSTOMIZE',
    "PROMPTED_TO_ADD_TO_ORDER": 'PROMPTED_TO_ADD_TO_ORDER',
    "PROMPTED_TO_ORDER_SPECIAL" : 'PROMPTED_TO_ORDER_SPECIAL',
    "PROMPTED_TO_CUSTOMIZE_SPECIAL_PIZZA" : 'PROMPTED_TO_CUSTOMIZE_SPECIAL_PIZZA',
    "PROMPTED_TO_HEAR_BLUE_SHIFT_SPECIAL_DETAILS": "PROMPTED_TO_HEAR_BLUE_SHIFT_SPECIAL_DETAILS"
}

class LaunchHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'LaunchRequest'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        person_id = utils.get_person_id(handler_input)
        session_attributes = handler_input.attributes_manager.session_attributes

class YesIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'AMAZON.YesIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        
        speak_output = None
        reprompt = None
        
        session_attributes = handler_input.attributes_manager.session_attributes
        state = session_attributes.get('state', None)

        day_and_period = utils.get_day_and_period(handler_input)
        day = day_and_period['day']
        period = day_and_period['period']
        
        # if we just prompted them for specials

        if state == STATES['PROMPTED_FOR_DAILY_SPECIALS']:
            print("Getting daily special for {period} on {day}".format(period, day))
            
            spoken_special = json.loads(json.dumps(menu.get_daily_special_for_period(day, period)))
            print("Daily special is {spoken_special}".format(spoken_special))

            # copying to new object to not mess up downstream storage of object in session
            
            if period == "lunch":
                handler_input.t('DAILY_LUNCH_SPECIAL',
                    day=day,
                    size=spoken_special["pizza"]["size"],
                    crust=spoken_special["pizza"]["crust"],
                    cheese=spoken_special["pizza"]["cheese"],
                    toppingsList=menu.make_speakable_list(spoken_special["pizza"]["toppings_list"]),
                    salad=spoken_special["salad"],
                    drinks=spoken_special["drinks"],
                    cost=spoken_special["cost"]
                )
            else:
                handler_input.t('DAILY_DINNER_SPECIAL',
                    day=day,
                    size=spoken_special["pizza"]["size"],
                    crust=spoken_special["pizza"]["crust"],
                    cheese=spoken_special["pizza"]["cheese"],
                    toppingsList=menu.make_speakable_list(spoken_special["pizza"]["toppings_list"]),
                    salad=spoken_special["salad"],
                    drinks=spoken_special["drinks"],
                    cost=spoken_special["cost"]
                )

            reprompt = handler_input.t('DAILY_SPECIAL_REPROMPT',
                day=day,
                period=period
            )

            session_attributes['state'] = STATES["PROMPTED_TO_ORDER_DAILY_SPECIAL"]
        
        elif state == STATES['PROMPTED_TO_ORDER_DAILY_SPECIAL']:
            daily_special = menu.get_daily_special_for_period(day, period);
            # the user answered 'yes' to ordering the daily special
            speakOutput = handler_input.t('ORDER_DAILY_SPECIAL',
                day=day,
                period=period
            );
            reprompt = handler_input.t('ORDER_DAILY_SPECIAL_REPROMPT',
                day=day,
                period=period
            )
            # let the system know we prompted to customize the pizza or salad
            session_attributes["state"] = STATES["PROMPTED_TO_ADD_TO_ORDER"]

            # lets save this order as in-progress
            session_attributes["in_progress"] = daily_special;            
        elif state == STATES['PROMPTED_TO_ADD_TO_ORDER']:
            # the user answered 'yes' to customizing something, lets find out which
            speak_output = handler_input.t('ADD_TO_ORDER')
            reprompt = handler_input.t('ADD_TO_ORDER_REPROMPT')
        elif state == STATES['PROMPTED_FOR_DAILY_SPECIALS']:
            # the user answered yes to ordering one of the special pizzas
            speak_output = handler_input.t('PROMPT_TO_CUSTOMIZE_SPECIAL',
                name=session_attributes.special_name
            );
            reprompt = handler_input.t('PROMPT_TO_CUSTOMIZE_SPECIAL_REPROMPT');
            session_attributes.state = STATES["PROMPTED_TO_CUSTOMIZE_SPECIAL_PIZZA"]
          
            # lets save this order as in-progress
            session_attributes["in_progress"] = {
                "special" : menu.get_special_pizza_details(session_attributes.special_name)
            };
        elif state == STATES['PROMPTED_FOR_DAILY_SPECIALS']:
            # user answered yes to customizing a pizza
            # send this to Alexa Conversations for customize special pizza

            try:
                name = session_attributes["in_progress"]["special"]["name"]
                handler_input.response_builder.add_directive(
                    DelegateRequestDirective(
                        target = "AMAZON.Conversations",
                        period = {
                            "until": "EXPLICIT_RETURN"
                        },
                        updated_request = {
                            "type": 'Dialog.InputRequest',
                            "input": {
                                "name": 'customizePizzaReferenceSpecial',
                                "slots": {
                                    "name": {
                                        "name" : 'name',
                                        "value": name
                                    }
                                }
                            }
                        }
                    )
                )
            except KeyError as e:
                # if we dont have a special name, lets ask for it again
                speak_output = handler_input.t("GET_SPECIAL_PIZZA_NAME")
                reprompt = handler_input.t("GET_SPECIAL_PIZZA_NAME_REPROMPT")

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class AddPizzaReferenceSpecialToOrderIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'AddPizzaReferenceSpecialToOrderIntent'

    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In AddPizzaReferenceSpecialToOrderIntentHandler");

        special_slot = ask_utils.request_util.get_slot(handler_input, 'special')
        first_authority = special_slot.resolutions.resolutions_per_authority[0]
        special = first_authority.values[0].value.name

        # the user answered yes to ordering one of the special pizzas
        speak_output = handler_input.t('PROMPT_TO_CUSTOMIZE_SPECIAL',
            name=special
        )
        reprompt = handler_input.t('PROMPT_TO_CUSTOMIZE_SPECIAL_REPROMPT')

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['state'] = STATES["PROMPTED_TO_CUSTOMIZE_SPECIAL_PIZZA"]
        # lets save this order as in-progress
        session_attr["in_progress"] = {
            "special" : menu.get_special_pizza_details(special)
        }

        return (handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class StartOverIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'StartOverIntent'
        
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        # they answered 'start over' when asked to customize/resume their in progress order
        # lets delete that state if saved

        session_attrs = handler_input.attributes_manager.session_attributes
        if session_attrs['state'] == STATES['PROMPTED_TO_CUSTOMIZE']:
            if session_attrs['in_progress'] is not None:
                del session_attrs['in_progress']

        speak_output = handler_input.t("PROMPT_FOR_ACTION")
        reprompt = handler_input.t("REPROMPT_FOR_ACTION")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class WhatsInMyOrderIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'WhatsInMyOrderIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        # They are asking what's in their current order
        session_attrs = handler_input.attributes_manager.session_attributes
        in_progress = session_attrs.get("in_progress", None)

        # they dont have an in progress order
        if in_progress is None:
            speak_output = handler_input.t("NO_CURRENT_ORDER")
            reprompt = handler_input.t("NO_CURRENT_ORDER_REPROMPT")
        else:
            speak_output = handler_input.t("CURRENT_ORDER",
                orderText=menu.generate_order_text(in_progress)
            )
            reprompt = handler_input.t("CURRENT_ORDER_REPROMPT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class NoIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'AMAZON.NoIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        speak_output = ""
        reprompt = ""
        session_attrs = handler_input.attributes_manager.session_attributes
        print("NOT SESSION ATTRS", session_attrs)
        # if we just prompted them for specials, ordering daily special, or customizing special pizza
        if session_attrs["state"] == STATES["PROMPTED_FOR_DAILY_SPECIALS"]\
            or session_attrs["state"] == STATES["PROMPTED_TO_ORDER_DAILY_SPECIAL"]\
            or session_attrs["state"] == STATES["PROMPTED_TO_ORDER_SPECIAL"]:
            
            speak_output = handler_input.t("PROMPT_FOR_ACTION")
            reprompt = handler_input.t("REMPROMPT_FOR_ACTION")
        
        # if we prompted them to customize and they said no
        if session_attrs["state"] == STATES["PROMPTED_TO_ADD_TO_ORDER"]\
            or session_attrs["state"] == STATES["PROMPTED_TO_CUSTOMIZE_SPECIAL_PIZZA"]:
            
            session_attrs["orders"] = []
            in_progress = session_attrs["in_progress"]
            session_attrs["orders"].append({
                "date": datetime.now().isoformat(),
                "order": in_progress
            })
            del session_attrs["in_progress"]
            print("ORDER TEXT", menu.generate_order_text(in_progress))
            speak_output = handler_input.t("PLACE_ORDER",
                orderText=menu.generate_order_text(in_progress)
            )
            reprompt = handler_input.t("PLACE_ORDER_REPROMPT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class ContinueOrderIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'ContinueOrderIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        # lets get the in_progress order
        session_attrs = handler_input.attributes_manager.session_attributes
        in_progress = session_attrs["in_progress"]
        order_text = menu.generate_order_text(in_progress)

        speak_output = handler_input.t("REPEAT_ORDER_AND_ADD_SOMETHING", 
            orderText=order_text
        )
        reprompt = handler_input.t("REPEAT_ORDER_AND_ADD_SOMETHING_REPROMPT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class OrderIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'OrderIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In OrderIntentHandler")

        session_attrs = handler_input.attributes_manager.session_attributes

        session_attrs['orders'] = []
        print(session_attrs)
        in_progress = session_attrs.get('in_progress', {})
        order_text = menu.generate_order_text(in_progress)

        session_attrs['orders'].append({
            "date": datetime.now().isoformat(),
            "order": in_progress
        })

        speak_output = handler_input.t("PLACE_ORDER", orderText=order_text)
        reprompt =  handler_input.t("PLACE_ORDER_REPROMPT")


        return (handler_input.response_builder
                            .speak(speak_output)
                            .ask(reprompt)
                            .response
                )

class AddSomethingIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'AddSomethingIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In AddSomethingIntentHandler")

        item_slot = ask_utils.request_util.get_slot_value(handler_input, "item")
        first_authority = item_slot.resolutions.resolutions_per_authority[0]
        item = first_authority.values[0].value.name

        if item == "pizza":
            speak_output = handler_input.t("PIZZA_ORDER_OPTIONS")
            reprompt = handler_input.t("PIZZA_ORDER_OPTIONS_REPROMPT")
        elif item == "salad":
            speak_output = handler_input.t("SALAD_ORDER_OPTIONS",
                salads=menu.make_speakable_list(menu.get_salads())
            )
            reprompt = handler_input.t("SALAD_ORDER_OPTIONS_REPROMPT")
        elif item == "side":
            speak_output = handler_input.t("SIDE_ORDER_OPTIONS",
                sides=menu.make_speakable_list(menu.get_sides())
            )
            reprompt = handler_input.t("SIDE_ORDER_OPTIONS_REPROMPT")
        elif item == "drink":
            speak_output = handler_input.t("DRINK_ORDER_OPTIONS",
                drinks=menu.make_speakable_list(menu.get_drinks())
            )
            reprompt = handler_input.t("DRINK_ORDER_OPTIONS_REPROMPT")
        elif item == "dessert":
            speak_output = handler_input.t("DESSERT_ORDER_OPTIONS",
                desserts=menu.make_speakable_list(menu.get_desserts())
            )
            reprompt = handler_input.t("DESSERT_ORDER_OPTIONS_REPROMPT")
        else:
            speak_output = handler_input.t("UNRECOGONIZED_ITEM")
            reprompt = handler_input.t("UNRECOGONIZED_ITEM_REPROMPT")

        return (
            handler_input
                .response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class HearPizzaReferenceSpecialsIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'HearPizzaReferenceSpecialsIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In HearPizzaReferenceSpecialsIntentHandler")

        specials = menu.make_speakable_list(menu.get_pizza_reference_specials())
        speak_output = handler_input.t("PIZZA_REFERENCE_SPECIALS", 
            specials=specials
        )
        reprompt = handler_input.t("PIZZA_REFERENCE_SPECIALS_REPROMPT")
        session_attrs = handler_input.attributes_manager.session_attributes
        session_attrs["state"] = STATES["PROMPTED_TO_HEAR_BLUE_SHIFT_SPECIAL_DETAILS"]
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'AMAZON.HelpIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In HelpIntentHandler")
        speak_output = handler_input.t("HELP_PROMPT")
        reprompt = handler_input.t("GENERIC_REPROMPT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class HearSpecialDetailsIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'HearSpecialDetailsIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In HearSpecialDetailsIntentHandler")

        special_slot = ask_utils.request_util.get_slot(handler_input, 'special')
        try:
            first_authority = special_slot.resolutions.resolutions_per_authority[0]
            special_name = first_authority.values[0].value.name
        except:
            special_name = None

        # if they didnt pass us a name and just asked for details 'on a special', lets prompt again for name
        if special_name is None:
            specials = menu.make_speakable_list(menu.get_pizza_reference_specials())
            speak_output = handler_input.t("REPEAT_PIZZA_REFERENCE_SPECIALS_AND_GET_NAME", 
                specials=specials,
                error=""
            )
            reprompt = handler_input.t("REPEAT_PIZZA_REFERENCE_SPECIALS_AND_GET_NAME_REPROMPT")
        
            return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
            )

        # if they passed in a name, but its not a special
        if special_name not in menu.get_pizza_reference_specials():
            specials = menu.make_speakable_list(menu.get_pizza_reference_specials())
            speak_output = handler_input.t("REPEAT_PIZZA_REFERENCE_SPECIALS_AND_GET_NAME", 
                specials=specials,
                error="Sorry, I dont recognize {} as one of our specials.".format(special_name)
            )
            reprompt = handler_input.t("REPEAT_PIZZA_REFERENCE_SPECIALS_AND_GET_NAME_REPROMPT")
        
            return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
            )

        # if we get here, we have a valid special name
        session_attrs = handler_input.attributes_manager.session_attributes();
        # if we are re-prompting them for the special name and they indicated they wanted to customize
        if session_attrs["state"] == STATES["PROMPTED_TO_CUSTOMIZE_SPECIAL_PIZZA"]:
            return (
                handler_input
                    .response_builder
                    .add_directive(
                        DelegateRequestDirective(
                            target = "AMAZON.Conversations",
                            period = {
                                "until": "EXPLICIT_RETURN"
                            },
                            updated_request = {
                                "type": "Dialog.InputRequest",
                                "input": {
                                    "name": "customizePizzaReferenceSpecial",
                                    "slots": {
                                        "name": {
                                            "name": "name",
                                            "value": special_name
                                        }
                                    }
                                }
                            }
                        )
                    )
                    .response
            )
        special = menu.get_special_pizza_details(special_name)
        speak_output = handler_input.t('PIZZA_REFERENCE_SPECIAL_DETAILS_PROMPT_TO_ORDER',
            name=special["name"],
            qty=special["qty"],
            size=special["pizza"]["size"],
            crust=special["pizza"]["crust"],
            cheese=special["pizza"]["cheese"],
            toppings=menu.make_speakable_list(special["pizza"]["toppingsList"]),
            cost=special["cost"]
        )
        reprompt = handler_input.t('PIZZA_REFERENCE_SPECIAL_DETAILS_PROMPT_TO_ORDER_REPROMPT',
            name=special["name"]
        )
        session_attrs["state"] = STATES["PROMPTED_TO_ORDER_SPECIAL"]
        session_attrs["specialName"] = special_name
        return (
            handler_input
                .response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class BuildMyOwnPizzaIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'BuildMyOwnPizzaIntent'

    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In BuildMyOwnPizzaIntentHandler")

        count_slot_value = ask_utils.request_util.get_slot_value(handler_input, 'count')

        if count_slot_value is not None:
            if count_slot_value is 2:
                return (
                    handler_input
                        .response_builder
                        .add_directive(
                            DelegateRequestDirective(
                                target = "AMAZON.Conversations",
                                period = {
                                    "until": "EXPLICIT_RETURN"
                                },
                                updated_request = {
                                    "type": "Dialog.InputRequest",
                                    "input": {
                                        "name": "startTwoToppingPizzaOrder",
                                    }
                                }
                            )
                        )
                        .response
                )

        size_slot_value = ask_utils.request_util.get_slot_value(handler_input, 'size')

        if size_slot_value is not None:
            return (
                handler_input
                    .response_builder
                    .add_directive(
                        DelegateRequestDirective(
                            target = "AMAZON.Conversations",
                            period = {
                                "until": "EXPLICIT_RETURN"
                            },
                            updated_request = {
                                "type": "Dialog.InputRequest",
                                "input": {
                                    "name": "orderSpecificSizePizza",
                                    "slots": {
                                        'name': {
                                            'name': 'size',
                                            'value': size_slot_value
                                        }
                                    }
                                }
                            }
                        )
                    )
                    .response
            )
        
        return (
            handler_input
                .response_builder
                .add_directive(
                    DelegateRequestDirective(
                        target = "AMAZON.Conversations",
                        period = {
                            "until": "EXPLICIT_RETURN"
                        },
                        updated_request = {
                            "type": 'Dialog.InputRequest',
                            "input": {
                                "name": "startPizzaOrder"
                            }
                        }
                    )
                )
                .response
        )

class GetHoursIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) == 'GetHoursIntent'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In GetHoursIntent")
        
        user = handler_input.request_envelope.context.system.user
        consent_token = user.permissions.consent_token if user.permissions is not None else None

        if consent_token is None:
            return (
                handler_input.response_builder
                .speak(handler_input.t("PERMISSIONS_ERROR"))
                .set_card(AskForPermissionsConsentCard(["read::alexa:device:all:address"]))
                .response
            )
        
        try:
            device_id = handler_input.request_envelope.context.system.device.device_id
            device_address_service_client = handler_input.service_client_factory.get_device_address_service()
            address = device_address_service_client.get_full_address(device_id)

            if address is None or (address.address_line1 is None and address.state_or_region is None):
                response = handler_input.response_builder.speak(handler_input.t("NO_ADDRESS_SET")).response
            else:
                city = address.city
                prompt = handler_input.t("CLOSEST_LOCATION", 
                    city=city
                )
                reprompt = handler_input.t("GENERIC_REPROMPT")
                response = (
                    handler_input
                        .response_builder
                        .speak(prompt)
                        .ask(reprompt)
                        .response
                    )
            return response
        except Exception as e:
            print(e)
            response = ( 
            handler_input
                .response_builder
                .speak(handler_input.t('GENERIC_REPROMPT'))
                .response
            )

# *****************************************************************************
# This is the default intent handler to handle all intent requests.
class OtherIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) != 'GetSpecialtyPizzaListIntent'\
            and ask_utils.request_util.get_intent_name(handler_input) != 'BuildMyOwnPizzaIntent'

    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        intent_name = ask_utils.request_util.get_intent_name(handler_input)
        print("In catch all intent handler. Intent invoked: {}".format(intent_name))

        speak_output = handler_input.t("GENERIC_REPROMPT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class StopIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) != 'AMAZON.StopIntent'

    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        speak_output = handler_input.t("EXIT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

class CancelIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'IntentRequest' \
            and ask_utils.request_util.get_intent_name(handler_input) != 'AMAZON.CancelIntent'

    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        speak_output = handler_input.t("PROMPT_FOR_ACTION")
        reprompt = handler_input.t("GENERIC_REPROMPT")
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class OrderPizza(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return utils.is_api_request(handler_input, 'OrderPizza')

    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In OrderPizza")
        api_arguments = utils.get_api_arguments(handler_input)
        sessiont_attrs = handler_input.attributes_manager.session_attributes
        sessiont_attrs['in_progress'] = { "pizza": api_arguments }

        return({
            "directives": [DelegateRequestDirective(
                target = "skill",
                period = {
                    "until": "EXPLICIT_RETURN"
                },
                updated_request = {
                    "type": 'IntentRequest',
                    "intent": {
                        "name": "OrderIntent"
                    }
                }
            )],
            'apiResponse': {}
            }
        )

class GetPizzaReferenceSpecialDetails(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return utils.is_api_request(handler_input, 'GetPizzaReferenceSpecialDetails')
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In GetPizzaReferenceSpecialDetails API Handler")

        api_arguments = utils.get_api_arguments(handler_input)
        special = menu.get_special_pizza_details(api_arguments["name"])

        return({
            'apiResponse': special
            }
        )

class GetRelativeFeedingSize(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return utils.is_api_request(handler_input, 'GetRelativeFeedingSize')
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In GetRelativeFeedingSize API Handler")

        api_arguments = utils.get_api_arguments(handler_input)
        feeding_size = menu.get_feeding_size(api_arguments["size"])

        return({
            'apiResponse': feeding_size
            }
        )

class OrderTwoToppingPizza(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return utils.is_api_request(handler_input, 'OrderTwoToppingPizza')
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In OrderTwoToppingPizza API Handler")

        api_arguments = utils.get_api_arguments(handler_input)
        session_attrs = handler_input.attributes_manager.session_attributes
        api_arguments["cheese"] = "normal"
        api_arguments["toppingsList"] = [api_arguments["toppingone"], api_arguments["toppingtwo"]]
        session_attrs["pizza"] = api_arguments

        return ({
            "directives": [
                DelegateRequestDirective(
                    target = "skill",
                    period = {
                        "until": "EXPLICIT_RETURN"
                    },
                    updated_request = {
                        "type": 'IntentRequest',
                        "intent": {
                            "name": "OrderIntent"
                        }
                    }
                )
            ],
            "apiResponse": {}
        })

class OrderCustomizedPizzaReferenceSpecial(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return utils.is_api_request(handler_input, 'OrderCustomizedPizzaReferenceSpecial')
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In OrderCustomizedPizzaReferenceSpecial API Handler")

        api_arguments = utils.get_api_arguments(handler_input)
        session_attrs = handler_input.attributes_manager.session_attributes

        special = {}
        special["pizza"] = {}
        special["name"] = api_arguments["name"]
        special["qty"] = api_arguments["qty"]
        special["pizza"]["size"] = api_arguments["size"]
        special["pizza"]["cheese"] = api_arguments["cheese"]
        special["pizza"]["crust"] = api_arguments["crust"]
        special["pizza"]["toppingsList"] = api_arguments["toppings"]
        special["pizza"]["cost"] = menu.get_special_cost(special["name"])
        session_attrs.in_progress = special

        return ({
            "directives": [
                DelegateRequestDirective(
                    target = "skill",
                    period = {
                        "until": "EXPLICIT_RETURN"
                    },
                    updated_request = {
                        "type": 'IntentRequest',
                        "intent": {
                            "name": "OrderIntent"
                        }
                    }
                )
            ],
            "apiResponse": {}
        })

class MenuQuestion(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return utils.is_api_request(handler_input, 'MenuQuestion')
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        print("In MenuQuestion API Handler")

        api_arguments = utils.get_api_arguments(handler_input)
        slots = utils.get_api_slots(handler_input)
        print(api_arguments)
        print(slots)

        option_value = api_arguments["option"]
        option_response = "Your choices of"

        if slots:
            option_value = slots.option.resolutionsPerAuthority[0].values[0].value.name
        
        if option_value == "size":
            option_response += "size are small, medium, large, and extra large"
        elif option_value == "crust":
            option_response += "crust are thin crust, deep dish, regular and brooklyn style"
        elif option_value == "cheese":
            option_response += "cheese are no cheese, light, normal, extra cheese or double cheese"
        
        option_response += ", what would you like"
        return {
            "apiResponse": {
                "optionResponse": option_response
            }
        }

# *****************************************************************************
# Generic session-ended handling logging the reason received, to help debug in error cases.
class SessionEndedRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return ask_utils.request_util.get_request_type(handler_input) == 'SessionEndedRequest'
    
    def handle(self, handler_input: HandlerInput) -> Union[None, Response]:
        reason = handler_input.request_envelope.request.reason
        print("Session ended with reason: ", reason)
        return handler_input.response_builder.response

class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def translate(self, key, **kwargs) -> str:
        return resources.get_translation(key, **kwargs)

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale[:2]))

        handler_input.t = self.translate

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response

        print(handler_input.request_envelope.request)
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

sb = StandardSkillBuilder()

# register request handlers
sb.add_request_handler(LaunchHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(AddPizzaReferenceSpecialToOrderIntentHandler())
sb.add_request_handler(StartOverIntentHandler())
sb.add_request_handler(WhatsInMyOrderIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(ContinueOrderIntentHandler())
sb.add_request_handler(OrderIntentHandler())
sb.add_request_handler(AddSomethingIntentHandler())
sb.add_request_handler(HearPizzaReferenceSpecialsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(HearSpecialDetailsIntentHandler())
sb.add_request_handler(BuildMyOwnPizzaIntentHandler())
sb.add_request_handler(GetHoursIntentHandler())
sb.add_request_handler(OtherIntentHandler())
sb.add_request_handler(StopIntentHandler())
sb.add_request_handler(CancelIntentHandler())
sb.add_request_handler(OrderPizza())
sb.add_request_handler(GetPizzaReferenceSpecialDetails())
sb.add_request_handler(GetRelativeFeedingSize())
sb.add_request_handler(OrderTwoToppingPizza())
sb.add_request_handler(OrderCustomizedPizzaReferenceSpecial())
sb.add_request_handler(MenuQuestion())
sb.add_request_handler(SessionEndedRequestHandler())

# interceptors
sb.add_global_request_interceptor(LocalizationInterceptor())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
