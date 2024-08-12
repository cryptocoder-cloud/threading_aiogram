# -*- coding: utf8 -*-
"""
Автор: cryptocoding
Дата создания: 12.08.2024
Описание: Данный модуль создан для примера выполнения асинхронного мультипотока без блокирования асинхрона.
"""
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = 'TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

thread_pool = ThreadPoolExecutor(max_workers=10)


def heavy_task(data):
    time.sleep(5)  # Имитация тяжелой задачи
    return f"Task completed with data: {data}"


async def run_heavy_task(data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(thread_pool, heavy_task, data)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Starting heavy task...")

    result = await run_heavy_task("some data")
    return await message.reply(result)


@dp.message_handler(commands=['hello'])
async def hello(message: types.Message):
    return await message.reply("Hello")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
