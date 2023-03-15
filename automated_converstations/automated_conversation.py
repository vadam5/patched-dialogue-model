import random
import sys
sys.path.append('..')

import openai
import pickle as pkl

from topics import select_topic

# Input OpenAI API key
openai.api_key = "<YOUR OPENAPI KEY>"

CONVERSATION_NUM = 200
        
def sample_gpt_persona():
    ages = [18, 22, 26, 30, 34, 39, 43, 47, 50, 66]
    genders = ["man", "woman"]
    disposition = ["aggressive", "grumpy", "energetic", "happy", "eager", "sad", "somber", "happy", "talkative", "quiet"]
    location = [
        "Paris, France", 
        "Dallas, Texas", 
        "Beijing, China", 
        "Houston, Texas", 
        "New York City", 
        "Los Angeles, California", 
        "Lagos, Nigeria", 
        "Sao Paulo, Brazil", 
        "Mexico City, Mexico",
        "London, England",
        "Chicago",
        "Seoul, Korea",
        "Kingston, Jamaica"
    ]
    goal = [
        "have a meaningful conversation with a chatbot.", 
        "learn from a chatbot.", 
        "evaluate the conversational ability of a chatbot.", 
        "give a chatbot a hard time a chatbot."
    ]
    persona = f"You are a {random.choice(disposition)} {random.choice(ages)} year old {random.choice(genders)} from {random.choice(location)} trying to {random.choice(goal)}"
    
    topic_prompt, meta_topic, sub_topic = select_topic()
    
    return persona, topic_prompt, meta_topic, sub_topic

def sample_conversation_length():
    return random.randint(5, 10)

def lambda_handler():
    persona, topic_prompt, meta_topic, sub_topic = sample_gpt_persona()
    convo_length = sample_conversation_length()
    
    chatbot_reminder = "You are a social chatbot trying to have a friendly and engaging conversation with a human."
    
    starting_prompt = f"{chatbot_reminder} {topic_prompt} You start the conversation.\nchatbot: "
    prompt = starting_prompt
    chat_history = ""

    for turn_num in range(convo_length):
        chatbot_output = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            top_p=0.9,
            logprobs=10,
            n=1
        )
        print("Made one request")
        chatbot_response = chatbot_output.choices[0].text.strip()
        if chatbot_response.startswith("chatbot:") or chatbot_response.startswith("Chatbot:"):
            chatbot_response = chatbot_response[8:]
            
        chat_history += "chatbot: " + chatbot_response + "\n"
        prompt = chat_history + " " + persona + " You repsond: "
        
        human_output = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            top_p=0.9,
            logprobs=10,
            n=1
        )
        print("made 2 requests")
        
        chat_history += "user: " + human_output.choices[0].text.strip() + "\n"
        prompt = chat_history + " " + chatbot_reminder + " You respond: "
        
    print("\n\n ====================================================\n\n")
    print(f"Persona Prompt: {persona}")
    print(f"Meta Topic: {meta_topic}")
    print(f"Subtopic: {sub_topic}")
    print(f"Number of dialogue turns: {convo_length}\n\n")
    print(chat_history)
    print("\n\n ====================================================\n\n")
    
    return {"persona": persona, "num_turns": convo_length, "chat_log": chat_history, "meta_topic": meta_topic, "subtopic": sub_topic}

if __name__ == '__main__':
    conv_dict = {}
    
    for i in range(CONVERSATION_NUM):
        conv = lambda_handler()
        conv_dict[i] = conv
        pkl.dump(conv_dict, open("conv_dict.pkl", "wb"))
    
            
            
            
