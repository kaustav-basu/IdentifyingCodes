# IdentifyingCodes

ilp.py computes the Minimum Identifying Code Set (MICS) for a given graph. The MICS ensures that every node in the graph has unique identification

## Getting Started

ilp.py requires graphs as input. There are a few example graphs provided, under the folders Edge-List and UndirectedGraphs.

### Prerequisites

Firstly, the user must have a solver installed on their system. My code uses Gurobi, but it can be changed to other solvers, depending on the the solver installed in the user's system. 

Secondly, the user must have the following packages installed:

```
1. pandas 0.23.4
2. networkx 2.1
3. pulp 1.6.8
4. numpy 1.15.1
```

### Testing

Type python ilp.py to run the program. The program asks for the input filetype (csv or txt). Once provided, the program executes and displays the following:
1. The value of the indicator variables (0/1)
2. The optimal objective function value
3. The total number of nodes in the graph
4. The total % savings 
5. The amount of time taken for the execution of the code
