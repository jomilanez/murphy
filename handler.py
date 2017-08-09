# coding=utf-8
import random

HELP_MESSAGE = (u"Sie können sagen: sag mir ein Murphys Gesetz, oder, Sie können sagen exit... Wie kann Ihnen helfen?")
HELP_QUESTION = u"Wie kann Ihnen helfen?"
WELCOME_MESSAGE = u"Frag mich ein Murphy Gesetz "
GOOD_BYE_MESSAGE = u"Danke sehr. Bis zum nächsten Mal!"
SKILL_NAME = "murphy"
murphy_laws = [
    u"Das herunterfallende Toastbroat landet stets auf der beschmierten Seite.",
    u"Jedes Handy, jeder Kühlschrank, jedes Auto zerstört sich genau im Monat nach Garantieablauf selbst.",
    u"Für jedes technische Problem musst Du mindestens zweimal in den Laden gehen.",
    u"Was Du suchst, ist immer dort, wo Du ganz am Ende nachschaust.",
    u"Freunde kommen und gehen, aber Feinde sammeln sich an.",
    u"Es regnet immer dann, wenn man kurz vorher mit dem Auto in der Waschanlage war.",
    u"Sobald man etwas an den Händen hat, etwa Motoröl oder Babykotze, juckt die Nase.",
    u"Die Wahrscheinlichkeit, beobachtet zu werden, steigt proportional mit der Idiotie unseres Verhaltens.",
    u"Stets ist jene Schlange im Supermarkt die langsamste, an der man sich selbst anstellt.",
    u"Ein Darlehen bekommt man nur, wenn man nachweist, dass man keins braucht.",
    u"Im Kino setzt sich der mit dem Riesenkopf immer genau vor einen.",
    u"Sobald Du Dich hinsetzt, um endlich eine Pause zu machen, verlangt jemand nach Dir.",
    u"Klamotten gibt’s immer in zwei Größen: zu klein und zu groß. Falls etwas doch passt, ist es hässlich.",
    u"Was wir gestern teuer gekauft haben, gibt’s heute zum Sonderangebot.",
    u"Jede Berechnung, in die sich ein Fehler einschleichen kann, wird auch einen haben. Fehler summieren sich immer in die ungünstigste Richtung.",
    u"Fünf Minuten Arbeitszeit dauern immer dreimal so lange wie fünf Minuten Freizeit.",
    u"Säcke und Zelte passen nur in größere Beutel als die, aus denen man sie geholt hat. Für einen ausgepackten Koffer braucht man zwei Koffer, um dasselbe Zeug wieder hineinzubekommen.",
    u"Der langsame LKW vor Dir bei ständigem Gegenverkehr fährt genau dorthin, wo Du auch hin willst.",
    u"Es liegen nur dann Scherben auf dem Boden, wenn Du barfuß bist.",
    u"Wenn alles scheinbar gut gelaufen ist, hast Du nur etwas übersehen."
]


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


def build_speechlet_response(output, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "shouldEndSession": should_end_session
    }


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request["requestId"] +
          ", sessionId=" + session["sessionId"])
    session_attributes = {}
    speech_output = WELCOME_MESSAGE
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def handle_get_help_request(intent, session):
    attributes = {}
    speech_output = HELP_MESSAGE
    reprompt_text = HELP_QUESTION
    should_end_session = False
    return build_response(
        attributes,
        build_speechlet_response(SKILL_NAME, speech_output, reprompt_text, should_end_session)
    )


def handle_finish_session_request(intent, session):
    attributes = session["attributes"]
    reprompt_text = None
    speech_output = GOOD_BYE_MESSAGE.format(SKILL_NAME)
    should_end_session = True
    return build_response(
        attributes,
        build_speechlet_response(speech_output, reprompt_text, should_end_session)
    )


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request["requestId"] +
          ", sessionId=" + session["sessionId"])
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    if intent_name == "MurphyIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")


def handle_answer_request(intent, session):
    session_attributes = {}
    print(intent)
    speech_output = random.choice(murphy_laws)
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(speech_output, should_end_session))


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request["requestId"] +
          ", sessionId=" + session["sessionId"])


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" +
          session_started_request["requestId"] + ", sessionId=" +
          session["sessionId"])


def lambda_handler(event, context):
    print("event.session.application.applicationId=" + event["session"]["application"]["applicationId"])
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]},
                           event["session"])
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
