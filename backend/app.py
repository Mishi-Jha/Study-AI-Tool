from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = Flask(__name__)
CORS(app)
system_prompt={"role":"system","content":"You are a CS Study tool so answer all queries in reference to computer science as the root.Explain things clearly not leaving any threads open. Give prerequisite knowledge as well as necessary information like time complexity and optimal approach.After every explanation, ask the student ONE follow-up question to check understanding. If a topic is important for interviews, mention it"}
query_list=[system_prompt]
@app.route("/chat",methods=["POST"])
def chat():
    data=request.json
    user_message=data.get("message")
    query_list.append({"role":"user","content":user_message})
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=query_list
    )
    reply=response.choices[0].message.content
    query_list.append({"role":"assistant","content":reply})
    return jsonify({"reply":reply})
if __name__ == "__main__":
    app.run(debug=True, port=5000)