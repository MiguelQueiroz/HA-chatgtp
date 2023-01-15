# HA-chatgtp

Just copy the contents of the folder into your custom_components folder

Then on your HA configuration.yaml file append this new service



<pre>
# ChatGTP Activate Service
chatgtp_service:
  api: "[YOUR openai secret KEY]"
  tts: "[a tts service that is available to talk the responses]" 
  max_context_length: 1000
</pre>

Note: max_context_length is the max length of the context file thread used for context. The service will always truncate if this is passing this value, by preserving the context prompt and the neareast message_post string, to avoid partial sentences that would make no sense.

The model works by conditioning the prompts to fit your needs. For that you can call the service with these data keys:

context_prompt: The prompt template/enginering to fit your model output needs.
message: This is the message input that is added to the context.
message_post: This is very useful for Assistant bot like chat, in this case you use "[AI]:" to force the AI to complete from that  prefix.

Due to context limitations, Its better for that case to use a [NAME]: form, because the service will try to truncate older context lines and use those "tags" to do that.

<pre>
service: chatgtp_service.ask
data:
  context_prompt: "Act like an AI assistant. [Me]: My Name is Mike. and You? [AI]: My name is Tau!"
  thread_id: "2"
  message: "[Me]: do short text with a paragraph"
  message_post: "[AI]:"
  max_tokens: 50
  entity_id: media_player.desktop_mediaplayer
</pre>

max_tokens is the limit of the response, token is a measure you must check with the openAI, since it defines the price you pay per token and engine model dependent.
Define the entity_id where the service will use to call the tts service
You can check the responses for each interaction on the event listener bus "chatgtp_service"

###thread_id defined the new context file that is created under this custom componenent folder. Each context can have its meaning, so, depending on the service call you can reuse a thread id, thats where the id comes into action.

## Another example ## 
You can create a context message that would be called on your automations/scripts that instead of conversational BOT, its just used to talk/advice about context variables of your home assistant:



<pre>"Room temp: 16ºc.
Heater:off.

What do you recomend me to do? act like a nice AI assistant advisor and  reply with no longer sentences!"
</pre>

<pre>"It is recommended that you turn on the heater to increase the room temperature. Additionally, you may want to consider wearing warmer clothing or using a blanket to stay warm."</pre>

This is one possible responses I received that. You can then forward this to your tts service to play in your media player


