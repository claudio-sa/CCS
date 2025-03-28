"""Simple travelling salesman problem between cities."""
from __future__ import print_function
from ortools.sat.python import cp_model


'''
#$ python tsp_from_OR-TOOLS.py 7_matrix.txt
$ python tsp_from_OR-TOOLS.py 38_matrix.txt
...................................
Route/sequence/cycle (0..N-1): 0 -> 9 -> 13 -> 20 -> 28 -> 29 -> 31 -> 34 -> 36 -> 37 -> 32 -> 33 -> 35 -> 30 -> 26 -> 27 -> 23 -> 21 -> 24 -> 25 -> 22 -> 19 -> 14 -> 12 -> 15 -> 16 -> 17 -> 18 -> 10 -> 11 -> 8 -> 7 -> 6 -> 5 -> 4 -> 2 -> 3 -> 1 -> 0
Travelled distance: 6656
'''


import sys
INP_FILE = sys.argv[1]   #### formatted ...

def get_matrix():
    matrix = []
    with open(INP_FILE, 'r') as file:
        for line in file.readlines():
            matrix.append( [ int(x) for x in line.split()] )
        #print("\n read it: ", matrix)

    file.close()   
    return(matrix)


###############################################
def main():
    """Entry point of the program."""

    DISTANCE_MATRIX = get_matrix()
    print("\n Matrix: ", *DISTANCE_MATRIX)
    num_nodes = len(DISTANCE_MATRIX)
    all_nodes = range(num_nodes)
    print('Num nodes =', num_nodes)

    # Model.
    model = cp_model.CpModel()

    obj_vars = []
    obj_coeffs = []

    # Create the circuit constraint.
    arcs = []
    arc_literals = {}
    for i in all_nodes:
        for j in all_nodes:
            if i == j:
                continue

            lit = model.NewBoolVar('%i follows %i' % (j, i))
            arcs.append([i, j, lit])
            arc_literals[i, j] = lit

            obj_vars.append(lit)
            obj_coeffs.append(DISTANCE_MATRIX[i][j])

    model.AddCircuit(arcs)

    # Minimize weighted sum of arcs. Because this s
    model.Minimize(
        sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    # To benefit from the linearization of the circuit constraint.
    solver.parameters.linearization_level = 2

    solver.Solve(model)
    print(solver.ResponseStats())

    current_node = 0
    str_route = '%i' % current_node
    route_is_finished = False
    route_distance = 0
    while not route_is_finished:
        for i in all_nodes:
            if i == current_node:
                continue
            if solver.BooleanValue(arc_literals[current_node, i]):
                str_route += ' -> %i' % i
                route_distance += DISTANCE_MATRIX[current_node][i]
                current_node = i
                if current_node == 0:
                    route_is_finished = True
                break

    print('Route/sequence/cycle (0..N-1):', str_route)
    print('Travelled distance:', route_distance)


if __name__ == '__main__':
    main()
