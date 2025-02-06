import logging
import functools
from typing import Any, Callable

logger = logging.getLogger(__name__)


def middleware_logging(func: Callable) -> Callable:
    """Middleware decorator for logging function calls."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f'Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}')
        try:
            result = func(*args, **kwargs)
            logger.info(f'Function {func.__name__} returned: {result}')
            return result
        except Exception as e:
            logger.error(f'Function {func.__name__} raised an error: {e}', exc_info=True)
            raise

    return wrapper
