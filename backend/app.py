from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import tempfile
from rag_langchain import process_pdf, retrieve
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = Flask(__name__)
CORS(app)
system_prompt={"role":"system","content":"You are a CS Study tool so answer all queries in reference to computer science as the root.Explain things clearly not leaving any threads open. Give prerequisite knowledge as well as necessary information like time complexity and optimal approach.After every explanation, ask the student ONE follow-up question to check understanding. If a topic is important for interviews, mention it"}
query_list=[system_prompt]
db=None

@app.route("/upload",methods=["POST"])
def upload():
    global db
    file = request.files["file"]
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)
    db=process_pdf(file_path)
    return jsonify({"message": "PDF processed successfully", "filename": file.filename})

@app.route("/chat",methods=["POST"])
def chat():
    data=request.json
    user_message=data.get("message")
    augmented_message=""
    if db:
        chunks=retrieve(user_message,db)
        context="\n".join(chunks)
        augmented_message=f"Relevant notes:\n{context}\n\nQuestion: {user_message}"
    else:
        augmented_message=user_message
    query_list.append({"role": "user", "content":augmented_message})
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=query_list
    )
    reply = response.choices[0].message.content
    query_list.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)