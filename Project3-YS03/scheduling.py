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
        self.counter = Course.totalCourses


    def print(self):
        print(f"----------- Course({self.counter}) -----------")
        print(f"Semester: {self.semester}")
        print(f"Course Name: {self.courseName}")
        print(f"Professor: {self.professor}")
        print(f"Hard: {self.isHard}")
        print(f"Lab: {self.hasLab}")
        

class Scheduling(csp.CSP):
    def __init__(self):
        self.variables = []
        # Dictionary {variable : domain of that variable}
        self.domains = dict()
        # 2 variables are neighbors if the value of the one affects the other
        self.neighbors = dict()


    inputFile = 'Στοιχεία Μαθημάτων.csv'
    daysNum = 21


    def readFile(inputFile):
        """Reads a csv file of courses and stores the necessary data to a courses list"""
        courses = []
        with open(inputFile,'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            next(csv_reader)
            for item in csv_reader:
                course = Course(item[0], item[1], item[2], item[3], item[4])
                courses.append(course)
                if item[4] == 'TRUE':
                    courseLab = Course(item[0], 'LAB_' + item[1], item[2], ' - ', ' - ')
                    courses.append(courseLab)

        # for course in courses:
        #     course.print()
        
        return courses

    def setVariables(self,inputFile, daysNum):
        """ Variables of form (x,y) """
        courses = Scheduling.readFile(inputFile)
        for i in range(1,Course.totalCourses+1):
            for j in range(1,daysNum+1):
            #     print('-', end=' ')
            # print("\n")
                self.variables.append((i,j))
        # print(self.variables)

    def setDomain(self):
        """ Domain of form (M,N,A,-) --> (Morning, Noon, Afternoon, Empty) """
        for var in self.variables:
            self.domains[var] = ['M','N','A', '-']
            # print(self.domains)

    def setNeighbors(self):
        for var in self.variables:
            for i in range(1,Course.totalCourses+1):
                if i != var[0]:
                    self.neighbors.setdefault(var,[]).append((i, var[1]))

        # print(self.neighbors)
        

s1 = Scheduling()
s1.setVariables(Scheduling.inputFile, Scheduling.daysNum)
s1.setDomain()
s1.setNeighbors()