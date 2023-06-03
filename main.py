from analysis import analyze
import json
import sys

def get_messages():
    messages = []
    print("Type 'help' to see available commands.")

    prev_sender = ""
    while True:
        s = input("-> ")
        if s == "help":
            print("Input format is user: message. For example, to indicate that user A said hello, type 'A: hello'.")
            print("Type 'save file.txt' to save the conversation to file.txt.")
            print("Type 'load file.txt' to load a conversation from file.txt.")
            print("Type 'done' to finish.")
            continue

        if s.split()[0] == "save":
            with open(s.split()[1], "w") as f:
                json.dump(messages, f)
            print("Saved '" + s.split()[1] + "'.")
            continue

        if s.split()[0] == "load":
            with open(s.split()[1], "r") as f:
                messages = json.load(f)
            print("Loaded '" + s.split()[1] + "'.")
            continue

        if s == "done":
            break

        msg = {
            "sender": s.split(": ")[0],
            "message": s.split(": ")[1]
        }

        if msg["sender"] == prev_sender:
            messages[-1]["message"] += " " + msg["message"]
        else:
            messages.append(msg)
        prev_sender = msg["sender"]

    return messages

messages = get_messages()
if len(messages) < 2:
    print("Not enough messages to review.")
    sys.exit(0)

review_as = input("Who to review as? ")

(analyzed, accuracy) = analyze(messages, review_as)
print("Your performance:", str(accuracy) + "%")
print(analyzed)

