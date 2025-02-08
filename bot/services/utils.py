from datetime import date, datetime

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
