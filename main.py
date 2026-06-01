from typing import List

# Check if woman prefers m over current partner m1
def prefers(women: List[List[int]], w: int, m: int, m1: int) -> bool:
    for i in range(len(women[w])):
        if women[w][i] == m:
            return True
        if women[w][i] == m1:
            return False
    return False
    

def stableMarriage(men: List[List[int]], women: List[List[int]]) -> List[int]:
    n = len(men)

    # women's current partners
    w_partner = [-1] * n  
    
    # man's current partners
    m_partner = [-1] * n  
    
    # next proposal index
    next_proposal = [0] * n  
    
    # Free Men
    free_man = [True] * n  

    free_count = n

    nb_iterations = 0

    while free_count > 0:
        m = next((m for m in range(n) if free_man[m]), None)

        w = men[m][next_proposal[m]]
        next_proposal[m] += 1

        # If w is free
        if w_partner[w] == -1:
            w_partner[w] = m
            m_partner[m] = w
            free_man[m] = False
            free_count -= 1
        else:
            m1 = w_partner[w]

            # If w prefers m over current partner
            if prefers(women, w, m, m1):
                w_partner[w] = m
                m_partner[m] = w

                free_man[m] = False
                free_man[m1] = True
        nb_iterations=nb_iterations+1

    print(nb_iterations)
    return m_partner

if __name__ == '__main__':
    n = 3

    men = [
        [1, 0, 2],
        [2, 1, 0],
        [0, 2, 1]
    ]

    women = [
        [1, 0, 2],
        [2, 1, 0],
        [0, 2, 1]
    ]

    result = stableMarriage(men, women)

    for i in range(n):
        print(result[i], end=''if i!= n - 1 else '\n')