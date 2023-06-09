#pip install aiogram
#pip install revChatGPT
import aiogram
from revChatGPT.V3 import Chatbot
from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, API_KEY

chatbot = Chatbot(API_KEY, system_prompt="You are ChatGPT, a large language model trained by OpenAI. Respond conversationally and then be sure to write everything in Russian. Imagine that you are an seo copywriter, also mandatory that the text should be at least 3000 characters long")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text="Привет! Напиши вопрос или задачу")


@dp.message_handler(commands=['continue'])
async def continue_generation(message: types.Message):
    await message.delete()
    try:
        answer = chatbot.ask("Продолжи данный текст еще на 1000-1500 символов")
        await message.answer(text=answer)
        await message.answer(text="Генерация окончена")
    except:
        await message.answer(text="Генерация окончена")
    chatbot.reset()


@dp.message_handler(commands=['new'])
async def reset_conv(message: types.Message):
    chatbot.reset()
    await message.answer(text="Начат новый диалог")


@dp.message_handler()
async def chat_text(message: types.Message):
    await message.answer(text=chatbot.ask(message.text))
    try:
        ans = chatbot.ask("Можешь ли ты продолжить данный текст ответь одним словом, да или нет?")
        if ans:
            await message.answer(text="Вы можете продолжить данный текст - /continue")
    except:
        await message.answer(text="Генерация окончена")
        chatbot.reset()


if __name__ == "__main__":
    executor.start_polling(dp)
