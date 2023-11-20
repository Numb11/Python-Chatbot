from openai import OpenAI


client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key="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",
        )

def message_reply(message):
    messages=[
            {
                "role": "system",
                "content": "You are a comedic assistant that will reply to the following messages as a friend jokingly.",

                "role": "user",
                "content": "Hi, how are you today",

                "role": "system",
                "content": "Great, wish I didnt have to get up early though! What are you up to?",

                "role": "user",
                "content": str(message),
            }
        ]
    

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = messages
        )

    return(chat_completion.choices[0].message.content)


