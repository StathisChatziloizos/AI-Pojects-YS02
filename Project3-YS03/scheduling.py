import csp
import csv
import contextlib
import random

class Course:

    totalCourses = 0

    def __init__(self, semester_, courseName_, professor_, isDifficult_, hasLab_):
        self.semester = semester_
        self.courseName = courseName_
        self.professor = professor_
        self.isDifficult = isDifficult_
        self.hasLab = hasLab_

        Course.totalCourses += 1
        self.index = Course.totalCourses


    def print(self):
        print(f"----------- Course({self.index}) -----------")
        print(f"Semester: {self.semester}")
        print(f"Course Name: {self.courseName}")
        print(f"Professor: {self.professor}")
        print(f"difficult: {self.isDifficult}")
        print(f"Lab: {self.hasLab}")
        

class Scheduling(csp.CSP):

    inputFile = 'Στοιχεία Μαθημάτων.csv'
    daysNum = 21

    def __init__(self):
        self.variables = []
        # Dictionary {variable : domain of that variable}
        self.domains = dict()
        # 2 variables are neighbors if the value of the one affects the other
        self.neighbors = dict()
        self.row = dict()
        self.courses = []
        self.difficultList = []

        self.setVariables(Scheduling.inputFile, Scheduling.daysNum)
        self.setDomain()
        self.setNeighbors()
        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraintFunction)





    def readFile(self, inputFile):
        """Reads a csv file of courses and stores the necessary data to a courses list"""
        courses = []
        with open(inputFile,'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            next(csv_reader)
            # i = 0
            for item in csv_reader:
                # i+=1
                # if i > 5:
                #     return
                course = Course(int(item[0]), item[1], item[2], item[3], item[4])
                courses.append(course)
                # If it has a lab
                if item[4] == 'TRUE':
                    courseLab = Course(-1, 'LAB_' + item[1], item[2], ' - ', ' - ')
                    courses.append(courseLab)
                # If its a difficult course
                if item[3] == 'TRUE':
                    self.difficultList.append(course.index)

        # for course in courses:
        #     course.print()
        
        return courses

    def setVariables(self,inputFile, daysNum):
        """ Variables of form (x,y) """
        self.courses = self.readFile(inputFile)
        for i in range(1, Course.totalCourses+1):
            for j in range(1, daysNum+1):
            #     print('-', end=' ')
            # print("\n")
                self.variables.append((i,j))
        # print(self.variables)

    def setDomain(self):
        """ Domain of form (M,N,A,-) --> (Morning, Noon, Afternoon, Empty) """
        for var in self.variables:
            # self.domains[var] = ['9-12','12-3','3-6', '-']
            self.domains[var] = ['-','9-12','12-3','3-6']
            # self.domains[var] = [111,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
            # self.domains[var] = ['M','N','A']
            # print(self.domains)

    def setNeighbors(self):
        for var in self.variables:
            (x,y) = var
            # Variable to the right of var
            varR = (x,y+1)
            # Variable to the right of varR
            varRR = (x,y+2)
            for i in range(1,Course.totalCourses+1):
                if i != var[0]:
                    self.neighbors.setdefault(var,[]).append((i, var[1]))
            
            # if y+1 < Scheduling.daysNum+1:
            #     for i in range(1,Course.totalCourses+1):
            #         if i != var[0]:
            #             # add column to the right of var
            #             self.neighbors.setdefault(var,[]).append((i, varR[1]))

            # if y+2 < Scheduling.daysNum+1:
            #     for i in range(1,Course.totalCourses+1):
            #         if i != var[0]:
            #             # add column to the right of var
            #             self.neighbors.setdefault(var,[]).append((i, varRR[1]))
            for i in range(1, Scheduling.daysNum+1):
                if i != var[1]:
                    self.neighbors.setdefault(var,[]).append((var[0], i))
                    # if i+1 < Scheduling.daysNum+1:
                    #     self.neighbors.setdefault(var,[]).append((var[0], i+1))
                    # if i+2 < Scheduling.daysNum+1:
                    #     self.neighbors.setdefault(var,[]).append((var[0], i+2))
                    self.row.setdefault(var,[]).append((var[0], i))
                # if self.courses[var[0]-1].isDifficult == 'TRUE' and (var[0], i) not in self.difficult:
                #     self.difficult.setdefault(var,[]).append((var[0], i))
            # for i in range(1,Course.totalCourses+1):
            #     if self.courses[var[0]-1].isDifficult == 'TRUE':
            #         self.difficult.add(var)
            #         for v in self.row[var]:
            #             self.difficult.add(v)

        A = (4,5)
        # print(A, self.neighbors[A])
        # print(self.neighbors)

    # i = course counter, j = day
    def constraintFunction(self, A, a, B, b):
        if A == B:
            return True

        # Indexes of the courses corresponding to variables A and B
        courseA_index = A[0] - 1
        courseB_index = B[0] - 1
        # For same column - same day
        if A[1] == B[1]:
            if a == b != '-':
                return False

            # Courses of the same semester can't be on the same day.
            # Labs are excluded from this constraint, hence semester > 0
            # (labs' semesters are set by default to -1)
            if self.courses[courseA_index].semester == self.courses[courseB_index].semester > 0:
                # A and B cannot be both occupied
                if a != '-' and b != '-':
                    return False
# ------------------------------------------------------------------------------------------------
            # Courses of the same professor
            if self.courses[courseA_index].professor == self.courses[courseB_index].professor:
                # Labs are excluded from this constraint, because they can be and should be on the same day
                if self.courses[courseA_index].semester != -1 and self.courses[courseB_index].semester != -1:
                    # If both variables have a value corresponding to an assigned slot
                    if a != '-' and b !='-':
                        # print(f"A = {A}, B = {B}, a = {a}, b = {b}")
                        return False

# ------------------------------------------------------------------------------------------------

        # For same row - same course
        if A[0] == B[0]:
            if a == b != '-':
                return False
            if a == '9-12' or a == '12-3' or a == '3-6':
                if b != '-':
                    return False
        
        if self.courses[courseA_index].hasLab == 'TRUE':
            if a == '3-6':
                return False
            if B == (A[0] + 1,A[1]):
                if a == '9-12' and b != '12-3':
                    return False
                if a == '12-3' and b != '3-6':
                    return False


        if self.courses[courseB_index].hasLab == 'TRUE':
            if b == '3-6':
                return False
            if A == (B[0] + 1,A[1]):
                if b == '9-12' and a != '12-3':
                    return False
                if b == '12-3' and a != '3-6':
                    return False
# **********************************************************************************************************
# TODO: Add two right columns, figure out the fcking bug 
# **********************************************************************************************************
                   

        if self.courses[courseA_index].isDifficult == self.courses[courseB_index].isDifficult == 'TRUE':
            # if  A[1] != B[1] and B[1] < A[1] + 2 and A[0] != B[0] and a != '-':
            # if A[0] != B[0]:
            if  A[1] <= B[1] <= A[1] + 1 and b != '-' and a!= '-':
                # pass
                # print("b != '-' (a,b)",a, b, A,B)
                return False
            if B[1] <= A[1] <= B[1] + 1 and a != '-' and b!= '-':
                # pass
                # print("a != '-' (a,b)",a, b, A,B)
                return False
# ------------------------------------------------------------------------------------------------

            if a!= '-':
                domain = self.curr_domains
                if domain:
                    for i in self.difficultList:
                        if A[1] + 1 <= Scheduling.daysNum and '-' not in domain[(i,A[1] + 1)]:
                            # print(f"AAA --- {A}, ({i},{A[1]+1}) --- {self.curr_domains[(i,A[1] + 1)]}")
                            return False
            if b!= '-':
                domain = self.curr_domains
                if domain:
                    for i in self.difficultList:
                        if B[1] + 1 <= Scheduling.daysNum and '-' not in domain[(i,B[1] + 1)]:
                            # print(f"BBB --- {B}, ({i},{B[1]+1}) --- {self.curr_domains[(i,B[1] + 1)]}")
                            return False

# ------------------------------------------------------------------------------------------------
        
        if A[0] == B[0]:
            if  a == b == '-':
                flag = False
                for var in self.row[A]:
                    if self.curr_domains:
                        domain = self.curr_domains[var]
                        if '9-12' in domain or '12-3' in domain or '3-6' in domain:
                            flag = True
                            break
                    else:
                        flag = True
                if flag == False:
                    # print(f"A,B = {A},{B}   {domain}")
                    # self.unassign(B,self.infer_assignment())
                    # self.unassign(A,self.infer_assignment())
                    return False

# ------------------------------------------------------------------------------------------------


                # if allVars:
                #     allEmpty = True
                #     for var in self.row[A]:
                #         if self.infer_assignment()[var] != '-':
                #             allEmpty = False
                #             break
                #     if allEmpty:
                #         pass
                        # return False

                    # if var in self.infer_assignment() and self.infer_assignment()[var] == '-':
                    #     return False
                        # print(s1.infer_assignment())
                        # print("\n\n")
                        # break
        # print(self.infer_assignment)
        # if a == '-':
        #     for var in self.row[A]:
        #         allEmpty = False
        #         if var in self.infer_assignment() and self.infer_assignment()[var] == a:
        #             # return False
        #             # print (self.infer_assignment()[var])
        #             break
        # assigned_vars = self.infer_assignment()
        # print(assigned_vars)

        # print(A, self.row[A])
        # if B in self.row[A]:
        #     if a == b == '-':
        #         allEmpty = True
        #         for var in self.row[A]:
        #             if '9-12' in self.curr_domains[var] or '12-3' in self.curr_domains[var] or '3-6' in self.curr_domains[var]:
        #                 print(var, self.curr_domains[var])
        #                 allEmpty = False
        #                 break
        #         if allEmpty:
        #             return False

        # if a == '-':
        #     allEmpty = True
        #     for var in self.row[A]:
        #         if var in self.infer_assignment():#self.infer_assignment()[var]:
        #             allEmpty = False
        #             break

        #     if allEmpty:
        #         return False
        
        # if b == '-':
        #     allEmpty = True
        #     for var in self.row[B]:
        #         if '9-12' in self.curr_domains[var] or '12-3' in self.curr_domains[var] or '3-6' in self.curr_domains[var]:
        #             allEmpty = False
        #             break

        #     if allEmpty:
        #         return False
                
        return True
        # return False


    def display(self, daysNum, assignment):
        with  open ('solution_csp_exams.txt', 'w') as f:
            with contextlib.redirect_stdout(f):
                print ("\n- - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - S O L U T I O N - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
                print("\n\nROW: Each row represents a course. Labs are also considered courses and are right beneath their corresponding course.")
                print("COLUMN: Each column represents a day")
                print("(ROW, COLUMN): Each (row, column) pair can have a time slot (9-12, 12-3, 3-6) or be empty (-)\n\n")
                print("      ", end='')
                for i in range (1,daysNum+1):
                    print(f"D{i:02d} ", end = '  ')
                print("\n")
                for i in range(1, Course.totalCourses+1):
                    print(f"C{i}.", end='  ')
                    for j in range(1, daysNum+1):
                        print(self.curr_domains[(i,j)], end=' ')
                        # print(f"[{assignment.get((i, j))}]", end='  ')
                    print("\n")




def main():
    # Exams Schedule
    exams = Scheduling()


    # FC algorithm
    # result = csp.backtracking_search(exams, select_unassigned_variable=csp.first_unassigned_variable, inference=csp.forward_checking, order_domain_values=csp.lcv)
    # MAC algorithm
    result =  csp.backtracking_search(exams, select_unassigned_variable=csp.first_unassigned_variable, inference=csp.mac, order_domain_values=csp.lcv)
    # MINCONFLICTS algorithm
    # random.shuffle(exams.variables)
    # result = csp.min_conflicts(exams, 100000)
    if result:
        print("Problem Satisfiable")
    else:
        print("Problem not Satisfiable")
    # csp.backtracking_search(exams)

    # s1.display(s1.infer_assignment())
    exams.display(Scheduling.daysNum, exams.infer_assignment())
    print(f"Number of assigns: {exams.nassigns}")
    # s1.display(s1.infer_assignment())
    # print(s1.infer_assignment())

if __name__ == "__main__":
    main()