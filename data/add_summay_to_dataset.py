import json

path1 = "model_gen_summaries.txt" 
path2 = "follow_up.json"

summary_file = open(path1, "r").readlines()
follow_up_file = open(path2, "r").readlines()
dialogue_with_summary = open("dialogue_with_summary.json", "w")

for i in range(len(summary_file)):
    summary = summary_file[i]
    summary = summary.split("summary:")[-1]
    summary = summary.strip()

    follow_up = json.loads(follow_up_file[i])
    follow_up = follow_up["followup"]

    print(summary)
    print(follow_up)

    line = {"taskname": "convo_w_history", "summary": summary, "follow_up": follow_up}
    dialogue_with_summary.write(json.dumps(line) + "\n")



