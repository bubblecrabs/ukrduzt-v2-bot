import time

import aiohttp
from bs4 import BeautifulSoup

from bot.services.redis.cache import cache_response
from bot.utils.schedule import parse_subjects


@cache_response("faculties")
async def fetch_faculties() -> dict[str, str] | None:
    """Fetches a list of faculties from the schedule website with caching."""
    url = "http://rasp.kart.edu.ua/schedule"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                faculty_list = soup.select("#schedule-search-faculty option")
                return {
                    faculty["value"]: faculty.text
                    for faculty in faculty_list if faculty.get("value")
                }
        except Exception as e:
            raise RuntimeError(f"Failed to fetch faculties: {e}") from e


@cache_response("groups:{faculty}:{course}")
async def fetch_groups(faculty: str, course: str, year_id: int) -> dict[str, str] | None:
    """Fetches a list of groups for a specific faculty and course with caching."""
    url = "http://rasp.kart.edu.ua/schedule/jdata"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = f"year_id={year_id}&faculty_id={faculty}&course_id={course}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                response_json = await response.json()
                return {team["id"]: team["title"] for team in response_json.get("teams", [])}
        except Exception as e:
            raise RuntimeError(f"Failed to fetch groups: {e}") from e


@cache_response("schedules:{day}:{faculty}:{course}:{group}")
async def fetch_schedules(
        week: str, day: str, faculty: str, course: str, group: str, year_id: int, semester: int
) -> dict[str, str]:
    """Fetches the schedule for a specific week, day, faculty, course, and group with caching."""
    url = (
        f"http://rasp.kart.edu.ua/schedule/jsearch?year_id={year_id}&semester_id={semester}"
        f"&faculty_id={faculty}&course_id={course}&team_id={group}"
    )
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = f"_search=false&nd={round(time.time())}&rows=20&page=1&sidx=&sord=asc"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                response_json = await response.json()
                return parse_subjects(week, day, response_json)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch schedules: {e}") from e
