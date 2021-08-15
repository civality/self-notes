def get_splits(edge, num_posts):
    N = len(edge)

    if N == 0:
        return [[0,0]]

    borders = list(range(0, N, num_posts))
    borders.append(N)
    splits = [borders[page:page+2] for page in range(0, len(borders)-1)]
    return splits


def get_pages(splits):
    pages = list(range(1, len(splits)+1))
    return pages


# Working draft # 1, assumed window size 2

def get_pagination(P, cur_page):

# First I did this during coding
    central_part_left = cur_page-2
    central_part_right = cur_page+2

    central_part = list(range(central_part_left, central_part_right+1))

    central_part_new = []
    for element in central_part:
        if element >=1 and element <= P:
            central_part_new.append(element)

# Second I did this during coding
    if cur_page >= 6:
        initial_part = [1, None]

    if cur_page == 5:
        initial_part = [1, 2]

    if cur_page == 4:
        initial_part = [1]

    if cur_page < 4:
        initial_part = []

# Third I did this during coding
    if cur_page + 2 < P - 2:
        last_part = [None, P]

    if cur_page + 2 == P - 2:
        last_part = [P-1, P]

    if cur_page + 2 == P - 1:
        last_part = [P]

    if cur_page + 2 >= P:
        last_part = []

    return initial_part + central_part_new + last_part

# Working draft # 2, less code, harder to read, assumed window size 2

def get_pagination(P, cur_page):

    # First I did this during coding

    central_part_left = max(1, cur_page - 2)
    central_part_right = min(P, cur_page+2)
    central_part = list(range(central_part_left, central_part_right+1))

    # Second I did this during coding
    if cur_page >= 6:
        initial_part = [1, None]
    else:
        initial_part = list(range(1, cur_page - 2))

    # Third I did this during coding
    if cur_page < P - 4:
        last_part = [None, P]
    else: 
        last_part = list(range(cur_page + 3, P + 1))
    
    return initial_part + central_part + last_part

# Working draft # 3, parametrized left/right window size next to current_page

def get_pagination(P, cur_page, w):

    # First I did this during coding

    central_part_left = max(1, cur_page - w)
    central_part_right = min(P, cur_page + w)

    central_part = list(range(central_part_left, central_part_right+1))
    
    # Second I did this during coding
    
    if cur_page - w > 3:
        initial_part = [1, None]
    else:
        initial_part = list(range(1, cur_page - w))

    # Third I did this during coding
    
    if cur_page + w < P - 2:
        last_part = [None, P]
    else:
        last_part = list(range(cur_page + w + 1, P+1))

    return initial_part + central_part + last_part

for cur_page in range(1, 21):
    oldp = get_pagination_old(20, cur_page) #change any draft methods name to this for comparing
    newp = get_pagination(20, cur_page)
    
    print(cur_page, newp)
    assert oldp == newp



# Note: max(1, cur_page - w)  guarantees that the experssion can be minimum 1
# Note: min(P, cur_page + w)  guarantees that the experssion can be maximum P
