from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
query_list=[]
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