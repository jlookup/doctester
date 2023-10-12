"""General, useful functions."""


def is_rjust(lst:list) -> bool:
    """checks if all elements of a list are right justified
    
    Examples:
        >>> l1 = ['   2', '3525', ' 233']
        >>> is_rjust(l1)
        True

        >>> l2 = ['2345', '3456', '4567']
        >>> is_rjust(l2)
        True

        >>> l3 = ['2345', '3456', '4500']
        >>> is_rjust(l3)
        True    

        >>> l4 = ['2345', '3456', '456700']
        >>> is_rjust(l4)
        False    

        >>> l5 = ['2345 ', '3456 ', '45670']
        >>> is_rjust(l5)
        False 

    """
    # naive version:
    # get max length of the elements of the list
    # check that all elements match that length 
    # check that no elements are left-padded
    # return True
    lengths = set(len(e) for e in lst)
    is_rjustified = (len(lengths) == 1 
                     and all((1 if e == e.rstrip()
                              else 0 for e in lst)))

    return is_rjustified


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    