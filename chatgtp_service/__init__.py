# Declare variables
import json
import requests
import os

DOMAIN = 'chatgtp_service'

# config
CONF_API = 'api'
CONF_TTS = 'tts'
CONF_MAXTOKENS = 'max_tokens'
CONF_MAX_CONTEXT_LENGTH="max_context_length"
CONF_TEMPERATURE = 'temperature'
CONF_MODEL = 'model'
CONF_MESSAGE_CONTEXT = 'context_prompt'
CONF_MESSAGE_THREAD_ID = 'thread_id'
CONF_MESSAGE = 'message'
CONF_MESSAGE_POST = 'message_post'
CONF_PLAYER_ID = 'entity_id'
CONF_CACHE = 'cache'
CON_CHAT_CONTEXT_PATH = '/config/custom_components/chatgtp_service/'



def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    def ask(data_call):
        """Handle the service call."""

        # Get config
        api = str(config[DOMAIN][CONF_API])
        tts = str(config[DOMAIN][CONF_TTS])
        max_context_length = int(config[DOMAIN][CONF_MAX_CONTEXT_LENGTH])
        
        # Get data service
        media_id = data_call.data.get(CONF_PLAYER_ID)
        cache_opt = bool(data_call.data.get(CONF_CACHE))
        max_tokens = int(data_call.data.get(CONF_MAXTOKENS))
        temperature = float(data_call.data.get(CONF_TEMPERATURE, 1))
        model = str(data_call.data.get(CONF_MODEL, "text-davinci-003"))
        
        #The promp conditioning allows to set the way the AI behaves and outputs, conditionning the results, example to force the AI to output in the style of Ai assistant.
        message_thread_id= str(data_call.data.get(CONF_MESSAGE_THREAD_ID, "1")) #keeps a track of thread context
        message_context = str(data_call.data.get(CONF_MESSAGE_CONTEXT,"")[0:2000]) #Promp conditioning: Example: Act like an AI assistant. Me: My Name is Mike. and You? AI: My name is AI! 
        message = str(data_call.data.get(CONF_MESSAGE)[0:2000]) #This is your normal message input. For these case it would need to be something like, Me: I'm feeling good and you?
        message_post = str(data_call.data.get(CONF_MESSAGE_POST,"")[0:2000]) #Final message template, to condition the AI to complete the rest, including the "AI:" the AI is not outputing this prefix since it is already here...

        context = False
        context_file=CON_CHAT_CONTEXT_PATH + "context_"+message_thread_id+".txt"
        if not os.path.exists(context_file):
              open(context_file, 'w').close()

        with open(context_file, "r") as file:
            context = file.read()

        if context:
            context+="\n"+message  + "\n"+message_post #Just append the new message input and the post part if exists
        else:
            context+=message_context+ "\n"+message + "\n"+message_post; #This is the full template prompt sent to chat gtp to complete. Append this new context

        
        #Feed this context to the AI

        # HTTP Request
        url = "https://api.openai.com/v1/completions"
        # Header Parameters
        headers = {'Content-type': 'application/json',
                   'Authorization': 'Bearer '+api}

        # Body Parameters
        data = {"model": model, "prompt": context, "max_tokens": max_tokens, "temperature": temperature}
        # Get respounse from Server

        response = requests.post(url, data=json.dumps(data), headers=headers)
        response_text = response.json().get("choices")[0].get("text")


        final_context=context+response_text;

        
        if len(final_context) >= max_context_length:
            final_context = final_context[len(final_context)-max_context_length:]
            lines = final_context.splitlines()
            lines_to_keep = []
            first_line_with_start=False;
            for index_line, line in enumerate(lines):
                if line.startswith(message_post) and first_line_with_start is False:
                    first_line_with_start=index_line
                if first_line_with_start:
                    lines_to_keep.append(line)
            final_context =  message_context+"\n"+(" \n".join(lines_to_keep))

        #Store this response as new context
        if response_text:
          with open(context_file, "w") as file:
             file.write(final_context) #Append the AI response, to store for next context
            
        hass.bus.async_fire("chatgtp_service", {"result": response_text})
        
        # Call tts service from Home Assistant
        service_data = {"entity_id": media_id, "cache": cache_opt, "message": response_text}
        hass.services.call('tts', tts, service_data)
    hass.services.register(DOMAIN, "ask", ask)
    return True
