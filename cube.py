import pycuber as pc
from collections import deque
import random

MOVES = ['U', "U'", 'D', "D'", 'R', "R'", 'L', "L'", 'F', "F'", 'B', "B'"]

def bfs_solver(scrambled_cube):
    visited = set()
    queue = deque()
    queue.append((scrambled_cube.copy(), []))  

    while queue:
        current_cube, path = queue.popleft()
        state_str = str(current_cube)

        if state_str in visited:
            continue
        visited.add(state_str)

        if current_cube == pc.Cube():
            return path

        for move in MOVES:
            new_cube = current_cube.copy()
            new_cube.perform_algo(move)
            queue.append((new_cube, path + [move]))

    return None

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

    solution = bfs_solver(scrambled_cube)
    if solution:
        print(f'Solução encontrada em {len(solution)} passos: {solution}')
    else:
        print('Solução não encontrada.')
