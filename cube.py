import pycuber as pc
from collections import deque
import random
import time

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

    solution, time_for_resolve, max_queue_size, nodes, avg_branching = bfs_solver(scrambled_cube)
    if solution:
        print(f'Solução encontrada em {len(solution)} passos: {solution}')
        print(f'Tempo gasto: {time_for_resolve:.4f} segundos')
        print(f'Tamanho máximo da fila: {max_queue_size}')
        print(f'Quantidade de nós expandidos: {nodes}')
        print(f'Fator de ramificação média: {avg_branching}')
    else:
        print('Solução não encontrada.')
