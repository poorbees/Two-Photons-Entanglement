import localsolver
import sys

def read_integers(filename):
    with open(filename) as f:
        return [int(elem) for elem in f.read().split()]

#
# Read instance data
#
def read_instance(filename):
    file_it = iter(read_integers(filename))
    # Number of vertices
    n = next(file_it)
    # Number of edges
    m = next(file_it)

    # Origin of each edge
    origin = [None] * m
    # Destination of each edge
    dest = [None] * m
    # Weight of each edge
    w = [None] * m

    for e in range(m):
        origin[e] = next(file_it)
        dest[e] = next(file_it)
        w[e] = next(file_it)
    
    return n, m, origin, dest, w

def main(instance_file, output_file, time_limit):
    n, m, origin, dest, w = read_instance(instance_file)

    with localsolver.LocalSolver() as ls:
        #
        # Declare the optimization model
        #
        model = ls.model

        # Decision variables x[i]
        # True if vertex x[i] is on the right side of the cut
        # and false if it is on the left side of the cut
        x = [model.bool() for i in range(n)]

        # An edge is in the cut-set if it has an extremity in each class of the bipartition
        incut = [None] * m
        for e in range(m):
            incut[e] = model.neq(x[origin[e] - 1], x[dest[e] - 1])

        # Size of the cut
        cut_weight = model.sum(w[e] * incut[e] for e in range(m))
        model.maximize(cut_weight)

        model.close()

        # Parameterize the solver
        ls.param.time_limit = time_limit

        ls.solve()

        #
        # Write the solution in a file with the following format:
        #  - objective value
        #  - each line contains a vertex number and its subset (1 for S, 0 for V-S)
        #
        if output_file != None:
            with open(output_file, 'w') as f:
                f.write("%d\n" % cut_weight.value)
                # Note: in the instances the indices start at 1
                for i in range(n):
                    f.write("%d %d\n" % (i + 1, x[i].value))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python maxcut.py inputFile [outputFile] [timeLimit]")
        sys.exit(1)

    instance_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None
    time_limit = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
    main(instance_file, output_file, time_limit)