import time
from functools import wraps
from typing import Callable, TypeVar, Tuple, NamedTuple,List

R = TypeVar("R")  # Tipo de retorno da função original

def timed(func: Callable[..., R]) -> Callable[..., Tuple[R, float]]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[R, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, end - start
    return wrapper


class Result(NamedTuple):
    solution: List[str] | None
    memoria: int | None
    nos: int | None
    avg_branching: float