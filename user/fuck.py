import asyncio

ascii_art = [
    ".                       /¯ )",
    "                      /¯  /",
    "                    /    /",
    "              /´¯/'   '/´¯¯•¸",
    "          /'/   /    /       /¨¯\\",
    "        ('(   (   (   (  ¯~/'  ')",
    "         \\                        /",
    "          \\                _.•´",
    "            \\              (",
    "              \\"
]

async def fuck_handle(client, msg, delay=0.5):
    for i in range(1, len(ascii_art) + 1):
        frame = "\n".join(ascii_art[:i])
        try:
            await msg.edit(frame)
            await asyncio.sleep(delay)
        except Exception:
            return