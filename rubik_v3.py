import pycuber as pc
from collections import deque
import random, time, heapq

MOVES = ['U', "U'", 'D', "D'", 'R', "R'", 'L', "L'", 'F', "F'", 'B', "B'"]

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
            time_for_resolve = end_time - start_time
            avg_branching = total_branches / branching_points if branching_points else 0
            return path, time_for_resolve, max_queue_size, nodes, avg_branching

        children = 0
        for move in MOVES:
            new_cube = current_cube.copy()
            new_cube.perform_algo(move)
            queue.append((new_cube, path + [move]))
            children += 1
        
        total_branches += children
        branching_points += 1


    avg_branching = total_branches / branching_points if branching_points else 0
    return None, None, max_queue_size, nodes, avg_branching

def ids_solver(scrambled_cube, max_depth=10):
    from copy import deepcopy
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
    """Retorna o número de stickers fora do lugar."""
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
    import itertools
    visited = set()
    heap = []
    counter = itertools.count()  # contador único para desempate
    start_time = time.time()
    nodes = 0
    max_heap_size = 1
    total_branches = 0
    branching_points = 0

    initial_h = heuristic(scrambled_cube)
    heapq.heappush(heap, (initial_h, next(counter), 0, scrambled_cube.copy(), []))  # (f, tie-breaker, g, cube, path)

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

def generate_scrambled_cube(n_moves):
    cube = pc.Cube()
    print(cube)
    scramble = random.choices(MOVES, k=n_moves)
    cube.perform_algo(' '.join(scramble))
    return cube, scramble


MAX_MOVES = 5
for n in range(1, MAX_MOVES + 1):
    print(f'\nEmbaralhando com {n} movimentos...')
    scrambled_cube, scramble_seq = generate_scrambled_cube(n)
    print(scrambled_cube)
    print(f'Movimentos usados no embaralhamento: {scramble_seq}')

    # --- BFS ---
    print('\n[BFS]')
    solution, time_for_resolve, max_queue_size, nodes, avg_branching = bfs_solver(scrambled_cube)
    if solution:
        print(f'Solução encontrada em {len(solution)} passos: {solution}')
        print(f'Tempo gasto: {time_for_resolve:.4f} segundos')
        print(f'Tamanho máximo da fila: {max_queue_size}')
        print(f'Quantidade de nós expandidos: {nodes}')
        print(f'Fator de ramificação média: {avg_branching}')
    else:
        print('Solução não encontrada.')

    # --- IDS ---
    print('\n[IDS]')
    solution, time_for_resolve, max_stack_size, nodes, avg_branching = ids_solver(scrambled_cube, max_depth=10)
    if solution:
        print(f'Solução encontrada em {len(solution)} passos: {solution}')
        print(f'Tempo gasto: {time_for_resolve:.4f} segundos')
        print(f'Tamanho máximo da pilha: {max_stack_size}')
        print(f'Quantidade de nós expandidos: {nodes}')
        print(f'Fator de ramificação média: {avg_branching}')
    else:
        print('Solução não encontrada.')

    # --- A* ---
    print('\n[A*]')
    solution, time_for_resolve, max_heap_size, nodes, avg_branching = a_star_solver(scrambled_cube)
    if solution:
        print(f'Solução encontrada em {len(solution)} passos: {solution}')
        print(f'Tempo gasto: {time_for_resolve:.4f} segundos')
        print(f'Tamanho máximo da fila (heap): {max_heap_size}')
        print(f'Quantidade de nós expandidos: {nodes}')
        print(f'Fator de ramificação média: {avg_branching}')
    else:
        print('Solução não encontrada.')

