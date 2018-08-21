from random import randint

def lambda_handler(event, context):
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.b2f876d5-7104-489e-9f79-1889baf3c84a"):
        raise ValueError("Invalid Application ID")
        
    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "SessionEndedRequest":
        return on_exit()
    elif event['request']['intent']['name'] in ["AMAZON.CancelIntent", "AMAZON.StopIntent"]:
        return on_exit()
    elif event['request']['intent']['name'] in ["AMAZON.HelpIntent"]:
        return on_help()
    elif event['request']['type'] == "IntentRequest":
        return on_get_quote(event['request']['intent'])
        
    return 'Hello from Lambda'
    
quotes = {
    'stressed': ["Don't let your mind bully your body into believing it must carry the burden of its worries.", "The greatest weapon against stress is our ability to choose one thought over another."],
    'hated': ["Throughout life people will make you mad, disrespect you and treat you bad. Let God deal with the things they do, cause hate in your heart will consume you too.", "Hate cages all the good things about you."],
    'good': ["Hard work makes you feel good because you have accomplished something.", "People who produce good results feel good about themselves."],
    'romantic': ["If I had a flower for every time I thought of you...I could walk through my garden forever.", "Once upon a time there was a boy who loved a girl, and her laughter was a question he wanted to spend his whole life answering."],
    'happy': ["Folks are usually about as happy as they make their minds up to be.", "The most important thing is to enjoy your life—to be happy—it's all that matters."],
    'envious': ["Our envy always lasts longer than the happiness of those we envy.", "It is never wise to seek or wish for another's misfortune. If malice or envy were tangible and had a shape, it would be the shape of a boomerang."],
    'lazy': ["Progress isn't made by early risers. It's made by lazy men trying to find easier ways to do something.", "Inspiration is a guest that does not willingly visit the lazy."],
    'guilty': ["Guilt is a useless feeling. It's never enough to make you change direction--only enough to make you useless.", "No guilt is forgotten so long as the conscience still knows of it."],
    'sad': ["The word 'happy' would lose its meaning if it were not balanced by sadness.", "Sadness flies away on the wings of time."],
    'annoyed': ["People who annoy people; they are the luckiest people in the world.", "Some people are like clouds. When they disappear, it's a brighter day."],
    'angry': ["For every minute you remain angry, you lose sixty seconds of peace of mind.", "Some people are like clouds. When they disappear, it's a brighter day."],
    'bad': ["Some days are just bad days, that's all.", "Sometimes we need to feel bad to know what it's like to feel good."]
}

def on_get_quote(intent):
    if intent['slots']['mood']['resolutions']['resolutionsPerAuthority'][0]['status']['code'] == "ER_SUCCESS_NO_MATCH":
        resFail = format_response()
        resFail['response']['outputSpeech']['text'] = "I am sorry. I could not understand your mood. Please give me a simple word like 'sad' or 'annoyed' or 'great'"
        resFail['response']['reprompt'] = None
        resFail['response']['shouldEndSession'] = False
        return resFail
        
    resolved = intent['slots']['mood']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        
    quote = getQuote(resolved)
    resp = format_response()
    resp['response']['outputSpeech']['text'] = quote
    resp['response']['reprompt'] = None
    resp['response']['shouldEndSession'] = True
    return resp
    
def getQuote(mood):
    return quotes[mood][randint(0,1)]

def on_launch():
    resp = format_response()
    resp['response']['outputSpeech']['text'] = "Sure! Give me one word that describes how you are feeling."
    resp['response']['card'] = {
      "type": "Standard",
      "title": "Welcome to MotivateMe",
      "text": "Sure! How are you feeling?",
    }
    resp['response']['reprompt'] = None
    return resp
    
def on_exit():
    resp = format_response()
    resp['response']['outputSpeech']['text'] = "Okay! Hope you are feeling well today. Come back if you need some motivation."
    resp['response']['shouldEndSession'] = True
    return resp

def on_help():
    resp = format_response()
    resp['response']['outputSpeech']['text'] = "Motivate Me gives you an inspirational quote relating to how you are feeling. All you have to do is speak one word that describes how you are feeling. So, how are you feeling today?"
    resp['response']['reprompt'] = None
    return resp
    

def format_response():
    return {
      "version": "string",
      "response": {
        "outputSpeech": {
          "type": "PlainText",
          "text": "Plain text string to speak"
        },
        "card": {
          "type": "Standard",
          "title": "Title of the card",
          "content": "Content of a simple card",
          "text": "Text content for a standard card",
        },
        "reprompt": {
      "outputSpeech": {
        "type": "PlainText",
        "text": "Plain text string to speak",
      }
    },
        "shouldEndSession": False
     }
    }
