use io;

/* Read instance data */
function input() {
    local usage = "Usage: localsolver maxcut.lsp "
            + "inFileName=inputFile [solFileName=outputFile] [lsTimeLimit=timeLimit]";

    if (inFileName == nil) throw usage;

    local inFile = io.openRead(inFileName);
    n = inFile.readInt();
    m = inFile.readInt();

    for [e in 1..m] {
        origin[e] = inFile.readInt();
        dest[e] = inFile.readInt();
        w[e] = inFile.readInt();
    }
}

/* Declare the optimization model */
function model() {
    // Decision variables x[i]
    // True if vertex x[i] is on the right side of the cut
    // and false if it is on the left side of the cut
    x[i in 1..n] <- bool();

    // An edge is in the cut-set if it has an extremity in each class of the bipartition
    incut[e in 1..m] <- x[origin[e]] != x[dest[e]];

    // Size of the cut
    cutWeight <- sum[e in 1..m](w[e] * incut[e]);
    maximize cutWeight;
}

/* Parametrize the solver */
function param() {
    if (lsTimeLimit == nil) lsTimeLimit = 10;
}

/* Write the solution in a file with the following format: 
 *  - objective value
 *  - each line contains a vertex number and its subset (1 for S, 0 for V-S) */
function output() {
    if (solFileName == nil) return;
    println("Write solution into file '" + solFileName + "'");
    local solFile = io.openWrite(solFileName);
    solFile.println(cutWeight.value);
    for [i in 1..n]
        solFile.println(i, " ", x[i].value);
}
