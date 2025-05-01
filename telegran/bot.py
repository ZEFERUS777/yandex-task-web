import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
import requests

# Настройка логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы для состояний ConversationHandler
(API_KEY, EMAIL, JOB_TITLE, TEAM_LEAD_ID,
 WORK_SIZE, COLLABORATORS, FINISH, JOB_ID) = range(8)
BASE_API_URL = "http://127.0.0.1:5000"

# ================== ОБРАБОТЧИКИ КОМАНД ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Привет! Я бот для управления работами проекта Liridius.\n\n"
        "📝 Доступные команды:\n"
        "/create_api_key - Создать API-ключ\n"
        "/add_job - Добавить работу\n"
        "/delete_job - Удалить работу\n"
        "/get_jobs - Список всех работ\n"
        "/get_job <id> - Информация о работе\n"
        "/profile - Мой профиль\n"
        "/help - Помощь"
    )

# ================== ЛИЧНЫЙ КАБИНЕТ ==================

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data
    stats = {
        'email': user_data.get('email', 'не указан'),
        'api_key': user_data.get('api_key', 'не указан'),
        'jobs_added': user_data.get('jobs_count', 0),
        'jobs_deleted': user_data.get('deleted_count', 0)
    }
    
    message = (
        "👤 *Ваш профиль*\n"
        f"📧 Email: `{stats['email']}`\n"
        f"🔑 API-ключ: `{stats['api_key']}`\n"
        f"✅ Добавлено работ: {stats['jobs_added']}\n"
        f"❌ Удалено работ: {stats['jobs_deleted']}"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# ================== СОЗДАНИЕ API КЛЮЧА ==================

async def create_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("📧 Введите ваш email:")
    return EMAIL

async def process_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    try:
        response = requests.post(
            f"{BASE_API_URL}/api/api_key/reg_api",
            params={"email": email}
        )

        if response.status_code == 200:
            api_key = response.json().get("apikey")
            context.user_data.update({
                'email': email,
                'api_key': api_key
            })
            await update.message.reply_text(f"🔑 Ваш API ключ: {api_key}")
        else:
            error = response.json().get("error", "Неизвестная ошибка")
            await update.message.reply_text(f"❌ Ошибка: {error}")

    except Exception as e:
        await update.message.reply_text(f"🚫 Ошибка соединения: {str(e)}")

    return ConversationHandler.END

# ================== ДОБАВЛЕНИЕ РАБОТЫ ==================

async def add_job_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🔑 Введите ваш API ключ:")
    return API_KEY

async def process_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["api_key"] = update.message.text
    await update.message.reply_text("📧 Введите ваш email:")
    return EMAIL

async def process_email_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["email"] = update.message.text
    await update.message.reply_text("🏷 Введите название работы:")
    return JOB_TITLE

async def process_job_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["job_title"] = update.message.text
    await update.message.reply_text("👤 Введите ID руководителя (число):")
    return TEAM_LEAD_ID

async def process_team_lead_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        team_lead_id = int(update.message.text)
        context.user_data["team_lead_id"] = team_lead_id
        await update.message.reply_text("⏳ Введите объем работы (число):")
        return WORK_SIZE
    except ValueError:
        await update.message.reply_text("❌ Введите целое число!")
        return TEAM_LEAD_ID

async def process_work_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        work_size = int(update.message.text)
        context.user_data["work_size"] = work_size
        await update.message.reply_text("👥 Введите участников (через запятую):")
        return COLLABORATORS
    except ValueError:
        await update.message.reply_text("❌ Введите целое число!")
        return WORK_SIZE

async def process_collaborators(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["collaborators"] = update.message.text
    await update.message.reply_text("✅ Работа завершена? (да/нет):")
    return FINISH

async def process_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    finish = update.message.text.lower()
    if finish in ["да", "yes"]:
        context.user_data["finish"] = True
    elif finish in ["нет", "no"]:
        context.user_data["finish"] = False
    else:
        await update.message.reply_text('❌ Ответьте "да" или "нет"!')
        return FINISH

    params = {
        "apikey": context.user_data["api_key"],
        "email": context.user_data["email"],
        "job_title": context.user_data["job_title"],
        "team_lead_id": context.user_data["team_lead_id"],
        "work_size": context.user_data["work_size"],
        "collaborators": context.user_data["collaborators"],
        "finish": context.user_data["finish"]
    }

    try:
        response = requests.post(f"{BASE_API_URL}/api/jobs/add", params=params)
        if response.status_code == 200:
            context.user_data['jobs_count'] = context.user_data.get('jobs_count', 0) + 1
            await update.message.reply_text("✅ Работа добавлена!")
        else:
            error = response.json().get("error", "Неизвестная ошибка")
            await update.message.reply_text(f"❌ Ошибка: {error}")
    except Exception as e:
        await update.message.reply_text(f"🚫 Ошибка соединения: {str(e)}")

    return ConversationHandler.END

# ================== УДАЛЕНИЕ РАБОТЫ ==================

async def delete_job_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🔑 Введите API ключ:")
    return API_KEY

async def process_api_key_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["api_key"] = update.message.text
    await update.message.reply_text("📧 Введите email:")
    return EMAIL

async def process_email_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["email"] = update.message.text
    await update.message.reply_text("🆔 Введите ID работы для удаления:")
    return JOB_ID

async def process_job_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        job_id = int(update.message.text)
        params = {
            "apikey": context.user_data["api_key"],
            "email": context.user_data["email"],
            "job_id": job_id
        }
        response = requests.delete(
            f"{BASE_API_URL}/api/jobs/delete", params=params)

        if response.status_code == 200:
            context.user_data['deleted_count'] = context.user_data.get('deleted_count', 0) + 1
            await update.message.reply_text("✅ Работа удалена!")
        else:
            error = response.json().get("error", "Неизвестная ошибка")
            await update.message.reply_text(f"❌ Ошибка: {error}")

    except ValueError:
        await update.message.reply_text("❌ Введите число!")
        return JOB_ID
    except Exception as e:
        await update.message.reply_text(f"🚫 Ошибка: {str(e)}")

    return ConversationHandler.END

# ================== ПОЛУЧЕНИЕ ДАННЫХ ==================

async def get_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(f"{BASE_API_URL}/api/jobs/")
        if response.status_code == 200:
            jobs = response.json()
            if jobs:
                message = "\n".join(
                    [f"ID: {job['id']}, 🏷 {job['Job_Title']}" for job in jobs]
                )
            else:
                message = "📭 Список работ пуст"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("❌ Ошибка при получении данных")
    except Exception as e:
        await update.message.reply_text(f"🚫 Ошибка соединения: {str(e)}")

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        job_id = int(context.args[0])
        response = requests.get(f"{BASE_API_URL}/api/jobs/{job_id}")

        if response.status_code == 200:
            job = response.json()
            message = (
                f"🆔 ID: {job['id']}\n"
                f"🏷 Название: {job['Job_Title']}\n"
                f"👤 Руководитель: {job['Team_lead_id']}\n"
                f"⏳ Объем: {job['Work_Size']} часов\n"
                f"👥 Участники: {job['Collaborators']}\n"
                f"✅ Статус: {'Завершена' if job['finish'] else 'В процессе'}"
            )
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("❌ Работа не найдена")

    except (IndexError, ValueError):
        await update.message.reply_text("ℹ️ Использование: /get_job <ID>")
    except Exception as e:
        await update.message.reply_text(f"🚫 Ошибка: {str(e)}")

# ================== ЗАПУСК ПРИЛОЖЕНИЯ ==================

def main() -> None:
    application = ApplicationBuilder().token("7956890852:AAE6RzlXvyvr4RGB0IVUL2kZzSO9gavalo4").build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_jobs", get_jobs))
    application.add_handler(CommandHandler("get_job", get_job))
    application.add_handler(CommandHandler("profile", show_profile))
    application.add_handler(CommandHandler("help", start))

    # Регистрация ConversationHandler
    conv_handlers = [
        ConversationHandler(
            entry_points=[CommandHandler("create_api_key", create_api_key)],
            states={EMAIL: [MessageHandler(filters.TEXT, process_email)]},
            fallbacks=[]
        ),
        ConversationHandler(
            entry_points=[CommandHandler("add_job", add_job_start)],
            states={
                API_KEY: [MessageHandler(filters.TEXT, process_api_key)],
                EMAIL: [MessageHandler(filters.TEXT, process_email_add)],
                JOB_TITLE: [MessageHandler(filters.TEXT, process_job_title)],
                TEAM_LEAD_ID: [MessageHandler(filters.TEXT, process_team_lead_id)],
                WORK_SIZE: [MessageHandler(filters.TEXT, process_work_size)],
                COLLABORATORS: [MessageHandler(filters.TEXT, process_collaborators)],
                FINISH: [MessageHandler(filters.TEXT, process_finish)]
            },
            fallbacks=[]
        ),
        ConversationHandler(
            entry_points=[CommandHandler("delete_job", delete_job_start)],
            states={
                API_KEY: [MessageHandler(filters.TEXT, process_api_key_delete)],
                EMAIL: [MessageHandler(filters.TEXT, process_email_delete)],
                JOB_ID: [MessageHandler(filters.TEXT, process_job_id)]
            },
            fallbacks=[]
        )
    ]

    for handler in conv_handlers:
        application.add_handler(handler)

    application.run_polling()

if __name__ == "__main__":
    main()