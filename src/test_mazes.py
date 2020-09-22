from mazeutils import str2nested_list, nested_list2str
from classydemo import demo

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

def test_demo_works_one():
    assert demo.bfs((1,1),(1,5)) == False

def test_demo_works_two():
    assert demo.shortest_path((1,1),(1,4)) ==  [(1, 1), (1, 2), (1, 3), (1, 4)]
