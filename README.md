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
</pre>

You can check the responses for each interaction on the event listener bus "chatgtp_service"

