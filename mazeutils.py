'''
In general:
    str2nested_list(nested_list2str(X)) == nested_list2str(str2nested_list(X))
'''

def str2nested_list(s, delim='\n'):
    return [list(e) for e in s.split(delim)]


def nested_list2str(l, delim='\n'):
    p = ""
    for row in l:
        p += "".join([str(e) for e in row]) + delim
    return p
