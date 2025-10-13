

acc_function = [{
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
},
{
    "name": "get_acc_balance",
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
]