import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand
from aiogram.exceptions import TelegramAPIError

TOKEN = "8151584208:AAHJTAQ2wKqzwTGYJC23KrNDTtqhl4giWFI"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    try:
        user = message.from_user
        logger.info(f"User {user.id} started the bot")
        await message.reply("Привет! Я бот АндреевАА. Мои команды: /help")
    except TelegramAPIError as e:
        logger.error(f"Error in /start: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")

@dp.message(Command("help"))
async def help_command(message: types.Message):
    try:
        await message.reply(
            "/start – Приветствие\n"
            "/help – Все команды\n"
            "/square [число] – Квадрат числа\n"
            "/count [текст] – Подсчёт символов и слов\n"
            "Можно также просто отправить число"
        )
    except TelegramAPIError as e:
        logger.error(f"Error in /help: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")

@dp.message(Command("square"))
async def square(message: types.Message):
    try:
        args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        if not args:
            await message.reply("Нужно ввести число, например: /square 5")
            return
        num = float(args)
        await message.reply(f"{num} в квадрате = {num ** 2}")
    except (ValueError, IndexError):
        await message.reply("Нужно ввести число, например: /square 5")
    except TelegramAPIError as e:
        logger.error(f"Error in /square: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")

@dp.message(Command("count"))
async def count_text(message: types.Message):
    try:
        args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        if not args:
            await message.reply("Нужно ввести текст, например: /count Привет как дела")
            return
        if len(args) > 1000:
            await message.reply("Текст слишком длинный!")
            return
        char_count = len(args.replace(" ", ""))
        word_count = len(args.split())
        await message.reply(f"Символов (без пробелов): {char_count}\nСлов: {word_count}")
    except TelegramAPIError as e:
        logger.error(f"Error in /count: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")

@dp.message()
async def handle_message(message: types.Message):
    try:
        if message.text.startswith('/'):
            return
        num = float(message.text)
        await message.reply(f"{num} в квадрате = {num ** 2}")
    except ValueError:
        await message.reply("Отправьте число, чтобы узнать его квадрат")
    except TelegramAPIError as e:
        logger.error(f"Error in handle_message: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Приветствие"),
        BotCommand(command="help", description="Все команды"),
        BotCommand(command="square", description="Квадрат числа"),
        BotCommand(command="count", description="Подсчёт символов и слов")
    ]
    try:
        await bot.set_my_commands(commands)
    except TelegramAPIError as e:
        logger.error(f"Error setting commands: {e}")

async def main():
    try:
        await set_bot_commands(bot)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Shutting down bot...")
        await bot.session.close()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
