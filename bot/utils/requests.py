import time
import json

import aiohttp
from bs4 import BeautifulSoup

from bot.config import config
from bot.utils.utils import check_week_and_day


async def get_faculties() -> dict[str, str]:
    """Fetches a list of faculties from the schedule website."""
    url = "http://rasp.kart.edu.ua/schedule"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                faculty_list = soup.find(id="schedule-search-faculty").find_all("option")
                return {
                    faculty.get("value"): faculty.text
                    for faculty in faculty_list if faculty.get("value")
                }
        except Exception as e:
            raise RuntimeError(f"Failed to fetch faculties: {e}") from e


async def get_groups(faculty: str, course: str) -> dict[str, str]:
    """Fetches a list of groups for a specific faculty and course."""
    url = "http://rasp.kart.edu.ua/schedule/jdata"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://rasp.kart.edu.ua",
        "Referer": "http://rasp.kart.edu.ua/schedule",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = f"year_id={config.year_id}&faculty_id={faculty}&course_id={course}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                response_json = await response.json()
                return {team["id"]: team["title"] for team in response_json.get("teams", [])}
        except Exception as e:
            raise RuntimeError(f"Failed to fetch groups: {e}") from e


async def get_schedules(week: str, day: str, faculty: str, course: str, group: str) -> tuple:
    """Fetches the schedule for a specific week, day, faculty, course, and group."""
    url = (
        f"http://rasp.kart.edu.ua/schedule/jsearch?year_id={config.year_id}&semester_id={config.semestr}"
        f"&faculty_id={faculty}&course_id={course}&team_id={group}"
    )
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://rasp.kart.edu.ua",
        "Referer": "http://rasp.kart.edu.ua/schedule",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = f"_search=false&nd={round(time.time())}&rows=20&page=1&sidx=&sord=asc"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                response_text = await response.text()
                response_json = json.loads(response_text)
                return check_week_and_day(week, day, response_json)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch schedules: {e}") from e
