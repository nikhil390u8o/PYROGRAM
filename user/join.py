from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types.input_stream import AudioPiped

# 🔊 aggressive loud filter
LOUD_FILTER = (
    "volume=3.5,"
    "acompressor=threshold=-25dB:ratio=14:attack=2:release=60:makeup=18,"
    "alimiter=limit=0.95,"
    "loudnorm=I=-10:TP=-0.5:LRA=5"
)

# join VC
@Client.on_message(filters.command("join", ".") & filters.me)
async def join_vc(client: Client, message: Message):

    try:
        await client.call_py.join_group_call(
            message.chat.id,
            AudioPiped(
                "song.mp3",   # audio file
                ffmpeg_filter=LOUD_FILTER
            )
        )

        await message.reply("🔊 Joined VC with loud audio")

    except Exception as e:
        await message.reply(f"VC Join Error: {e}")


# leave VC
@Client.on_message(filters.command("leave", ".") & filters.me)
async def leave_vc(client: Client, message: Message):

    try:
        await client.call_py.leave_group_call(message.chat.id)

        await message.reply("👋 Left voice chat")

    except Exception as e:
        await message.reply(f"VC Leave Error: {e}")
