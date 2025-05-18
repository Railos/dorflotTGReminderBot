import asyncio
from datetime import datetime, time
from telegram import Bot
from telegram.error import TelegramError
import pytz
from config import TOKEN, CHAT_ID

# Напоминание в 18:00 по Москве
REMINDER_TIME = time(18, 0)
REMINDER_MESSAGE = '''В конце дня обязательно должны быть закончены все диалоги, 
все доставки и Возвраты  должны быть переданы в чат,

проверьте все свои сделки закрыты ли в ЦРМ Разбираторе и внесены в чат кассы  

@Kupper_A @dkenswere @maksbenz @Andreyjojo'''
TIMEZONE = pytz.timezone('Europe/Moscow')

async def send_reminder(bot: Bot, chat_id: str | int, message: str):
    """Улучшенная функция отправки сообщения с обработкой ошибок"""
    try:
        print(f"Попытка отправить сообщение в чат {chat_id}...")
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown'  # Опционально, если нужно форматирование
        )
        print(f"✅ Сообщение успешно отправлено в {datetime.now(TIMEZONE).strftime('%H:%M')}")
    except TelegramError as e:
        print(f"❌ Ошибка при отправке в чат {chat_id}: {e}")
        if "chat not found" in str(e):
            print("⚠️ Возможные причины:")
            print("- Бот не добавлен в этот чат")
            print("- Указан неверный CHAT_ID")
            print("- Чат был удален")
        elif "Forbidden" in str(e):
            print("⚠️ Бот был заблокирован пользователем")

async def check_reminders(bot: Bot):
    """Проверка времени с улучшенным логированием"""
    now = datetime.now(TIMEZONE)
    current_time = now.time()
    
    print(f"Текущее время: {current_time.strftime('%H:%M')} (МСК)", end='\r')
    
    if (current_time.hour == REMINDER_TIME.hour and 
        current_time.minute == REMINDER_TIME.minute):
        print("\n" + "="*50)
        print(f"⏰ Время напоминания! {REMINDER_TIME.strftime('%H:%M')}")
        await send_reminder(bot, CHAT_ID, REMINDER_MESSAGE)
        print("="*50 + "\n")

async def main():
    """Основная функция с инициализацией"""
    print("🔔 Бот напоминаний запущен")
    print(f"Чат ID: {CHAT_ID}")
    print(f"Сообщение: '{REMINDER_MESSAGE}'")
    print(f"Время отправки: {REMINDER_TIME.strftime('%H:%M')} по МСК")
    print("="*50)
    
    try:
        bot = Bot(token=TOKEN)
        # Проверка доступности бота
        me = await bot.get_me()
        print(f"Бот @{me.username} готов к работе!")
        
        while True:
            await check_reminders(bot)
            await asyncio.sleep(60)
            
    except Exception as e:
        print(f"🚨 Критическая ошибка: {e}")
    finally:
        print("Бот завершает работу")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")