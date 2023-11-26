import random
responses = {
    "tell me a joke":["I'm afraid for the calendar. Its days are numbered",
    "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.",
    "What do you call a fish wearing a bowtie? Sofishticated.",
    "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along."],

    "greeting":["Hey, there!","Hi, how are you?", "Hello :)", "Yo"],
    "how are you":["Im great!", "I am a computer so who knows!", "I'm pretty tired right now", "I'm happy!"],
    "who created you":["Joe did"],
    "whats your name":["Jerry the pyhton bot"]
}

print(responses["greeting"][random.randint(0,3)])
while True: 
    user_inp = str(input("Enter response: ")).lower()
    print((responses[user_inp][random.randint(0,len(responses[user_inp])-1)])  if user_inp in responses.keys() else "I'm not sure how to respond to that.")