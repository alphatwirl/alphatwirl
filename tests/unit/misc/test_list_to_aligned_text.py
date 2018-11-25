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

def test_same_flost_to_str_conversion_between_python2_and_3():

    src = [
        ('component', 'htbin', 'njetbin', 'mhtbin', 'alphaT', 'n', 'nvar'),
        ('data1', 800, 2, 200, 0.41999999999999993, 2, 2),
        ('data1', 800, 2, 200, 0.43999999999999995, 2, 2),
        ('data1', 800, 2, 200, 0.45999999999999996, 0, 0),
        ('data1', 800, 2, 400, 0.41999999999999993, 1, 1),
        ('data1', 800, 2, 400, 0.43999999999999995, 0, 0),
        ('data1', 800, 2, 600, 0.41999999999999993, 0, 0),
        ('data1', 800, 2, 600,                0.54, 1, 1),
        ('data1', 800, 2, 600,                0.56, 0, 0),
        ('data1', 800, 3, 200,  0.3999999999999999, 1, 1),
    ]

    actual = list_to_aligned_text(src)

    expected = """\
 component htbin njetbin mhtbin alphaT n nvar
     data1   800       2    200   0.42 2    2
     data1   800       2    200   0.44 2    2
     data1   800       2    200   0.46 0    0
     data1   800       2    400   0.42 1    1
     data1   800       2    400   0.44 0    0
     data1   800       2    600   0.42 0    0
     data1   800       2    600   0.54 1    1
     data1   800       2    600   0.56 0    0
     data1   800       3    200    0.4 1    1
"""

    assert expected == actual

def test_same_flost_to_str_conversion_between_python2_and_3_part2():

    src = [
        ('component', 'met', 'n', 'nvar'),
        ('data1', 158.48931924611142, 16, 16),
        ('data1', 199.52623149688807, 33, 33),
        ('data1', 251.18864315095823, 43, 43),
        ('data1', 316.22776601683825, 33, 33),
        ('data1',  398.1071705534977, 25, 25),
        ('data1', 501.18723362727303, 15, 15),
        ('data1',  630.9573444801943,  7,  7),
        ('data1',   794.328234724283,  3,  3),
        ('data1',  1000.000000000002,  1,  1),
        ('data1',   1258.92541179417,  1,  1),
        ('data1', 1584.8931924611175,  0,  0),
    ]

    actual = list_to_aligned_text(src)

    expected = """\
 component           met  n nvar
     data1 158.489319246 16   16
     data1 199.526231497 33   33
     data1 251.188643151 43   43
     data1 316.227766017 33   33
     data1 398.107170553 25   25
     data1 501.187233627 15   15
     data1  630.95734448  7    7
     data1 794.328234724  3    3
     data1          1000  1    1
     data1 1258.92541179  1    1
     data1 1584.89319246  0    0
"""

    assert expected == actual
##__________________________________________________________________||
