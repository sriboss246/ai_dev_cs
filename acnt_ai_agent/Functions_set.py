

acc_function = [{
    "name": "get_acc_details",
    "description": "Get the Account details of the user. When user want to know about account details ask for user name if you dont have, once you have user name then call this function",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {
                "type": "string",
                "description": "The user id mapped to User account",
            },
        },
        "required": ["user_name"],
        "additionalProperties": False
    }
}
,
{
    "name": "get_acc_balance",
    "description": "Get the Account balance of the user. "
                   "Call this whenever as to check account balance, if you have user name then call this function, otherwise ask for username and then call this function",
    "parameters": {
        "type": "object",
        "properties": {
            "user_name": {
                "type": "string",
                "description": "The account_number mapped to User account",
            },
        },
        "required": ["user_name"],
        "additionalProperties": False
    }
}
]