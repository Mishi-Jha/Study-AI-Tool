from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
system_prompt={"role":"system","content":"You are a CS Study tool so answer all queries in reference to computer science as the root.Explain things clearly not leaving any threads open. Give prerequisite knowledge as well as necessary information like time complexity and optimal approach.After every explanation, ask the student ONE follow-up question to check understanding. If a topic is important for interviews, mention it"}
query_list=[system_prompt]
while True:
    user_input=input("Write a message..")
    if user_input=="quit":
        break
    query_list.append({"role": "user", "content": user_input})
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=query_list
    )
    print(response.choices[0].message.content)
    query_list.append({"role": "assistant", "content": response.choices[0].message.content})