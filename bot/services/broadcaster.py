import asyncio
import logging

from aiogram import Bot, types
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup

async def complex_message(
    bot: Bot,
    call: types.CallbackQuery | types.Message,
    text: str,
    reply_markup = None):
    '''
        Deleting message and send another message.
    '''
    if isinstance(call, types.CallbackQuery):
        chat_id = call.message.chat.id
        message_id=call.message.message_id
    elif isinstance(call, types.Message):
        chat_id=call.chat.id
        message_id=call.message_id
        
    await delete_message(
            bot=bot,
            chat_id=chat_id,
            message_id=message_id
    )
    await send_message(
        bot=bot,
        user_id=call.from_user.id,
        text=text,
        reply_markup=reply_markup
    )

async def delete_message(
    bot: Bot,
    chat_id: int | str,
    message_id: int,
    request_timeout: int | None = None
) -> bool:
    """
    Safe messages deleter

    :param bot: Bot instance.
    :param chat_id: chat id.
    :param message_id: message id.
    :param request_timeout: request timeout.
    :return: success.
    """
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
            request_timeout=request_timeout
        )
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [CHAT-ID:{chat_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
            request_timeout=request_timeout
        )
        # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [CHAT-ID:{chat_id}]: failed")
    else:
        logging.info(f"Target [CHAT-ID:{chat_id}]: message deleted.")
        return True
    return False


async def send_message(
    bot: Bot,
    user_id: int | str,
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    """
    Safe messages sender

    :param bot: Bot instance.
    :param user_id: user id. If str - must contain only digits.
    :param text: text of the message.
    :param disable_notification: disable notification or not.
    :param reply_markup: reply markup.
    :return: success.
    """
    try:
        await bot.send_message(
            user_id,
            text,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
    except exceptions.TelegramBadRequest:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            bot, user_id, text, disable_notification, reply_markup
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False

async def edit_message(call: types.CallbackQuery,
                       text: str | None = None,
                       reply_markup: InlineKeyboardMarkup | None = None):
    '''Safe inline message editor/markup changer
    
    :param bot: Bot instance.
    :param call: callbackquery. Telegram object.
    :param text: text of the message.
    :param reply_markup: reply markup.
    :return: success.
    '''
    try:
        if text and reply_markup:
            await call.message.edit_text(text=text, reply_markup=reply_markup)
            logging.info(f"Target [ID:{call.from_user.id}]: success change text and markup")
        elif text:
            await call.message.edit_text(text=text,
                                    chat_id=call.from_user.id,
                                    message_id=call.message.messsage_id,
                                    reply_markup = None)
            logging.info(f"Target [ID:{call.from_user.id}]: success change text")
        elif reply_markup:
            await call.message.edit_reply_markup(reply_markup=reply_markup)
            logging.info(f"Target [ID:{call.from_user.id}]: success change markup")
    except Exception as ex:
        logging.error(f"Target [ID:{call.from_user.id}]: got {ex}")
    else:
        return True
    return False



async def broadcast(
    bot: Bot,
    users: list[str | int],
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> int:
    """
    Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param text: Text of the message.
    :param disable_notification: Disable notification or not.
    :param reply_markup: Reply markup.
    :return: Count of messages.
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(
                bot, user_id, text, disable_notification, reply_markup
            ):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count