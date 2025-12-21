# sorting by value [bins], then price if the bins are the same value
def merge_sort(lst, key_func=lambda x: x, reverse=False):
    # sorting transaction in ordinal order (ascending), then by price (descending order)
    
    if len(lst) <= 1:
        return lst
    
    # splitting the list into two halves
    mid = len(lst) // 2
    left = merge_sort(lst[:mid], key_func, reverse)
    right = merge_sort(lst[mid:], key_func, reverse)
    return _merge(left, right, key_func, reverse) 

def _merge(left, right, key_func, reverse):
    merged = []
    i = j = 0
    cmp = (lambda a, b: a > b) if not reverse else (lambda a, b: a < b)

    while i < len(left) and j < len(right):

        if cmp(key_func(left[i]), key_func(right[j])):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
        
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged