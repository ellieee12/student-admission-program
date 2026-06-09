from collections import defaultdict
from typing import List, Tuple, Set
import pandas as pd
import random

def prefers(students: List[List[int]], stu: int, sch: int, sch1: int) -> bool:
    return students[stu][sch] < students[stu][sch1]

def stableMarriage(schools: List[List[int]], students: List[List[int]], schools_capacity: List[int]) -> Tuple[List[Set[int]], int]:
    n = len(schools)
    student_partner = defaultdict(lambda: None)
    school_partner = [set() for _ in range(n)]
    next_proposal = [0] * n
    nb_iterations = 0
    while len(student_partner) < n :
        if (sch := next((sch for sch in range(n) if len(school_partner[sch]) < schools_capacity[sch]), None)) is None:
            print("there is not enough space for all students")
            return school_partner, nb_iterations
        for _ in range(schools_capacity[sch] - len(school_partner[sch])):
            stu = schools[sch][next_proposal[sch]]
            next_proposal[sch] += 1
            if student_partner[stu] is None:
                student_partner[stu] = sch
                school_partner[sch].add(stu)
            else:
                sch1 = student_partner[stu]
                if prefers(students, stu, sch, sch1):
                    student_partner[stu] = sch
                    school_partner[sch1].discard(stu)
                    school_partner[sch].add(stu)
        nb_iterations += 1
    return school_partner, nb_iterations

def display_assignment_table(school_partner: List[Set], students: List[List[int]], nb_iteration: int):
    rows = []
    for sch, students_set in enumerate(school_partner):
        for stu in sorted(students_set):
            rows.append({
                "Student": stu,
                "School":  sch,
                "Student's preference rank": students[stu][sch] + 1,
            })
 
    df_assignments = pd.DataFrame(rows).sort_values("Student").reset_index(drop=True)
    df_assignments.index += 1
    print(df_assignments.to_string())
    print(f"Number of iteration: {nb_iteration}")


def generate_tables(n, m):
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

    return table1, table2


if __name__ == '__main__':
    schools, students = generate_tables(9, 10)

    schools_capacity = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    result, count = stableMarriage(schools, students, schools_capacity)
    display_assignment_table(result, students, count)