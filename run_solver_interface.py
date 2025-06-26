import matplotlib.pyplot as plt
import threading
import time
from src.cube_interactive import Cube, InteractiveCube

from src.solvers import a_star_solver,generate_scrambled_cube

scrambled_cube, scramble_seq = generate_scrambled_cube(5)
print("Scramble:", scramble_seq)

cubo_visual = Cube(N=3)
for move in scramble_seq:
    face = move[0]
    direction = -1 if "'" in move else 1
    cubo_visual.rotate_face(face, direction)

def rodar_solver_em_thread(ax):
    time.sleep(1)

    (caminho, _, _, _), duration = a_star_solver(scrambled_cube)
    print(caminho)
    
    for move in caminho:
        print(f"Aplicando: {move}")
        face = move[0]
        direction = -1 if "'" in move else 1
        ax.rotate_face(face, direction)
        time.sleep(0.4)

fig = plt.figure()
ax = InteractiveCube(cubo_visual)
fig.add_axes(ax)

threading.Thread(target=rodar_solver_em_thread, args=(ax,)).start()

plt.show()
