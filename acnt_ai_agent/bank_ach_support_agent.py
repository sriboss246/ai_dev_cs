

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import Functions_set
import Db_utility
from acnt_ai_agent.Functions_set import acc_function

# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4o-mini"
openai = OpenAI()




system_message = "You are a helpful assistant for an Bank account details. Welcome user to Uthutthi bank Singapore"
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

# This function looks rather simpler than the one from my video, because we're taking advantage of the latest Gradio updates

dbutil = Db_utility.Db_utility('nonprod')

def get_acc_details(user_name):
    print(f"Tool get_acc_details called for {user_name}")
    user = user_name.lower()
    rec=dbutil.get_acc_details(user)
    return rec[0]

def get_acc_balance(acc_number):
    print(f"Tool get_acc_balance called for {acc_number}")
    rec=dbutil.get_acc_balance(acc_number)
    return rec[0]

# There's a particular dictionary structure that's required to describe our function:
print("function1 = ",Functions_set.acc_function[0])
print("function2 = ",Functions_set.acc_function[1])

tools = [{"type": "function", "function": Functions_set.acc_function[0]},{"type": "function", "function": Functions_set.acc_function[1]}]

# We have to write that function handle_tool_call:

def handle_tool_call(message):
    print("handle message ", message)
    tool_call = message.tool_calls[0]
    print(f"Tool_call called for {tool_call}")
    arguments = json.loads(tool_call.function.arguments)
    print(f"Tool_call called for {arguments}")
    function_name = tool_call.function.name
    print(f"Function_name called for {function_name}")

    if function_name == "get_acc_balance":
        print("function_name = ", function_name)
        acc_details=get_acc_details(arguments.get("user_name"))
        print("acc_details = ", acc_details)
        acc_number=acc_details[0]
        acc_balance=get_acc_balance(acc_number)
        response = {
            "role": "tool",
            "content": json.dumps({"acc_no": acc_number, "type": acc_details[1],
                                   "balance": acc_balance}),
            "tool_call_id": tool_call.id
        }
    elif function_name == "get_acc_details" :
        print("get_acc_details called")
        acc_details = get_acc_details(arguments.get("user_name"))
        print("acc_details = ", acc_details)
        response = {
            "role": "tool",
            "content": json.dumps({"acc_no": acc_details[0], "type": acc_details[1]}),
            "tool_call_id": tool_call.id
        }


    return response, arguments.get("user_name")

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        print(f"Tool_call returned {response.choices[0].finish_reason}")
        message = response.choices[0].message
        response, user_id = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()