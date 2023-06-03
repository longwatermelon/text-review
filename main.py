from analysis import analyze

messages = [
    { "sender": "A", "message": "My dog just died" },
    { "sender": "B", "message": "Lol" },
    { "sender": "A", "message": "Bro come on" },
]

(analyzed, accuracy) = analyze(messages, "B")
print("Your performance:", str(accuracy) + "%")
print(analyzed)

