import pycuber as pc
from collections import deque
import random
import time
import heapq
import itertools

MOVES = ['U', "U'", 'D', "D'", 'R', "R'", 'L', "L'", 'F', "F'", 'B', "B'"]


def generate_scrambled_cube(n_moves):
    cube = pc.Cube()
    scramble = random.choices(MOVES, k=n_moves)
    cube.perform_algo(' '.join(scramble))
    return cube, scramble


def bfs_solver(scrambled_cube):
    visited = set()
    queue = deque()
    queue.append((scrambled_cube.copy(), []))
    start_time = time.time()
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
            end_time = time.time()
            avg_branching = total_branches / branching_points if branching_points else 0
            return path, end_time - start_time, max_queue_size, nodes, avg_branching

        children = 0
        for move in MOVES:
            new_cube = current_cube.copy()
            new_cube.perform_algo(move)
            queue.append((new_cube, path + [move]))
            children += 1

        total_branches += children
        branching_points += 1

    return None, None, max_queue_size, nodes, 0


def ids_solver(scrambled_cube, max_depth=10):
    start_time = time.time()
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
            time_for_resolve = time.time() - start_time
            avg_branching = total_branches / branching_points if branching_points else 0
            return result, time_for_resolve, max_stack_size, nodes, avg_branching

    return None, None, max_stack_size, nodes, 0


def heuristic(cube):
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


def a_star_solver(scrambled_cube):
    visited = set()
    heap = []
    counter = itertools.count()
    start_time = time.time()
    nodes = 0
    max_heap_size = 1
    total_branches = 0
    branching_points = 0

    initial_h = heuristic(scrambled_cube)
    heapq.heappush(heap, (initial_h, next(counter), 0, scrambled_cube.copy(), []))

    while heap:
        f, _, g, current_cube, path = heapq.heappop(heap)
        state_str = str(current_cube)
        max_heap_size = max(max_heap_size, len(heap))

        if state_str in visited:
            continue
        visited.add(state_str)
        nodes += 1

        if current_cube == pc.Cube():
            end_time = time.time()
            avg_branching = total_branches / branching_points if branching_points else 0
            return path, end_time - start_time, max_heap_size, nodes, avg_branching

        children = 0
        for move in MOVES:
            new_cube = current_cube.copy()
            new_cube.perform_algo(move)
            new_path = path + [move]
            h = heuristic(new_cube)
            heapq.heappush(heap, (g + 1 + h, next(counter), g + 1, new_cube, new_path))
            children += 1

        total_branches += children
        branching_points += 1

    return None, None, max_heap_size, nodes, 0
