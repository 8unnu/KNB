async def sign_converter(sign):
    if sign == "✂️":
        return "scissors"
    elif sign == "🪨":
        return "stone"
    elif sign == "🧻":
        return "paper"

async def reverse_sign_converter(sign):
    if sign == "scissors":
        return "✂️"
    elif sign == "stone":
        return "🪨"
    elif sign == "paper":
        return "🧻"