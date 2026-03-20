# app/conversation_context.py

USER_CONTEXT = {}

def get_context(user="default"):
    return USER_CONTEXT.get(user, {})

def set_context(user="default", key=None, value=None):

    if user not in USER_CONTEXT:
        USER_CONTEXT[user] = {}

    USER_CONTEXT[user][key] = value

def clear_context(user="default"):
    USER_CONTEXT[user] = {}