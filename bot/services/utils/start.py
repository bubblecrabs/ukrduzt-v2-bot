from datetime import date


def get_current_week() -> str:
    """Get the current week type based on the ISO calendar."""
    today = date.today()
    week_number = today.isocalendar()[1]
    return "Парна" if week_number % 2 != 0 else "Непарна"


def generate_start_text() -> str:
    """Generates the welcome text with the current week."""
    week = get_current_week()
    return (
        f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень\n\n"
        f"📆 Поточна неділя - *{week}*"
    )
