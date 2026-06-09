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
        next_proposal = [0] * nb_schools
        while any(len(school_partner[s]) < schools_capacity[s] and next_proposal[s] < nb_students for s in range(nb_schools)) :
            sch = next((sch for sch in range(nb_schools) if len(school_partner[sch]) < schools_capacity[sch] and next_proposal[sch] != nb_students), None)
            for _ in range(min(schools_capacity[sch] - len(school_partner[sch]), nb_students - next_proposal[sch])):
                stu = schools[sch][next_proposal[sch]]
                next_proposal[sch] += 1
                if student_partner[stu] is None:
                    student_partner[stu] = sch
                    school_partner[sch].add(stu)
                else:
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
            u = students[s][next_proposal[s]]
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

    a = random.sample(range(1,c),n -1 ) + [0, c]
    table3 = [a[i+1] - a[i] for i in range(len(a) - 1)]

    return table1, table2, table3


if __name__ == '__main__':
    schools, students, schools_capacity = generate_tables(9, 10, 9)
    result, count = stableMarriageAlgorithm(schools, students, schools_capacity, True)
    display_assignment_table(result, students, schools, count)