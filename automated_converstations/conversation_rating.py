import openai
import pickle as pkl
import time

openai.api_key = "<YOUR OPENAI KEY>"

# Load conversations
conv_dict = pkl.load(open("conv_dict.pkl", "rb"))
num_convs = len(conv_dict)
instuctions = "Given the following conversation, rate the ChatBot's final response out of 10 and give detailed feedback on what went wrong and how it can be improved:\n"

feedback_list = []

for n in range(num_convs):
    conv = conv_dict[n]
    print(conv["persona"])
   
    conv_log = conv["chat_log"]
    conv_log = conv_log.split("\n")
    chunck_start = 0
    
    try:
   
        for chunck_end in range(3, len(conv_log), 2):
            conv_chunck = conv_log[chunck_start: chunck_end]
            chunck_start = chunck_end - 1
            
            conv_chunk_string = "\n".join(conv_chunck)
            prompt = instuctions + conv_chunk_string

            completion = openai.Completion.create(
                engine="text-davinci-003", 
                prompt=prompt,
                temperature=1,
                max_tokens=100,
                top_p=0.9,
                logprobs=10,
                n=1
            )
            
            rating_and_feedback = completion.choices[0].text.strip()
            
            try:
                rating, feedback = rating_and_feedback.split("/10")
                rating = rating.replace("Rating:", "").strip()
                feedback_dict = {
                    "convo_chunk" : conv_chunk_string, 
                    "final_bot_response": conv_chunck[-1], 
                    "rating": int(rating), 
                    "feedback": feedback
                }
                feedback_list.append(feedback_dict)
            except:
                print(f"couldn't parse the feedback given:\n{rating_and_feedback}")
                print("=" * 100)
                
            time.sleep(1)
    except:
        print("Open AI server got over loaded")
        continue
            
        
        
pkl.dump(feedback_list, open("feedback_list.pkl", "wb"))
