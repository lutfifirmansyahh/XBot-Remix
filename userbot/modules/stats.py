import asyncio
import os
from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ustat(?: |$)(.*)")
async def _(event):
    try:
        event.pattern_match.group(1)
        await event.edit("`Processing..`")
        async with bot.conversation("@tgscanrobot") as conv:
            try:
                r1 = await conv.get_response()
                r2 = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await event.reply("Unblock @tgscanrobot plox")
            if r1.text.startswith("No"):
                return await event.edit("`No result found for`")
                p = event.client.send_messages(
                    event.chat_id,
                    r1,
                    reply_to=event.reply_to_msg_id,
                )
                event.client.send_messages(
                    event.chat_id,
                    r2,
                    reply_to=event.reply_to_msg_id,
                )
                await event.client.delete_messages(
                    conv.chat_id, [r1.id, r2.id]
                )
    except TimeoutError:
        return await event.edit("`@xbotgroup_bot isnt responding..`")
