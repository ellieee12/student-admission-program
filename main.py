from collections import defaultdict
from typing import List, Tuple, Set
import pandas as pd
import random

def prefers(students: List[List[int]], stu: int, sch: int, sch1: int) -> bool:
    return students[stu][sch] < students[stu][sch1]

def lowest_preferred_candidate(universities, u, s, currentStudents):
    currentStudents = list(currentStudents)
    worst = None
    for candidate in currentStudents:
        # university prefers s over this candidate (higher rank = less preferred)
        if universities[u][s] < universities[u][candidate]:
            if worst is None or universities[u][candidate] > universities[u][worst]:
                worst = candidate  # store the student INDEX, not the rank
    return worst

def stableMarriageAlgorithm(schools: List[List[int]], students: List[List[int]], schools_capacity: List[int], changeBidding: bool) -> Tuple[List[Set[int]], int]:
    nb_schools = len(schools)
    nb_students = len(students)
    student_partner = defaultdict(lambda: None)
    school_partner = [set() for _ in range(nb_schools)]
    nb_iterations = 0
    if changeBidding :
        # set proposal index to 0
        next_proposal = [0] * nb_schools
        # while all schools are not yet full and the schools have finished their proposals
        while any(len(school_partner[s]) < schools_capacity[s] and next_proposal[s] < nb_students for s in range(nb_schools)) :
            # get the next school that is not full and has available place 
            sch = next((sch for sch in range(nb_schools) if len(school_partner[sch]) < schools_capacity[sch] and next_proposal[sch] != nb_students), None)
            # the school proposes to the n first candidates according to its remaining capacity or the minimum proposition left
            for _ in range(min(schools_capacity[sch] - len(school_partner[sch]), nb_students - next_proposal[sch])):
                #identify which student to propose to
                stu = schools[sch].index(next_proposal[sch])
                #increase proposal index by 1
                next_proposal[sch] += 1
                #if the student does not have a university, they are matched
                if student_partner[stu] is None:
                    student_partner[stu] = sch
                    school_partner[sch].add(stu)
                else:
                    # if the student already has a university matched, we identify the student's preference 
                    sch1 = student_partner[stu]
                    if prefers(students, stu, sch, sch1):
                        student_partner[stu] = sch
                        school_partner[sch1].remove(stu)
                        school_partner[sch].add(stu)
            nb_iterations += 1
    else:
        next_proposal = [0] * nb_students
        #while there is a student without a university and has not finished his proposals
        while any(student_partner[s] is None and next_proposal[s] < nb_schools for s in range(nb_students)):
            #finds first free students in the list
            s = next((s for s in range(nb_students) if student_partner[s] is None and next_proposal[s] != nb_schools), None)
            #identify which school to propose to
            u = students[s].index(next_proposal[s])
            #avances proposal index of their unasked school
            next_proposal[s] += 1
            #If a university capacity is not yet achieved
            if len(school_partner[u]) < schools_capacity[u]: 
                school_partner[u].add(s)
                student_partner[s] = u
            else: 
                # if the university prefers s over one of current students
                if (stu_lowest_preference := lowest_preferred_candidate(schools, u, s, school_partner[u])) is not None:
                    school_partner[u].remove(stu_lowest_preference)
                    school_partner[u].add(s)
                    student_partner[s] = u
                    student_partner[stu_lowest_preference] = None
            nb_iterations += 1
    # check if there is enough places for the amount students
    if sum(1 for v in student_partner.values() if v is not None) < nb_students:
        print("there is not enough space for all students")
    return school_partner, nb_iterations

def display_assignment_table(partner: List[Set], students: List[List[int]], schools: List[List[int]], nb_iteration: int):
    rows = []
    for sch, students_set in enumerate(partner):
        for stu in sorted(students_set):
            rows.append({
                "Student": stu,
                "School":  sch,
                "Student's preference rank": students[stu][sch] + 1,
                "School's preference rank": schools[sch][stu] + 1,
            })
 
    df_assignments = pd.DataFrame(rows).sort_values("Student").reset_index(drop=True)
    df_assignments.index += 1
    print(df_assignments.to_string())
    print(f"Number of iteration: {nb_iteration}")

def generate_tables(n, m, c):
    table1 = []
    for _ in range(n):
        row = list(range(m))
        random.shuffle(row)
        table1.append(row)

    table2 = []
    for _ in range(m):
        row = list(range(n))
        random.shuffle(row)
        table2.append(row)

    if c >= n:
        a = sorted(random.sample(range(1, c), n - 1) + [0, c])
        table3 = [a[i+1] - a[i] for i in range(len(a) - 1)]
    else:
        a = sorted(random.sample(range(1, c), c - 1) + [0, c]) if c > 1 else [0, c]
        parts = [a[i+1] - a[i] for i in range(len(a) - 1)]
        table3 = parts + [0] * (n - len(parts))

    return table1, table2, table3

if __name__ == '__main__':
    # # universities[u][s] = rank university u gives to student s (lower = more preferred)
    # universities = [
    #     [0, 2, 4, 5, 1, 3],  # Uni 0: prefers s0 > s4 > s1 > s5 > s2 > s3
    #     [3, 1, 2, 4, 5, 0],  # Uni 1: prefers s1 > s2 > s5 > s0 > s3 > s4
    #     [5, 1, 3, 0, 2, 4],  # Uni 2: prefers s3 > s1 > s4 > s2 > s5 > s0
    #     [2, 4, 0, 3, 1, 5],  # Uni 3: prefers s2 > s4 > s0 > s3 > s1 > s5
    # ]
    # universities_capacity = [1, 1, 1, 1]  # total capacity = 7 > 6 students, all should be matched

    # # students[s][i] = university at position i in student s's preference list
    # students = [
    #     [0, 3, 1, 2],  # s0: prefers Uni0 > Uni3 > Uni1 > Uni2
    #     [1, 2, 0, 3],  # s1: prefers Uni1 > Uni2 > Uni0 > Uni3
    #     [3, 0, 2, 1],  # s2: prefers Uni3 > Uni0 > Uni2 > Uni1
    #     [2, 1, 3, 0],  # s3: prefers Uni2 > Uni1 > Uni3 > Uni0
    #     [0, 1, 3, 2],  # s4: prefers Uni0 > Uni1 > Uni3 > Uni2
    #     [1, 3, 0, 2],  # s5: prefers Uni1 > Uni3 > Uni0 > Uni2
    # ]
    
    schools, students, schools_capacity = generate_tables(9, 10, 9)
    result, count = stableMarriageAlgorithm(schools, students, schools_capacity, False)
    display_assignment_table(result, students, schools, count)