import asyncio
import random

# Mapping normal letters to small caps style
small_caps_map = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ',
    'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
    'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ',
    'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
    ' ': ' ', '💞': '💞'
}

heart_emojis = ['💞', '💕', '💖', '💘', '❤️', '💓']

def to_small_caps(text):
    return ''.join(small_caps_map.get(c.lower(), c) for c in text)

def glitch_text(text):
    result = ''
    for c in text:
        if c != ' ' and c not in heart_emojis:
            prefix = random.choice(heart_emojis) if random.choice([True, False]) else ''
            suffix = random.choice(heart_emojis) if random.choice([True, False]) else ''
            result += prefix + c + suffix
        else:
            result += c
    return result

async def lover_handle(client, event):
    base_text = "Love you meri jaan 💞"
    small_caps_text = to_small_caps(base_text)
    for i in range(10):
        if i == 9:  # Last iteration (0-based index 9 = 10th iteration)
            animated = small_caps_text  # clean text without glitch
        else:
            animated = glitch_text(small_caps_text)
        await event.edit(animated)