import time
import json
from typing import Any

import aiohttp
from bs4 import BeautifulSoup

from bot.core.loader import redis_cache
from bot.utils.schedule import parse_subjects


async def fetch_faculties() -> Any | None:
    """Fetches a list of faculties from the schedule website with caching."""
    cache_key = "faculties"
    cached_data = await redis_cache.get(cache_key)
    if cached_data:
        return cached_data

    url = "http://rasp.kart.edu.ua/schedule"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                faculty_list = soup.find(id="schedule-search-faculty").find_all("option")
                result = {
                    faculty.get("value"): faculty.text
                    for faculty in faculty_list if faculty.get("value")
                }
                await redis_cache.set(cache_key, result)
                return result
        except Exception as e:
            raise RuntimeError(f"Failed to fetch faculties: {e}") from e
        finally:
            await redis_cache.close()


async def fetch_groups(faculty: str, course: str, year_id: int) -> Any | None:
    """Fetches a list of groups for a specific faculty and course with caching."""
    cache_key = f"groups:{faculty}:{course}"
    cached_data = await redis_cache.get(cache_key)
    if cached_data:
        return cached_data

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
                result = {team["id"]: team["title"] for team in response_json.get("teams", [])}
                await redis_cache.set(cache_key, result)
                return result
        except Exception as e:
            raise RuntimeError(f"Failed to fetch groups: {e}") from e
        finally:
            await redis_cache.close()


async def fetch_schedules(
        week: str,
        day: str,
        faculty: str,
        course: str,
        group: str,
        year_id: int,
        semester: int
) -> Any | None:
    """Fetches the schedule for a specific week, day, faculty, course, and group with caching."""
    cache_key = f"schedules:{day}:{faculty}:{course}:{group}"
    cached_data = await redis_cache.get(cache_key)
    if cached_data:
        return cached_data

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
                response_text = await response.text()
                response_json = json.loads(response_text)
                result = parse_subjects(week, day, response_json)
                await redis_cache.set(cache_key, result)
                return result
        except Exception as e:
            raise RuntimeError(f"Failed to fetch schedules: {e}") from e
        finally:
            await redis_cache.close()
