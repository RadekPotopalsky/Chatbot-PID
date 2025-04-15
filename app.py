from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# 🔑 Tvůj API klíč
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 Načteme znalostní bázi
with open("data.txt", "r", encoding="utf-8", errors="replace") as file:
    context = file.read()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    messages = [
        {"role": "system", "content": f"Jsi nápomocný asistent, který odpovídá na základě následující dokumentace:\n{context}"},
        {"role": "user", "content": user_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Nastala chyba: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
