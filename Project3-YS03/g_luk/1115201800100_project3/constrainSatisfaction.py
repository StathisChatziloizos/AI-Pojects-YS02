import os
import time
import random
import sys
from csp import *
from utils import argmin_random_tie, count, first
# The file identifier of the problem to be solved
problem = "2-f24"
# The global dictionary of constrains
constrains = None

# ----------------------------------------- File Parsing --------------------------------------------

def getProblem(problemId = problem):

    var = getVariables(problemId);
    dom = getDomains(problemId);
    (variables, domains) = mapVariablesToDomains(var, dom);
    ctr = getConstrains(problemId);
    neighbors = getNeighbors(var, ctr);
    return {
        "variables" : variables,
        "domains" : domains,
        "neighbors" : neighbors, 
        "constrains" :ctr,
    }

# Turn the var file to a list of (variable, domainId) tuples
def getVariables(problemId = problem):
    # print("Parsing Variables");
    try:
        fileToOpen = "var"+problemId+".txt";
        variableFile = open("./rlfap/"+fileToOpen);
    except OSError:
        return None;
    n = int(variableFile.readline());
    variables = list();
    for i in range(n):
        line = variableFile.readline();
        values = line.split(" ");
        var = int(values[0]);
        dom = int(values[1]);
        t = (var, dom);
        variables.append(t);
    variableFile.close();
    return variables;

# Turn the dom file into a {domainId: [domain]} dictionary 
def getDomains(problemId = problem):
    # print("Parsing Domains");
    try:
        fileToOpen = "dom"+problemId+".txt";
        domainFile = open("./rlfap/"+fileToOpen);
    except OSError:
        return None;

    n = int(domainFile.readline())
    domains = dict();
    for i in range(n):
        line = domainFile.readline();
        values = line.split(" ");
        domId = int(values[0]);
        dom = list();
        for j in range(2,len(values)):
            dom.append(int(values[j]));
        domains[domId] = dom;
    domainFile.close();
    return domains;

# Turn the ctr file into a {(Var1, Var2): (Operator, Constant)} dictionary
def getConstrains(problemId = problem):
    # print("Parsing Constrains");
    try:
        fileToOpen = "ctr"+problemId+".txt";
        constrainFile = open("./rlfap/"+fileToOpen);
    except OSError:
        return None;
    n = int(constrainFile.readline());
    constrains = dict();
    for i in range(n):
        line = constrainFile.readline();
        values = line.split(" ");
        var1 = int(values[0]);
        var2 = int(values[1]);
        operator = values[2];
        constant = int(values[3]);
        t1 = (var1, var2);
        t2 = (operator, constant);
        constrains[t1] = t2;
    constrainFile.close();
    return constrains;

# Turn the output from the getVariables and getDomains functions to the format used by the CSP class
def mapVariablesToDomains(var, doms):
    variables = list();
    domains = dict();
    for v in var:
        variables.append(v[0]);
        domains[v[0]] = doms[v[1]];
    return (variables, domains);

# Create a {Variable : [Neighbors]} dictionary
def getNeighbors(var, ctr):
    neighbors = dict();
    for v in var:
        neighbors[v[0]] = list();

    for c in ctr:
        if c[1] not in neighbors[c[0]]:
            neighbors[c[0]].append(c[1]);
        if c[0] not in neighbors[c[1]]:
            neighbors[c[1]].append(c[0]);
    return neighbors;

# A funtion that, given two variables and their respective values, determines if the contrains are met
def constrainFunction(A, a, B, b, problemId = problem):
    # Avoid continiously parsing the constrain file by keeping the constrain dictionary in a global variable
    global constrains
    if not constrains:
        constrains = getConstrains(problemId);

    diff = abs(int(a)-int(b));

    if (A,B) in constrains:
        constrain1 = constrains[(A,B)]
        diff1 = constrain1[1];
        operator1 = constrain1[0];
        if operator1 == ">" and diff <= diff1:
            return False
        if operator1 == "<" and diff >= diff1:
            return False
        if operator1 == "=" and diff != diff1:
            return False

    if (B,A) in constrains:
        constrain2 = constrains[(B,A)];
        diff2 = constrain2[1];
        operator2 = constrain2[0];

        if operator2 == ">" and diff <= diff2:
            return False
        if operator2 == "<" and diff >= diff2:
            return False
        if operator2 == "=" and diff != diff2:
            return False

    return True;

# ----------------------------------------- Constrain Satisfaction Search --------------------------------------------


