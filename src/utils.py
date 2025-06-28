import time
from functools import wraps
from typing import Callable, TypeVar, Tuple, NamedTuple,List
import itertools
import pycuber as pc

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
    
class State:
    counter = itertools.count()
    def __init__(self,heuristic_pontos:int, cube:pc.Cube, path:List[str]):
        self.heuristic_pontos = heuristic_pontos
        self.passos = len(path)
        self.cube = cube
        self.path = path
        self.identificador = next(State.counter)
    
    def function_otimization(self):
        return self.passos + self.heuristic_pontos
    
    
    def __lt__(self, other:'State'):
        return (self.function_otimization(), self.identificador) < (other.function_otimization(), other.identificador)
    
    def __str__(self):
        return (
            f"State(id={self.identificador}, "
            f"passos={self.passos}, heuristic_pontos={self.heuristic_pontos}, function={self.function_otimization()}, "
            f"path={self.path})"
        ) 
    def __repr__(self):
        return self.__str__()
    
def is_opposite_move(move1: str, move2: str) -> bool:
    if move1.endswith("'"):
        return move2 == move1[:-1]
    else:
        return move2 == move1 + "'"