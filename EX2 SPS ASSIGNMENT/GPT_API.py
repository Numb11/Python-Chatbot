from openai import OpenAI
messages=[ #creation of list containing dictionary stored in variable messages
            {
            }
        ]

client = OpenAI( #Creation of OpenAI client
            api_key = '', #initalize api key to access GPT API
        )

def message_reply(message):
    # updating of messages in a format readable by GPT API
    (messages[0])['role'] = 'user'
    (messages[0])['content'] = message

    
    

    chat_completion = client.chat.completions.create(
        model='gpt-3.5-turbo', #specify what version of openAI GPT to use
        messages = messages #Give the AI API the message history
        )
    
    reply = chat_completion.choices[0].message.content #make an API request and make a request to the API with the message parameter store this in a vriable reply
    (messages[0])['role'] = 'system'
    (messages[0])['content'] = reply

    return(reply)
