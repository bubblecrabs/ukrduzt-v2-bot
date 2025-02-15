from datetime import datetime, date

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.requests.users import update_user, get_user_by_id

week_days = [
    {"name": "Понеділок", "id": "2"},
    {"name": "Вівторок", "id": "3"},
    {"name": "Середа", "id": "4"},
    {"name": "Четвер", "id": "5"},
    {"name": "П'ятниця", "id": "6"},
]


def get_current_week() -> str:
    """Get the current week type based on the ISO calendar."""
    today = date.today()
    week_number = today.isocalendar()[1]
    return "Парна" if week_number % 2 != 0 else "Непарна"


def is_weekend() -> bool:
    """Checks whether today is a Saturday or Sunday."""
    today = datetime.today().weekday()
    return today >= 5


async def get_user_group_data(
        call: CallbackQuery, state: FSMContext, session: AsyncSession
) -> tuple[str, str, str, str, str, str]:
    """Retrieves and processes user group data based on the callback query and FSM state."""
    if call.message.text == "Виберіть групу ⬇️":
        user_data = await state.get_data()

        group, group_name = call.data.split(",")
        faculty = user_data["faculty"].removeprefix("faculty_")
        course = user_data["course"].removeprefix("course_")
        selected_day, selected_day_id = user_data["day"].split("_")

        await update_user(
            session=session,
            faculty=int(faculty),
            course=int(course),
            group=int(group),
            group_name=group_name,
            user_id=call.from_user.id,
        )
    else:
        user = await get_user_by_id(session=session, user_id=call.from_user.id)
        faculty = user.user_faculty
        course = user.user_course
        group = user.user_group
        group_name = user.user_group_name
        selected_day, selected_day_id = call.data.split("|")

    return faculty, course, group, group_name, selected_day, selected_day_id


def format_schedule_text(subjects: dict[int, str], week: str, selected_day: str, group_name: str) -> str:
    """Formats the schedule text based on the provided data."""
    week_str = "наступний" if is_weekend() else "цей"
    subjects_text = "\n".join(f"{sid}: *{sname}*" for sid, sname in subjects.items())

    template = (
        f"🔔 Показано розклад на *{week_str}* тиждень.\n\n"
        f"{subjects_text}\n\n" if subjects_text
        else "🔍 На *цей* день ваш розклад вільний.\n\n"
    )
    return template + (
        f"⏰ Вибраний день - *{selected_day}*\n"
        f"📆 Поточна неділя - *{week}*\n"
        f"💼 Вибрана група - *{group_name}*"
    )


def replace_numbers(text: str) -> str:
    """Replace numbers in the text with corresponding emoji numbers."""
    replacements = {
        '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣',
        '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '10': '🔟'
    }
    words = text.split()
    replaced_words = [
        replacements.get(word, "".join(replacements.get(c, c) for c in word))
        for word in words
    ]
    return " ".join(replaced_words)


def parse_subjects(week: str, day: str, json_data: dict) -> dict[str, str]:
    """Check the schedule for the specified week and day."""
    result: dict[str, str] = {}
    change = is_weekend()
    sid = 1

    for subject in json_data.get("rows", []):
        row = subject["cell"]
        cur_week_pair = row[1]
        new_week_pair = "парн." if change and cur_week_pair == "непарн." else "непарн." if change else cur_week_pair

        if (week == "Парна" and new_week_pair != "непарн.") or (week == "Непарна" and new_week_pair == "непарн."):
            name_subject = row[int(day)]
            if name_subject:
                result[replace_numbers(str(sid))] = name_subject
            sid += 1

    return result
