from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import io
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern=r"^\.ustat")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        return
    await event.edit("Balas di Pesan Goblok!!")
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        return
    await event.edit("Balas di Pesan Goblok!!")
    chat = "@tgscanrobot"
    await event.edit("Checking....")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=1557162396))
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("unblock me @tgscanrobot to work")
            return
        if response.text.startswith("I understand only stickers"):
            await event.edit("Sorry i cant't convert it check wheter is non animated sticker or not")
        else:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=1557162396))
            response = await response
            if response.text.startswith("Information"):
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=1557162396))
                response = await response
                await event.delete()
                await event.client.send_message(event.chat_id, response.message, reply_to=reply_message.id)
                await event.client.delete_message(event.chat_id, [msg.id, response.id])
            else:
                await event.edit("try again")
        await bot.send_read_acknowledge(conv.chat_id)
