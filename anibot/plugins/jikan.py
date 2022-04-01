# uses jikanpy (Jikan API)
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from .. import BOT_NAME, TRIGGERS as trg, anibot
from ..utils.data_parser import get_scheduled
from ..utils.helper import control_user, get_btns, check_user
from ..utils.db import get_collection

DC = get_collection('DISABLED_CMDS')


@anibot.on_message(filters.command(["schedule", f"schedule{BOT_NAME}"], prefixes=trg))
@control_user
async def get_schuled(client: anibot, message: Message, mdata: dict):
    """Get List of Scheduled Anime"""
    gid = mdata['chat']['id']
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'schedule' in find_gc['cmd_list'].split():
        return
    x = await client.send_message(gid, "<code>Fetching Scheduled Animes</code>")
    user = mdata['from_user']['id']
    msg = await get_scheduled()
    buttons = get_btns("SCHEDULED", result=[msg[1]], user=user)
    await x.edit_text(msg[0], reply_markup=buttons)


@anibot.on_callback_query(filters.regex(pattern=r"sched_(.*)"))
@check_user
async def ns_(client: anibot, cq: CallbackQuery, cdata: dict):
    kek, day, user = cdata['data'].split("_")
    msg = await get_scheduled(int(day))
    buttons = get_btns("SCHEDULED", result=[int(day)], user=user)
    await cq.edit_message_text(msg[0], reply_markup=buttons)