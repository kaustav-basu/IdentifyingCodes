__author__ = "Kaustav Basu"

'''
Please read the papers under Research, to better grasp the concept of Identifying Codes.
This program computes the Minimum Identifying Code Set for a given graph. 
I utilize the Gurobi Optimization package to obtain the optimal solution.
'''


# Packages required in this program
import networkx as nx
from pulp import *
import time
from itertools import combinations
import numpy as np
import pandas as pd

# To read edge-lists stored as txt files
def readGraphEdgelist():
    G = nx.Graph()
    G = nx.read_edgelist("Edge-Lists/ParisAdj.txt", nodetype = int, create_using = nx.Graph())
    return nx.to_numpy_matrix(G, nodelist = sorted(list(G.nodes())))

# To read Adjacency matrix stored as csv files
def readGraphCSV():
    df = pd.read_csv("UndirectedGraphs/MONTREALGANG_UN.csv")
    #print(df)
    df = df.drop(df.columns[[0]], axis = 1)
    return df.values

# This function removes twins by forming super nodes (removing duplicates)
def twinRemoval(filetype):
    # Filetype is a user input to allow the program to select the appropriate file

    if filetype == 'csv':
        M = readGraphCSV()
    elif filetype == 'txt':
        M = readGraphEdgelist() 
    m, _ = M.shape
    print("Original Shape: ", M.shape)

    # Diagonal elements set to 1 to capture the closed neighborhood concept
    for i in range(len(M)):
        M[i, i] = 1

    df = pd.DataFrame(M)
    print(df.values.shape)

    # Utilizing Pandas to remove duplicate rows (and columns, since it's an adjacency matrix)
    dupRemoved = pd.DataFrame.drop_duplicates(df)
    _, idx = np.unique(dupRemoved, axis = 1, return_index = True)
    dupRemoved = dupRemoved.iloc[:, idx]
    dupRemoved.sort_index(axis = 1, inplace = True)
    print("New Shape: ", dupRemoved.shape)

    # Creating the graph from the new matrix with duplicates removed
    G = nx.from_numpy_matrix(dupRemoved.values)
    return G

# This function computes the optimal MICS for the input graph
def model(filetype):
    start = time.time()
    G = twinRemoval(filetype)

    # Relabeling nodes of the graph as consecutive integers starting from 1 instead of 0 (for ease of understanding)
    G = nx.convert_node_labels_to_integers(G, first_label = 1, ordering = 'default')
    numNodes = nx.number_of_nodes(G)
    nodes = [i + 1 for i in range(numNodes)]

    print("Initializing Integer Linear Program")
    print("-----------------------------------")
    problem = LpProblem("IdentifyingCodes1", LpMinimize)
    x = LpVariable.dict("x_%s", nodes, 0, 1, LpInteger)

    problem += sum(x[i] for i in nodes)
    valColor = 0
    neighbor = []


    print("Adding Coloring Constraints")
    print("-----------------------------------")
    for i in nodes:
        valColor = 0
        neighbor = list(G.neighbors(i))
        neighbor = neighbor + [i]
        for j in neighbor:
            valColor += x[j]
        problem += valColor >= 1, "Coloring_Constraint_{}".format(i)
    valUnique = 0
    neighbor_i = []
    neighbor_j = []

    comb = combinations(nodes, 2)
    print("Adding Uniqueness Constraints")
    print("-----------------------------------")

    for i in comb:
        pair = list(i)
        node1 = pair[0]
        node2 = pair[1]
        neighbor1 = list(G.neighbors(node1))
        neighbor1 = neighbor1 + [node1]
        neighbor2 = list(G.neighbors(node2))
        neighbor2 = neighbor2 + [node2]
        set1 = set(neighbor1)
        set2 = set(neighbor2)
        unique = list(set1.symmetric_difference(set2))
        for k in unique:
            valUnique += x[k]
        problem += valUnique >= 1, "Uniqueness_Constraint_{}".format(i)
        valUnique = 0

    print("Solving")
    print("-------------------------------------------------------")
    problem.solve(GUROBI())
    if LpStatus[problem.status] == 'Optimal':
        for v in problem.variables():
            print(v.name, "=", v.varValue)
    print("-------------------------------------------------------")
    print("Amount of Resources Required for Unique Monitoring: {}".format(value(problem.objective)))
    print("Total number of nodes: {}".format(G.number_of_nodes()))
    print("% Savings: {}".format(float(100 * (G.number_of_nodes() - int(value(problem.objective))) / G.number_of_nodes())))
    print("-------------------------------------------------------")
    print("Time taken = {} seconds".format(time.time() - start))
    print("-------------------------------------------------------")
    

def main():
    filetype = input("Please indicate the input file type (csv or txt):")
    model(filetype)


if __name__ == '__main__':
    main()