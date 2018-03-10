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

def store_planet_in_session(intent, session):
    card_title = intent['name']
    session_attributes = session.get('attributes', {})

    if 'Planet' in intent['slots']:
        planet = intent['slots']['Planet']['value']
        session_attributes = {'planet': planet}

        speech_output = "I know where the plans are."
        reprompt_text = None
    else:
        speech_output = "That planet is not in this system, " \
                        "Please try a new planet."
        reprompt_text = "Please try a new planet."

    should_end_session = False

    return response_builders.build_response(session_attributes,
        response_builders.build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))

def get_planet_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']

    if session_attributes.get('planet', {}):
        speech_output = "The plans are on " + session_attributes['planet']

        should_end_session = True
    else:
        speech_output = 'I do not know.'
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