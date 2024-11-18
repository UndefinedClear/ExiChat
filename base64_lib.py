from base64 import b64encode, b64decode

def encode(text: str) -> str:
    message_bytes = text.encode()
    base64_bytes = b64encode(message_bytes)
    base64_message = base64_bytes.decode()

    return base64_message

def decode(base64: str) -> str:
    base64_bytes = base64.encode()
    message_bytes = b64decode(base64_bytes)
    message = message_bytes.decode()

    return message