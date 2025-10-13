
# AI Agent for Travel advisor and Airline selector
# imports

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


ticket_function = {
      "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

system_message = "You are a helpful assistant for an Airline called FlightAI. Wish user with Welcome message from Ailines and then start conversation "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

# This function looks rather simpler than the one from my video, because we're taking advantage of the latest Gradio updates


ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

# There's a particular dictionary structure that's required to describe our function:
tools = [{"type": "function", "function": ticket_function}]

# We have to write that function handle_tool_call:

def handle_tool_call(message):
    print("handle message ",message)
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    print(f"Tool_call called for {city}")
    price = get_ticket_price(city)
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    print(messages)
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    print(str(response))
    if response.choices[0].finish_reason == "tool_calls":
        print(f"Tool_call returned {response.choices[0].finish_reason}")
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()