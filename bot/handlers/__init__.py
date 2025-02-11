from aiogram import Router

from .admin import panel, stats, export_users, mailing
from .schedule import day, faculty, course, group, schedule
from .start import start


def get_routers() -> list[Router]:
    """Return a list of all routers used in the bot."""
    admin_routers = [
        start_admin.router,
        stats.router,
        export_users.router,
        mailing.router,
    ]
    schedule_routers = [
        day.router,
        faculty.router,
        course.router,
        group.router,
        schedule.router,
    ]
    start_routers = [
        start.router,
    ]
    return admin_routers + schedule_routers + start_routers
