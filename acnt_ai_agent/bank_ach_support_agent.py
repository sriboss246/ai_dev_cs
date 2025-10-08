
#Acc support agent
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4o-mini"
openai = OpenAI()


price_function = {
    "name": "get_acc_details",
    "description": "Get the Account details of the user. Call this whenever you need to know the user account details, for example when a customer asks 'give account details'",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user id mapped to User account",
            },
        },
        "required": ["user_id"],
        "additionalProperties": False
    }
}

system_message = "You are a helpful assistant for an Bank account details. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

# This function looks rather simpler than the one from my video, because we're taking advantage of the latest Gradio updates

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()

acc_deatils = {"abc100":{"acc_no":"12345","acc_type":"savings","balance":"$8500.00"},"bcd200":{"acc_no":"12355","acc_type":"savings","balance":"$65000.00"}}

def get_acc_details(user_id):
    print(f"Tool get_acc_details called for {user_id}")
    user = user_id.lower()
    return acc_deatils.get(user, "Unknown")

# There's a particular dictionary structure that's required to describe our function:
tools = [{"type": "function", "function": price_function}]

# We have to write that function handle_tool_call:

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    user_id = arguments.get('user_id')
    acc_deatils = get_acc_details(user_id)
    response = {
        "role": "tool",
        "content": json.dumps({"acc_no": acc_deatils.get('acc_no'),"type": acc_deatils.get('acc_type'),"balance": acc_deatils.get('balance')}),
        "tool_call_id": tool_call.id
    }
    return response, user_id

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response, user_id = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()