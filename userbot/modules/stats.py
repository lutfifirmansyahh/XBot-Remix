import random
import requests
from asyncio.exceptions import TimeoutError

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.ustat")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Balas di Pesan Goblok!!.```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Balas di Pesan Goblok!!```")
    chat = "@tgscanrobot"
    if reply_message.sender.bot:
        return await qotli.edit("```Balas di Pesan Goblok!!.```")
    await qotli.edit("```Checking......```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=1557162396))
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                response2 = await response
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply("```Please unblock @tgscanrobot and try again```")
            if response.text.startswith("Hi!"):
                await qotli.edit("```Can you kindly disable your forward privacy settings for good?```")
            else:
                await qotli.delete()
                await bot.send_messages(qotli.chat_id, response.message, response2.message)
                await bot.send_read_acknowledge(qotli.chat_id)
                """ - cleanup chat after completed - """
                await qotli.client.delete_messages(conv.chat_id,
                                                   [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()
