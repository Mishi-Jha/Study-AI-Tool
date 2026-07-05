from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from rag import process_pdf, retrieve
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
    try:
        chunks=retrieve(user_message)
        context="\n".join(chunks)
        augmented_message=f"Relevant noted:\n{context}\n\nQuestion:{user_message}"
    except:
        augmented_message=user_message    
    query_list.append({"role":"user","content":augmented_message})
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=query_list
    )
    reply=response.choices[0].message.content
    query_list.append({"role":"assistant","content":reply})
    return jsonify({"reply":reply})

@app.route("/upload",methods=["POST"])
def upload():
    file=request.files["file"]
    file_path=f"./uploads/{file.filename}"
    os.makedirs("./uploads",exist_ok=True)
    file.save(file_path)
    process_pdf(file_path)
    return jsonify({"message":"PDF processed successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)