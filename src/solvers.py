import pycuber as pc
from collections import deque
import random
import heapq
import itertools
from src.utils import Result, State, is_opposite_move, timed

MOVES = ['U', "U'", 'D', "D'", 'R', "R'", 'L', "L'", 'F', "F'", 'B', "B'"]

def simplify_pair(a, b):
    if a[0] != b[0]:
        return [a, b]

    if a == b + "'" or b == a + "'":
        return []
    if a == b:
        return [a, a]
    return [a, b]

def generate_scrambled_cube(n_moves):
    scramble = []
    while len(scramble) < n_moves:
        move = random.choice(MOVES)
        if not scramble:
            scramble.append(move)
            continue

        last = scramble.pop()
        simplified = simplify_pair(last, move)
        scramble.extend(simplified)
    cube = pc.Cube()
    cube.perform_algo(' '.join(scramble))
    return cube, scramble

@timed
def bfs_solver(scrambled_cube:pc.Cube) -> Result:
    """Algoritmo de busca em profundidade"""
    visited = set()
    queue = deque()
    queue.append((scrambled_cube.copy(), []))
    max_queue_size = 1
    nodes = 0
    total_branches = 0
    branching_points = 0

    while queue:
        current_cube, path = queue.popleft()
        state_str = str(current_cube)
        max_queue_size = max(max_queue_size, len(queue))

        if state_str in visited:
            continue
        visited.add(state_str)
        nodes += 1

        if current_cube == pc.Cube():
            avg_branching = total_branches / branching_points if branching_points else 0
            return Result(solution=path,memoria=max_queue_size,nos=nodes,avg_branching=avg_branching)


        children = 0
        for move in MOVES:
            new_cube = current_cube.copy()
            new_cube.perform_algo(move)
            queue.append((new_cube, path + [move]))
            children += 1

        total_branches += children
        branching_points += 1

    return Result(solution=None,memoria=max_queue_size,nos=nodes,avg_branching=-1)

@timed
def ids_solver(scrambled_cube:pc.Cube, max_depth=10) -> Result:
    nodes = 0
    max_stack_size = 1
    total_branches = 0
    branching_points = 0

    def dls(cube, path, depth, visited):
        nonlocal nodes, max_stack_size, total_branches, branching_points

        state_str = str(cube)
        if state_str in visited:
            return None

        visited.add(state_str)
        nodes += 1

        if cube == pc.Cube():
            return path

        if depth == 0:
            return None

        children = 0
        for move in MOVES:
            new_cube = cube.copy()
            new_cube.perform_algo(move)
            result = dls(new_cube, path + [move], depth - 1, visited.copy())
            children += 1
            if result is not None:
                return result

        total_branches += children
        branching_points += 1
        return None

    for depth in range(max_depth + 1):
        visited = set()
        result = dls(scrambled_cube.copy(), [], depth, visited)
        if result is not None:
            avg_branching = total_branches / branching_points if branching_points else 0
            return Result(solution=result,memoria=max_stack_size,nos=nodes,avg_branching=avg_branching)

    return Result(solution=None,memoria=max_stack_size,nos=nodes,avg_branching=-1)


def heuristic(cube:pc.Cube)->int:
    """Heurística que contabiliza quantos peças estão na posição errada."""
    goal = pc.Cube()
    count = 0
    for face in 'ULFRBD':
        current_face = cube.get_face(face)
        goal_face = goal.get_face(face)
        for i in range(3):
            for j in range(3):
                if current_face[i][j] != goal_face[i][j]:
                    count += 1
    return count

@timed
def a_star_solver(scrambled_cube:pc.Cube)-> Result:
    heap = []
    nodes = total_branches = branching_points = 0
    
    state = State(
        heuristic_pontos=heuristic(scrambled_cube),
        cube=scrambled_cube.copy(),
        path=[]
    )
    heapq.heappush(heap,state)

    while heap:
        state:State = heapq.heappop(heap)

        nodes += 1

        if state.cube == pc.Cube():
            avg_branching = total_branches / branching_points if branching_points else 0
            return Result(solution=state.path,memoria=len(heap),nos=nodes,avg_branching=avg_branching)
            
        branches = 0
        last_move = state.path[-1] if state.path else ""
        for move in MOVES:
            if is_opposite_move(move,last_move):
                continue
            new_cube = state.cube.copy()
            new_cube.perform_algo(move)
            new_path = state.path + [move]

            heapq.heappush(heap,State(
                heuristic_pontos=heuristic(new_cube),
                cube=new_cube,
                path=new_path
            ))
            branches += 1

        total_branches += branches
        branching_points += 1
        print(f"state: {state.path},State: {state}")
    return Result(solution=None,memoria=len(heap),nos=nodes,avg_branching=-1)
