import response_builders

def get_welcome_response(session):
    session_attributes = session.get('attributes', {})
    card_title = "Welcome"
    speech_output = "Welcome to Star Wars commands. " \
                    "Please say a command."

    reprompt_text = "Please tell me a command."
    should_end_session = False
    return response_builders.build_response(session_attributes,
        response_builders.build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))

def execute_order_sixty_six(session):
    session_attributes = session.get('attributes', {})
    card_title = "Order66"
    speech_output = "Yes, my lord."
    reprompt_text = None

    should_end_session = False
    return response_builders.build_response(session_attributes,
        response_builders.build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))

def store_data_in_session(intent, session):
    card_title = intent['name']
    session_attributes = session.get('attributes', {})

    if 'Data' in intent['slots']:
        data = intent['slots']['Data']['value']
        session_attributes = {'data': data}

        speech_output = "Data stored."
        reprompt_text = "I stored the data."
    else:
        speech_output = "I did not understand what to store." \
                        "Please tell me again."
        reprompt_text = "Please tell me again."

    should_end_session = False

    return response_builders.build_response(session_attributes,
        response_builders.build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))

def get_data_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']

    if session_attributes.get('data', {}):
        data_str = "Your data is: " + session_attributes['data']

        speech_output = "If into the security recordings you go, " \
                        "only pain will you find. " + data_str
        should_end_session = True
    else:
        speech_output = 'I have no data.'
        should_end_session = False

    reprompt_text = None

    should_end_session = True
    return response_builders.build_response(session_attributes,
        response_builders.build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = 'Session Ended'
    speech_output = 'It will be done, my Lord.'
    reprompt_text = None

    should_end_session = True
    return response_builders.build_response({},
        response_builders.build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))