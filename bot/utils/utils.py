from datetime import date, datetime

week_days_h: list[str] = ["Понеділок|2", "Вівторок|3", "Середа|4", "Четвер|5", "П'ятниця|6"]
week_days_first: list[str] = ["Понеділок_2", "Вівторок_3", "Середа_4", "Четвер_5", "П'ятниця_6"]


def get_current_week() -> str:
    """Get the current week type based on the ISO calendar."""
    today = date.today()
    week_number = today.isocalendar()[1]
    return "Парна" if week_number % 2 != 0 else "Непарна"


def replace_numbers(text: str) -> str:
    """Replace numbers in the text with corresponding emoji numbers."""
    replacements = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣'}
    return ''.join(replacements.get(c, c) for c in text)


def check_week_and_day(week: str, day: str, res_text: dict) -> tuple[dict[str, str], bool]:
    """Check the schedule for the specified week and day."""
    name_subjects: dict[str, str] = {}
    day_name = datetime.now().strftime('%A')  # Get current day in full format (e.g., "Monday")
    change = day_name in ("Saturday", "Sunday")

    for name_id, subject in enumerate(res_text.get("rows", []), start=1):
        row = subject["cell"]
        cur_week_pair = row[1]
        new_week_pair = "парн." if change and cur_week_pair == "непарн." else "непарн." if change else cur_week_pair

        if (week == "Парна" and new_week_pair != "непарн.") or (week == "Непарна" and new_week_pair == "непарн."):
            name_subject = row[int(day)]
            if name_subject:
                name_subjects[replace_numbers(str(name_id))] = name_subject

    return name_subjects, change
