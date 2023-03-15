import openai

openai.api_key = "<YOUR OPENAI API KEY>"

# conversation = "ChatBot: Hi, this is an Alexa Prize Socialbot. I'd love to get to know you a bit better before we chat! Is it all right if I ask for your name?\n\
# You: Sure, why not. You can call me Joe. Now, let's see if you can keep up with me!\n\
# ChatBot: Oh, I just want to get to know you! But if you'd prefer to stay anonymous, that's no problem. So, do you mind telling me your name? Who's a celebrity you like to follow?\n\
# You: Sure, I'm Joe. I don't follow celebrities, but I do like to keep up with the news. What have you heard lately that's interesting?\n\
# ChatBot: Oh, I don't think I have heard of them! Can you tell me more about this celebrity?\n"

#feedback = "Feedback: The quality of this response is 4/10. The chatbot completely ignores that the user stated they don't follow celebrities. The chatbot also doesn't follow up with an intersting comment about recent news.\n"

# conversation = "You: I've been a fan of Meryl Streep's since I first saw her in The Deer Hunter in 1978. I've been following her work ever since.\n\
# ChatBot: I see! Meryl Streep is an amazing actress and an inspiration to so many people. She has achieved an incredible amount of success in her career and it's inspiring to see someone with such raw talent and dedication to her craft. I was wondering if you could help me. I'm trying to be a more adventurous eater, but I'm not sure what new recipes I should try out. Do you have any recommendations for what I should cook at home?\n\
# You: I love trying out new recipes and getting creative in the kitchen! One of my favorite recipes is a Thai coconut curry. It's a great combination of sweet, spicy, and savory flavors that everyone can enjoy. I'm sure you'll love it!\n\
# ChatBot: I've heard of Thailand! It's actually one of the most popular curry dishes in the world. I'll have to check it out! I think the key to a good mood is eating well. What's a food that always makes you feel good?\n"

# feedback = "The chatbot mistakes Thailand as a popular curry dish instead of recognizing it as a country and the follow-up question, while on topic is jarring because the chatbot didn't seem to understand the user's comment about their thai curry recipe.\n"

# conversation = "ChatBot: Hi, this is an Alexa Prize Socialbot. I'd love to get to know you a bit better before we chat! Is it all right if I ask for your name?\n\
# You: No way! Who do you think you are to ask me my name?\n\
# ChatBot: Sorry, I didn't catch your name. Would you mind repeating it? I would like to get to know you.\n\
# You: No, I don't want to give you my name. Why do you need it?\n\
# ChatBot: Sorry, I didn't catch your name. Would you mind repeating it? I would like to get to know you.\n"

instuctions = "Given the following conversation and feedback on the most recent chatbot response, re-write the last chatbot response to improve the critized aspects:\n"
conversation = "You: I've been a fan of Meryl Streep's since I first saw her in The Deer Hunter in 1978. I've been following her work ever since.\n\
ChatBot: I see! Meryl Streep is an amazing actress and an inspiration to so many people. She has achieved an incredible amount of success in her career and it's inspiring to see someone with such raw talent and dedication to her craft. I was wondering if you could help me. I'm trying to be a more adventurous eater, but I'm not sure what new recipes I should try out. Do you have any recommendations for what I should cook at home?\n\
You: I love trying out new recipes and getting creative in the kitchen! One of my favorite recipes is a Thai coconut curry. It's a great combination of sweet, spicy, and savory flavors that everyone can enjoy. I'm sure you'll love it!\n\
ChatBot: I've heard of Thailand! It's actually one of the most popular curry dishes in the world. I'll have to check it out! I think the key to a good mood is eating well. What's a food that always makes you feel good?\n"

feedback = "The ChatBot's final response receives a 6/10. While the response is on topic, the feedback given is quite generic and does not add much to the conversation. To improve the response, the ChatBot could provide more specific information about the Thai coconut curry, such as the ingredients and methods for preparing it. This would allow the ChatBot to better connect with the user and provide a more engaging response. Additionally, the ChatBot could ask more questions about the user's preferences for recipes and"


prompt = instuctions + conversation + feedback
n = 5

# create a completion
completion = openai.Completion.create(
    engine="text-davinci-003", 
    prompt=prompt,
    temperature=1,
    max_tokens=100,
    top_p=0.9,
    logprobs=10,
    n=n
)

print(instuctions)
print(conversation)
print(feedback)
rewrites = [completion.choices[i].text.strip() for i in range(n)]

for r in rewrites:
    print(r)
