import predict

sentiments = ["extremely negative", "negative", "neutral", "positive", "extremely positive"]
eval_names = ["blunder", "mistake", "inaccuracy", "okay", "good", "excellent", "brilliant"]

def difference(sentimentA, sentimentB):
    global sentiments
    neutral = sentiments.index("neutral");
    a = sentiments.index(sentimentA)
    b = sentiments.index(sentimentB)
    diff = a - b
    if a < neutral and b < neutral:
        return diff - 1
    if a > neutral and b > neutral:
        return diff + 1

    return sentiments.index(sentimentA) - sentiments.index(sentimentB)

def review(review_as, messages):
    for i in range(len(messages)):
        if messages[i]["sender"] != review_as or review_as == None:
            messages[i]["sentiment"] = predict.predict(messages[i]["message"])

    prev_sentiment = "neutral"
    for i in range(1, len(messages)):
        if messages[i]["sender"] != review_as or review_as == None:
            diff = difference(messages[i]["sentiment"], prev_sentiment)
            evals = {
                -5: "blunder",
                -4: "blunder",
                -3: "mistake",
                -2: "mistake",
                -1: "inaccuracy",
                0: "okay",
                1: "good",
                2: "excellent",
                3: "brilliant",
                4: "brilliant",
                5: "brilliant"
            }
            messages[i - 1]["eval"] = evals[diff]
            prev_sentiment = messages[i]["sentiment"]

    return messages

def accuracy(messages, review_as):
    res = 0.
    count = 0
    for msg in messages:
        if (msg["sender"] == review_as or review_as == None) and "eval" in msg:
            count += abs(eval_names.index(msg["eval"]) - eval_names.index("okay"))
            if eval_names.index(msg["eval"]) > eval_names.index("okay"):
                res += eval_names.index(msg["eval"]) - eval_names.index("okay")
    return res / count * 100

def analyze(messages, review_as = None):
    analysis = review(review_as, messages)
    s = ""
    for msg in analysis:
        if (msg["sender"] == review_as or review_as == None) and "eval" in msg:
            eval_sym = {
                "blunder": "⁇",
                "mistake": "⁈",
                "inaccuracy": "?",
                "okay": "=",
                "good": "✓",
                "excellent": "☆",
                "brilliant": "★"
            }[msg['eval']]
            s += f"[{eval_sym}] {msg['sender']}: {msg['message']}\n"
        else:
            s += f"    {msg['sender']}: {msg['message']}\n"
    s = s[:-1]
    return (s, accuracy(messages, review_as))

