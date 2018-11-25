# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl import list_to_aligned_text

##__________________________________________________________________||
def test_one():

    src = [
        ('component', 'v1', 'nvar', 'n'),
        ('data1',  100, 6.0,   40),
        ('data1',    2, 9.0, 3.3),
        ('data1', 3124, 3.0, 0.0000001),
        ('data2',  333, 6.0, 300909234),
        ('data2',   11, 2.0, 323432.2234),
    ]

    actual = list_to_aligned_text(src)

    expected = """\
 component   v1 nvar           n
     data1  100    6          40
     data1    2    9         3.3
     data1 3124    3       1e-07
     data2  333    6   300909234
     data2   11    2 323432.2234
"""

    assert expected == actual

def test_quote():

    src = [
        ('component', 'v1', 'v2'),
        ('data1',      100, ''),
        ('data1',        2, 'abc def'),
        ('data1',     3124, '"AAA"'),
        ('data2',      333, ' abc "de fg" hij '),
        ('data2',       11, 'xyz'),
    ]

    actual = list_to_aligned_text(src)

    expected = r""" component   v1                    v2
     data1  100                    ""
     data1    2             "abc def"
     data1 3124             "\"AAA\""
     data2  333 " abc \"de fg\" hij "
     data2   11                   xyz
"""

    assert expected == actual

def test_formatDict_01():

    src = [
        ('component', 'v1', 'nvar', 'n'),
        ('data1',  100, 6.0,   40),
        ('data1',    2, 9.0, 3.3),
        ('data1', 3124, 3.0, 0.0000001),
        ('data2',  333, 6.0, 300909234),
        ('data2',   11, 2.0, 323432.2234),
    ]

    format_dict = dict(n = '{:.2f}')

    actual = list_to_aligned_text(src, format_dict)

    expected = """\
 component   v1 nvar            n
     data1  100    6        40.00
     data1    2    9         3.30
     data1 3124    3         0.00
     data2  333    6 300909234.00
     data2   11    2    323432.22
"""

    assert expected == actual

def test_formatDict_left_align_last_column():

    src = [
        ('component', 'v1', 'nvar', 'n'),
        ('data1',  100, 6.0,   40),
        ('data1',    2, 9.0, 3.3),
        ('data1', 3124, 3.0, 0.0000001),
        ('data2',  333, 6.0, 300909234),
        ('data2',   11, 2.0, 323432.2234),
    ]

    format_dict = dict(n = '{}')

    actual = list_to_aligned_text(src, format_dict, left_align_last_column = True)

    expected = """\
 component   v1 nvar n
     data1  100    6 40
     data1    2    9 3.3
     data1 3124    3 1e-07
     data2  333    6 300909234
     data2   11    2 323432.2234
"""

    assert expected == actual

def test_headonly():

    src = [
        ('component', 'v1', 'nvar', 'n'),
    ]

    actual = list_to_aligned_text(src)

    expected = " component v1 nvar n\n"
    assert expected == actual

def test_empty_one():
    src = [ ]
    actual = list_to_aligned_text(src)
    expected = ""
    assert expected == actual

def test_empty_two():
    src = [()]
    actual = list_to_aligned_text(src)
    expected = ""
    assert expected == actual

def test_empty_three():
    src = [(), (), ()]
    actual = list_to_aligned_text(src)
    expected = ""
    assert expected == actual

##__________________________________________________________________||
