from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import io
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.itos$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("sir this is not a image message reply to image message")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("sir, This is not a image ")
        return
    chat = "@buildstickerbot"
    await event.edit("Membuat Sticker..")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=164977173))
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("unblock me (@buildstickerbot) and try again")
            return
        if response.text.startswith("Hi!"):
            await event.edit("Can you kindly disable your forward privacy settings for good?")
        else:
            await event.delete()
            await bot.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, response.message)
            await event.client.delete_message(event.chat_id, [msg.id, response.id])


@register(outgoing=True, pattern="^.get$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("Balas di Sticker Goblok!!")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("Balas di Sticker Tolol!!")
        return
    await event.edit("Convert to image..")
    msg = await event.client.forward_messages(reply_message)
    async with bot.conversation("@stickers_to_image_bot") as conv:
        try:
            r1 = await conv.get_response()
            r2 = await conv.get_response()
            r3 = await conv.get_response()
        except YouBlockedUserError:
            await event.reply("unblock me (@stickers_to_image_bot) to work")
            return
        if r1.text.startswith("I've got your sticker"):
            return
            await event.edit("Sorry i cant't convert it check wheter is non animated sticker or not")
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, r3, reply_to=reply_message.id)
            await event.client.delete_messages(
                    conv.chat_id, [msg.id, r1.id, r2.id, r3.id]
                )
        else:
            await event.edit("try again")
        await bot.send_read_acknowledge(conv.chat_id)


@register(outgoing=True, pattern="^.stoi$")
async def sticker_to_png(sticker):
    if not sticker.is_reply:
        await sticker.edit("`NULL information to feftch...`")
        return False

    img = await sticker.get_reply_message()
    if not img.document:
        await sticker.edit("Ini Bukan sticker Goblok!!!...`")
        return False

    await sticker.edit("`Stiker Berhasil Di Colong!`")
    image = io.BytesIO()
    await sticker.client.download_media(img, image)
    image.name = "sticker.png"
    image.seek(0)
    await sticker.client.send_file(
        sticker.chat_id, image, reply_to=img.id, force_document=True
    )
    await sticker.delete()
    return


CMD_HELP.update(
    {
        "stickers_v2": ">`.itos`"
        "\nUsage: Reply .itos to a sticker or an image to kang it to your userbot no pack "
        "\n\n>`.get`"
        "\nUsage: reply to a sticker to get 'PNG' file of sticker."
        "\n\n>`.stoi`"
        "\nUsage: reply to a sticker to get 'PNG' file of sticker."})
