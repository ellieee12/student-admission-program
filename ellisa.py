from typing import List
from collections import defaultdict
import pandas as pd


# Check if woman prefers m over current partner m1
def prefers(universities: List[List[int]], u: int, s: int, currentStudents: List[int]) -> bool:
    currentStudents = list(currentStudents)
    for i in range(len(currentStudents)):
        if universities[u][s]<universities[u][currentStudents[i]] :
            return True
    return False

    

def universitiesChooseStudents(universities: List[List[int]], students: List[List[int]], universities_capacity : List[int]) :
    nb_students = len(students)
    nb_universities = len(universities)
    # universities_partner = defaultdict(lambda: None)
    universities_candidates = [set() for _ in range(nb_universities)]

    #Initialize all universities and students to free
    # rows,cols = (nb_universities,max(uni_capabilites))
    # universities_candidates = [[-2]*cols]*rows
    
    # man's current partners
    student_current_uni = [-1] * nb_students
    
    # next proposal index
    next_proposal = [0] * nb_students
    
    # Free Men
    free_students = [True] * nb_students

    free_count = nb_students

    nb_iterations = 0

    while free_count > 0:
        #finds first free students in the list
        s = next((s for s in range(nb_students) if free_students[s]), None)
        #identify which school to propose to
        u = students[s][next_proposal[s]]
        #avances proposal index of their unasked school
        next_proposal[s] += 1
        #If a university capacity is not yet achieved
        if len(universities_candidates[u])<universities_capacity[u] : 
            universities_candidates[u].add(s)
            student_current_uni[s] = u
            free_students[s] = False
            free_count -= 1
        else : 
            # if the university prefers s over one of current students
            if prefers(universities,u,s,universities_candidates[u]) :
                stu_lowest_preference = lowest_preferred_candidate(universities,u,s,universities_candidates[u])
                universities_candidates[u].remove(stu_lowest_preference)
                universities_candidates[u].add(s)
                free_students[s] = False
                free_students[stu_lowest_preference] = True
        nb_iterations =+ 1
    return [universities_candidates,nb_iterations]



def lowest_preferred_candidate (universities: List[List[int]], u: int, s: int, currentStudents: List[int]) -> int:
    currentStudents = list(currentStudents)
    min = currentStudents[0]
    for i in range (1,len(currentStudents)) :
        if universities[u][currentStudents[i]]<universities[u][min] :
            min = universities[u][currentStudents[i]]
    return min

    #     # If w is free
    #     if w_partner[w] == -1:
    #         w_partner[w] = m
    #         m_partner[m] = w
    #         free_man[m] = False
    #         free_count -= 1
    #     else:
    #         m1 = w_partner[w]

    #         # If w prefers m over current partner
    #         if prefers(women, w, m, m1):
    #             w_partner[w] = m 
    #             m_partner[m] = w

    #             free_man[m] = False
    #             free_man[m1] = True
    #     nb_iterations=nb_iterations+1

    # print(nb_iterations)
    # return m_partner
def display_assignment_table(school_partner: List[set], students: List[List[int]], nb_iteration: int):
    rows = []
    for sch, students_set in enumerate(school_partner):
        for stu in sorted(students_set):
            rows.append({
                "Student": stu,
                "School":  sch,
                "Student's preference rank": students[sch][stu] + 1,
            })
 
    df_assignments = pd.DataFrame(rows).sort_values("Student").reset_index(drop=True)
    df_assignments.index += 1
    print(df_assignments.to_string())
    print(f"Number of iteration: {nb_iteration}")
if __name__ == '__main__':
    n_students = 6
    n_universities = 4

    # universities[u][s] = rank university u gives to student s (lower = more preferred)
    universities = [
        [0, 2, 4, 5, 1, 3],  # Uni 0: prefers s0 > s4 > s1 > s5 > s2 > s3
        [3, 0, 1, 4, 5, 2],  # Uni 1: prefers s1 > s2 > s5 > s0 > s3 > s4
        [5, 1, 3, 0, 2, 4],  # Uni 2: prefers s3 > s1 > s4 > s2 > s5 > s0
        [2, 4, 0, 3, 1, 5],  # Uni 3: prefers s2 > s4 > s0 > s3 > s1 > s5
    ]
    universities_capacity = [2, 2, 1, 2]  # total capacity = 7 > 6 students, all should be matched

    # students[s][i] = university at position i in student s's preference list
    students = [
        [0, 3, 1, 2],  # s0: prefers Uni0 > Uni3 > Uni1 > Uni2
        [1, 2, 0, 3],  # s1: prefers Uni1 > Uni2 > Uni0 > Uni3
        [3, 0, 2, 1],  # s2: prefers Uni3 > Uni0 > Uni2 > Uni1
        [2, 1, 3, 0],  # s3: prefers Uni2 > Uni1 > Uni3 > Uni0
        [0, 1, 3, 2],  # s4: prefers Uni0 > Uni1 > Uni3 > Uni2
        [1, 3, 0, 2],  # s5: prefers Uni1 > Uni3 > Uni0 > Uni2
    ]

    [result,count] = universitiesChooseStudents(universities, students, universities_capacity)
    display_assignment_table(result, universities, count)
    print(result)
    # for u, candidates in enumerate(result):
    #     print(f"University {u} (capacity {universities_capacity[u]}): admitted students {candidates}")


    # for i in range(n):
    #     print(result[i], end=''if i!= n - 1 else '\n')

