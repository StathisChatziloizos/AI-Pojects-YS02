import csp
import csv

class Course:

    totalCourses = 0

    def __init__(self, semester_, courseName_, professor_, isHard_, hasLab_):
        self.semester = semester_
        self.courseName = courseName_
        self.professor = professor_
        self.isHard = isHard_
        self.hasLab = hasLab_

        Course.totalCourses += 1
        self.index = Course.totalCourses


    def print(self):
        print(f"----------- Course({self.index}) -----------")
        print(f"Semester: {self.semester}")
        print(f"Course Name: {self.courseName}")
        print(f"Professor: {self.professor}")
        print(f"Hard: {self.isHard}")
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
        self.courses = []

        self.setVariables(Scheduling.inputFile, Scheduling.daysNum)
        self.setDomain()
        self.setNeighbors()
        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraintFunction)




    def readFile(inputFile):
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
                if item[4] == 'TRUE':
                    courseLab = Course(-1, 'LAB_' + item[1], item[2], ' - ', ' - ')
                    courses.append(courseLab)

        # for course in courses:
        #     course.print()
        
        return courses

    def setVariables(self,inputFile, daysNum):
        """ Variables of form (x,y) """
        self.courses = Scheduling.readFile(inputFile)
        for i in range(1, Course.totalCourses+1):
            for j in range(1, daysNum+1):
            #     print('-', end=' ')
            # print("\n")
                self.variables.append((i,j))
        # print(self.variables)

    def setDomain(self):
        """ Domain of form (M,N,A,-) --> (Morning, Noon, Afternoon, Empty) """
        for var in self.variables:
            self.domains[var] = ['9-12','12-3','3-6', '-']
            # self.domains[var] = [111,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
            # self.domains[var] = ['M','N','A']
            # print(self.domains)

    def setNeighbors(self):
        for var in self.variables:
            for i in range(1,Course.totalCourses+1):
                if i != var[0]:
                    self.neighbors.setdefault(var,[]).append((i, var[1]))
            for i in range(1, Scheduling.daysNum+1):
                if i != var[1]:
                    self.neighbors.setdefault(var,[]).append((var[0], i))

        # print(self.neighbors)

    # i = course counter, j = day
    def constraintFunction(self, A, a, B, b):
        # For same column - same day
        if A[1] == B[1]:
            if a == b != '-':
                return False

            # Indexes of the courses corresponding to variables A and B
            courseA_index = A[0] - 1
            courseB_index = B[0] - 1

            # Courses of the same semester can't be on the same day.
            # Labs are obviously excluded from this constraint, hence semester > 0
            # (labs' semesters are set by default to -1)
            if self.courses[courseA_index].semester == self.courses[courseB_index].semester > 0:
                # A and B cannot be both occupied
                if a != '-' and b != '-':
                    return False

        # For same row - same course
        if A[0] == B[0]:
            if a == b != '-':
                return False
            if a == '9-12' or a == '12-3' or a == '3-6':
                if b != '-':
                    return False
        
        
        return True
        # return False


    def displayVariables(self, daysNum):
        for i in range(1, Course.totalCourses+1):
            for j in range(1, daysNum+1):
                print(self.curr_domains[(i,j)], end=' ')
            print("\n")
        

s1 = Scheduling()
csp.backtracking_search(s1)
# s1.display(s1.infer_assignment())
s1.displayVariables(Scheduling.daysNum)
# s1.display(s1.infer_assignment())
