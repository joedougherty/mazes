from mazeutils import str2nested_list, nested_list2str


def test_str_expansion_ints():
    s = '12345'
    assert str2nested_list(s) == [['1', '2', '3', '4', '5']]


def test_str_expansion_empty():
    s = ''
    assert str2nested_list(s) == [[]]


def test_str_expansion_tiny_docs():
    tiny = ''' 
######
#    #
# # ##
######
'''.strip()
    exp = [
        ['#', '#', '#', '#', '#', '#'],
        ['#', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', '#', ' ', '#', '#'],
        ['#', '#', '#', '#', '#', '#']
    ] 
    assert str2nested_list(tiny) == exp

