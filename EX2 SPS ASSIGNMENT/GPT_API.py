from openai import OpenAI


client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key='',
        )

def message_reply(message):
    messages=[
            {
            }
        ]
    (messages[0])["role"] = "user"
    (messages[0])["content"] = message

    
    

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages
        )
    
    reply = chat_completion.choices[0].message.content
    (messages[0])["role"] = "system"
    (messages[0])["content"] = reply

    return(reply)

'''while True:
    print(message_reply(input("Enter response:")))'''