# BT
def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        # If we have assigned all the variables return the assignment
        if len(assignment) == len(csp.variables):
            return assignment
        # Select the next variable to assign
        var = select_unassigned_variable(assignment, csp, weights)
        # For each of it's remaining values
        for value in order_domain_values(var, assignment, csp):
            # If it doen't conflict with the current assignment
            if 0 == csp.nconflicts(var, value, assignment):
                # Assign it
                csp.assign(var, value, assignment)
                # print(f"{var} -> {value}");
                # Remove the rest of it's values from its domain
                removals = csp.suppose(var, value)
                # Remove the non compatible values from it's neighbors' domains. If all have at least one value left then continue
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                else:
                    for neighbor in csp.neighbors[var]:
                        if not csp.curr_domains[neighbor]:
                            weights[(var,neighbor)] += 1;
                            weights[(neighbor,var)] += 1;

                # Else undo
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    weights = {(x,y):1 for x in csp.variables for y in csp.neighbors[x]};
    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

# CBJ
def backjumping_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values= unordered_domain_values, inference= no_inference):

    def backtrack(assignment):
        # If we have assigned all the variables return the assignment
        if len(assignment) == len(csp.variables):
            return assignment
        # Select the next variable to assign
        var = select_unassigned_variable(assignment, csp, weights)
        # For each of it's remaining values
        for value in order_domain_values(var, assignment, csp):
            # If it doesn't conflict with the current assignment
            if 0 == csp.nconflicts(var, value, assignment):
                # Assign it
                csp.assign(var, value, assignment)
                # Keep the order in which the variables have been assigned
                if var not in assignmentOrder:
                    assignmentOrder.append(var);
                # print(f"{var} -> {value}");
                # Remove the rest of it's values from its domain
                removals = csp.suppose(var, value)
                # Remove the non compatible values from it's neighbors' domains. If all have at least one value left then continue
                if inference(csp, var, value, assignment, removals):
                    # For every variable that has lost values due to this assignment add var to it's confict set
                    for r in removals:
                        if r[0] != var:
                            if var not in conflictSets[r[0]]:
                                # Update it's conflict set
                                conflictSets[r[0]].append(var);
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                else:
                    # If there are any variables with no more values left update the weight of the corresponding constrain
                    for neighbor in csp.neighbors[var]:
                        if not csp.curr_domains[neighbor]:
                            weights[(var,neighbor)] += 1;
                            weights[(neighbor,var)] += 1;
                # Else undo
                csp.restore(removals)

        # If there are elements in the conflict set of a the current variable
        if len(conflictSets[var]) !=0:
            # Find the last variable that caused a confict with var
            backjumpTo = assignmentOrder[max([assignmentOrder.index(x) for x in conflictSets[var]])];
        # If the conflict set of the current variable is empty just backtrack
        else:
            for variable in csp.variables:
                if var in conflictSets[variable]:
                    conflictSets[variable].remove(var);
            csp.unassign(var, assignment)
            if var in assignmentOrder:
                assignmentOrder.remove(var);
            return None
        # Remove it from var's conflictSet
        conflictSets[var].remove(backjumpTo);
        # Remove the value that caused the conflict from the domain of the variable that caused the confict
        # csp.prune(backjumpTo, assignment[backjumpTo], []);
        # From every variable assigned inbetween the jump
        for v in assignmentOrder[assignmentOrder.index(backjumpTo):]:
            # Remove it from the conflict sets of other variables
            for variable in csp.variables:
                if v in conflictSets[variable]:
                    conflictSets[variable].remove(v);
            # Unassign it
            try:
                csp.unassign(v, assignment);
                assignmentOrder.remove(v);
            except KeyError:
                print("Key Error")

        for c in conflictSets[var]:
            if c not in conflictSets[backjumpTo]:
                conflictSets[backjumpTo].append(c);

        return None

    conflictSets = list();
    for v in csp.variables:
        conflictSets.append(list());   
    assignmentOrder = list(); 
    weights = {(x,y):1 for x in csp.variables for y in csp.neighbors[x]};
    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result


# ----------------------------------------- Variable Selection --------------------------------------------

def num_legal_values(cs, var, assignment):
    if cs.curr_domains:
        return len(cs.curr_domains[var])
    else:
        return count(cs.nconflicts(var, val, assignment) == 0 for val in cs.domains[var])

def first_unassigned_variable(assignment, cs, weights):
    """The default variable order."""
    # First not assigned variable
    return first([var for var in cs.variables if var not in assignment])


def mrv(assignment, csp, weights):
    """Minimum-remaining-values heuristic."""
    # Variable with least remaining values in its domain
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))

def domWeg(assignment, cs, weights):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in cs.variables if v not in assignment],
                             key=lambda var: num_legal_values(cs, var, assignment)/sum([weights[(var,y)] for y in cs.neighbors[var]]))


