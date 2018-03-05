import behaviors

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return behaviors.get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    if intent_name == 'Order66Intent':
        return behaviors.execute_order_sixty_six(session)
    elif intent_name == 'StoreDataIntent':
        return behaviors.store_data_in_session(intent, session)
    elif intent_name == 'GetDataIntent':
        return behaviors.get_data_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return behaviors.get_welcome_response(session)
    elif intent_name == "AMAZON.CancelIntent" or \
        intent_name == "AMAZON.StopIntent":
        return behaviors.handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here