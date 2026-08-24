from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import agent
from agent import run_agent
from rag_langchain import process_pdf
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)
db=None

@app.route("/upload",methods=["POST"])
def upload():
    global db
    file = request.files["file"]
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)
    db=process_pdf(file_path)
    agent.db=db
    return jsonify({"message": "PDF processed successfully", "filename": file.filename})

@app.route("/chat",methods=["POST"])
def chat():
    data=request.json
    user_message=data.get("message")
    try:
        reply = run_agent(user_message)
    except Exception as e:
        print("Error:",e)
        reply="Sorry, I ran into an error answering that. Try rephrasing your question."    
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000,use_reloader=False)