# --------------------------------------------- Inference ----------------------------------------------------

def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    # For each neighbor of var
    for B in csp.neighbors[var]:
        # If it hasn't been assigned
        if B not in assignment:
            # For each of its available values
            for b in csp.curr_domains[B][:]:
                # If it's not consistent with the "value" of var delete it
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            # If there is a neighbor with no more values in its domain we failed
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals, constraint_propagation=AC4):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

# ---------------------------------------------------------------------------------------------------------------

def main():

    print(f"---------------PROBLEM {problem}-------------------")
    # Parse the variable file
    var = getVariables(problem);
    # Parse the domain file
    dom = getDomains(problem);
    # Parse the constrain file
    ctr = getConstrains(problem);
    # Turn the parsed data to the format needed by the csp constructor
    (variables, domains) = mapVariablesToDomains(var, dom);
    neighbors = getNeighbors(var, ctr);
    cs =  CSP(variables, domains, neighbors, constrainFunction);

    totalTime = 0;
    totalAssignments = 0;
    # FC algorithm
    print("***FC algorithm***");
    for i in range(3):
        # Create a fresh problem (leaving the previous curr_domains as it is will provide the already found solution to the new iteration of the search)
        cs =  CSP(variables, domains, neighbors, constrainFunction);
        fcStartTime = time.time();
        resultFC =  backtracking_search(cs, select_unassigned_variable= domWeg, inference=  forward_checking, order_domain_values= lcv);
        fcEndTime = time.time();
        # print(resultFC);
        if resultFC:
            print("SAT");
        else:
            print("UNSAT")
        print(f"Time: {fcEndTime-fcStartTime} seconds");
        print(f"Assignments: {cs.nassigns}");
        totalTime = totalTime + (fcEndTime-fcStartTime);
        totalAssignments = totalAssignments +cs.nassigns;
    print(f"Average time: {totalTime/3}");
    print(f"Average assignments: {totalAssignments/3}");

    print();

    totalTime = 0;
    totalAssignments = 0;
    # MAC algorithm
    print("***MAC algorithm***");
    for i in range(3):
        # Create a fresh problem (leaving the previous curr_domains as it is will provide the already found solution to the new iteration of the search)
        cs =  CSP(variables, domains, neighbors, constrainFunction);
        macStartTime = time.time();
        resultMac =  backtracking_search(cs, select_unassigned_variable= domWeg, inference=  mac, order_domain_values= lcv);
        macEndTime = time.time();
        # print(resultMac);
        if resultMac:
            print("SAT");
        else:
            print("UNSAT")
        print(f"Time: {macEndTime-macStartTime} seconds");
        print(f"Assignments: {cs.nassigns}");
        totalTime = totalTime + (macEndTime-macStartTime);
        totalAssignments = totalAssignments +cs.nassigns;
    print(f"Average time: {totalTime/3}");
    print(f"Average assignments: {totalAssignments/3}");

    print();

    totalTime = 0;
    totalAssignments = 0;
    # FC-CBJ algorithm
    print("***CBJ algorithm***");
    for i in range(3):
        # Create a fresh problem (leaving the previous curr_domains as it is will provide the already found solution to the new iteration of the search)
        cs =  CSP(variables, domains, neighbors, constrainFunction);
        cbjStartTime = time.time();
        resultCBJ =  backjumping_search(cs, select_unassigned_variable=domWeg, inference=  forward_checking, order_domain_values= lcv);
        cbjEndTime = time.time();
        if resultCBJ:
            print("SAT");
        else:
            print("UNSAT")
        print(f"Time: {cbjEndTime-cbjStartTime} seconds");
        print(f"Assignments: {cs.nassigns}");
        totalTime = totalTime + (cbjEndTime-cbjStartTime);
        totalAssignments = totalAssignments +cs.nassigns;
    print(f"Average time: {totalTime/3}");
    print(f"Average assignments: {totalAssignments/3}");

    print();

    # Min conflict algorithm
    print("***Min conflict algorithm***");
    for i in range(3):
        # Shuffle the variables to increase chances of success
        random.shuffle(variables);
        cs =  CSP(variables, domains, neighbors, constrainFunction);
        minStartTime = time.time();
        resultMin = min_conflicts(cs, 10000);
        minEndTime = time.time();
        # print(resultMin);
        if resultMin:
            print("SAT");
        else:
            print("UNSAT");
        print(f"Time: {minEndTime-minStartTime} seconds");
        print(f"Assignments: {cs.nassigns}");

if __name__ == "__main__":
    main()


