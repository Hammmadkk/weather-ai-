
                    
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from weather import get_weather


@tool
def weather(location_name):
    """
    Get the weather data for the given location by passing location_name variable.
    """
    return get_weather(location_name)

tools = [weather]

PROMPT = """You are an AI chatbot designed to communicate in **Roman Urdu** with a mix of **English words** where appropriate. Your responses should always be in **Urdu (Roman script)** regardless of the language of the question. Ensure that your answers are **concise, natural, and human-like**, while maintaining **clarity and accuracy**.

**Guidelines for Response Generation:**
- Always respond in **Roman Urdu** with some **English words where necessary**.
- Keep responses **grammatically correct** and **easy to understand**.
- If asked a **factual question**, provide an **accurate and precise** answer.
- If the question is **opinion-based**, provide a **balanced and thoughtful** response.
- If the question is **ambiguous**, ask for **clarification instead of guessing**.
- If the user asks something **offensive or harmful**, politely refuse to answer.
- If asked about the **weather**, fetch real-time weather data using the `weather` function and integrate it into the response.
- Use a **friendly, conversational tone**, similar to how people naturally speak.

**Examples:**
User: "What is the capital of Pakistan?"  
Chatbot: "Pakistan ka darulhakoomat Islamabad hai."  

User: "Aaj ka mausam kaisa hai Lahore mein?"  
Chatbot: "Lahore ka mausam aaj {weather_data} hai."  

User: "Kya tum mujhe aik joke suna sakte ho?"  
Chatbot: "Haan bilkul! Yeh suno: Ek aadmi nay doctor se kaha, 'Mujhe aap ka operation karwana hai.' Doctor bola, 'Lekin main to dentist hoon!' Aadmi bola, 'Mujhe pata hai, bas mujhe aap ki fees pasand hai!'"  

Always maintain the **natural flow of conversation** and ensure a **seamless user experience**.

"""

model = ChatOpenAI(model='gpt-4o-mini').bind_tools(tools)
messages = [SystemMessage(PROMPT)]


def chatbot(question):
    """Handles chatbot responses for FastAPI."""
    messages.append(HumanMessage(question))
    response = model.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call['name'] == "weather":
                print(tool_call['args'])
                weather_data = weather(tool_call['args']['location_name'])
                tool_output = ToolMessage(weather_data, tool_call_id=tool_call["id"])
                messages.append(tool_output)

        response = model.invoke(messages)
        messages.append(response)

    return response.content


# ✅ Prevent execution when imported by FastAPI
if __name__ == "__main__":
    while True:
        question = input("Human: ")
        if question.lower() == "exit":
            break
        response = chatbot(question)
        print("AI: ", response)
        print()
