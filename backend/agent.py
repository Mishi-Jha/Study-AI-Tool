from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage,ToolMessage
from dotenv import load_dotenv
from groq import BadRequestError
import os
load_dotenv()
llm=ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)
search_tool=TavilySearch(max_results=3)
db=None
@tool
def search_notes(query:str)->str:
    """Search the user's uploaded study notes for relevant information."""
    if db is None:
        return "No notes uploaded yet"
    results=db.similarity_search(query,k=3)
    return "\n".join([doc.page_content for doc in results])

tools=[search_tool,search_notes]
llm_with_tools=llm.bind_tools(tools)

def run_agent(user_message:str)->str:
    system = SystemMessage(content="You are a CS Study Buddy. Use search_notes for questions about uploaded notes. Use tavily_search_results_json for recent or general CS questions. Always explain clearly with time complexity where relevant.")
    messages=[system,HumanMessage(content=user_message)]
    try:
        response=llm_with_tools.invoke(messages)
    except BadRequestError:
        response=llm.invoke(messages)
        return response.content


    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"]=="search_notes":
                tool_result=search_notes.invoke(tool_call["args"])
            else:
                tool_result=search_tool.invoke(tool_call["args"])
            messages.append(response)   
            messages.append(ToolMessage(content=str(tool_result),tool_call_id=tool_call["id"]))
        try:
            final=llm_with_tools.invoke(messages)
        except BadRequestError:
            final=llm.invoke(messages)
        return final.content
    return response.content    