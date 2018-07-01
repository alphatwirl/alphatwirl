# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.summary import BackrefMultipleArrayReader

##__________________________________________________________________||
@pytest.mark.parametrize('kwargs', (
    dict(arrays=[[ ] ], idxs_conf=( )),
    dict(arrays=[[ ], [ ]], idxs_conf=(2, 3, 4)),
    dict(arrays=[[ ], [ ]], idxs_conf=(2, 3), backref_idxs=(None, None, 1)),
))
def test_init_raise(kwargs):
    with pytest.raises(ValueError):
        BackrefMultipleArrayReader(**kwargs)

@pytest.mark.parametrize('kwargs', (
    dict(arrays=[[ ], [ ]], idxs_conf=(1, 2), backref_idxs=None),
))
def test_init(kwargs):
    BackrefMultipleArrayReader(**kwargs)

##__________________________________________________________________||
params_without_backref = (
    pytest.param([ ], ( ), [
        dict(arrays=[ ], expected=(( ), )),
    ], id='empty'),
    pytest.param([[ ]], (0, ), [
        dict(arrays=[[12, 13, 14]], expected=((12, ), )),
        dict(arrays=[[ ]], expected=( ))
    ], id='1-element'),
    pytest.param([[ ], [ ], [ ]], (1, 0, 2), [
        dict(
            arrays=[
                [12, 13, 14],
                [105],
                [33, 35, 37],
            ],
            expected=((13, 105, 37), )
        ),
        dict(
            arrays=[
                [12], # <- out of range
                [105],
                [33, 35, 37],
            ],
            expected=( )
        ),
        dict(
            arrays=[
                [12, 13, 14],
                [ ], # <- out of range
                [33, 35, 37],
            ],
            expected=( )
        ),
        dict(
            arrays=[
                [12, 13, 14],
                [105],
                [33, 35], # <- out of range
            ],
            expected=( )
        ),
    ], id='3-element'),
    pytest.param([[ ]], ('*', ), [
        dict(arrays=[[ ]], expected=( )),
        dict(arrays=[[12]], expected=((12, ), )),
        dict(arrays=[[12, 13]], expected=((12, ), (13, ))),
        dict(arrays=[[12, 13, 14]], expected=((12, ), (13, ), (14, ))),
    ], id='1-wildcard'),
    pytest.param([[ ], [ ]], (1, '*'), [
        dict(arrays=[[ ], [ ]], expected=( )),
        dict(arrays=[[203, 204, 205], [ ]], expected=( )),
        dict(arrays=[[203, 204, 205], [12]], expected=((204, 12), )),
        dict(arrays=[[203, 204, 205], [12, 13, 14]], expected=((204, 12), (204, 13), (204, 14))),
        dict(arrays=[[ ], [12, 13, 14]], expected=()),
    ], id='1-index-1-wildcard'),
    pytest.param([[ ], [ ]], ('*', '*'), [
        dict(arrays=[[ ], [ ]], expected=( )),
        dict(arrays=[[12], [ ]], expected=( )),
        dict(arrays=[[12, 13], [ ]], expected=( )),
        dict(arrays=[[ ], [104]], expected=( )),
        dict(arrays=[[ ], [104, 105]], expected=( )),
        dict(arrays=[[12], [104]], expected=((12, 104), )),
        dict(arrays=[[12, 13], [104]], expected=((12, 104), (13, 104))),
        dict(arrays=[[12, 13, 14], [104]], expected=((12, 104), (13, 104), (14, 104))),
        dict(
            arrays=[[12, 13, 14], [104, 105]],
            expected=((12, 104), (12, 105), (13, 104), (13, 105), (14, 104), (14, 105))
        ),
        dict(
            arrays=[[12, 13, 14], [104, 105, 106]],
            expected=((12, 104), (12, 105), (12, 106), (13, 104), (13, 105), (13, 106), (14, 104), (14, 105), (14, 106))
        ),
    ], id='2-wildcards'),
    pytest.param([[ ], [ ], [ ]], ('*', '*', '*'), [
        dict(arrays=[[ ], [ ], [ ]], expected=( )),
        dict(arrays=[[12, 13], [ ], [ ]], expected=( )),
        dict(arrays=[[ ], [104], [ ]], expected=( )),
        dict(arrays=[[ ], [104], [1001, 1002, 1003]], expected=( )),
        dict(
            arrays=[[12, 13, 14], [104, 105], [1001, 1002, 1003]],
            expected=(
                (12, 104, 1001), (12, 104, 1002), (12, 104, 1003),
                (12, 105, 1001), (12, 105, 1002), (12, 105, 1003),
                (13, 104, 1001), (13, 104, 1002), (13, 104, 1003),
                (13, 105, 1001), (13, 105, 1002), (13, 105, 1003),
                (14, 104, 1001), (14, 104, 1002), (14, 104, 1003),
                (14, 105, 1001), (14, 105, 1002), (14, 105, 1003),
            )
        ),
    ], id='3-wildcards'),
    pytest.param([[ ], [ ], [ ], [ ], [ ]], (1, '*', '*', 2, '*'), [
        dict(arrays=[[ ], [ ], [ ], [ ], [ ]], expected=( )),
        dict(
            arrays=[[55, 66, 77], [12, 13, 14], [104, 105], [222, 333, 444, 555], [1001, 1002, 1003]],
            expected=(
                (66, 12, 104, 444, 1001), (66, 12, 104, 444, 1002), (66, 12, 104, 444, 1003),
                (66, 12, 105, 444, 1001), (66, 12, 105, 444, 1002), (66, 12, 105, 444, 1003),
                (66, 13, 104, 444, 1001), (66, 13, 104, 444, 1002), (66, 13, 104, 444, 1003),
                (66, 13, 105, 444, 1001), (66, 13, 105, 444, 1002), (66, 13, 105, 444, 1003),
                (66, 14, 104, 444, 1001), (66, 14, 104, 444, 1002), (66, 14, 104, 444, 1003),
                (66, 14, 105, 444, 1001), (66, 14, 105, 444, 1002), (66, 14, 105, 444, 1003),
            )
        ),
    ], id='2-indices--wildcards'),
)

@pytest.mark.parametrize('arrays, idxs_conf, data', params_without_backref)
def test_read_without_backref(arrays, idxs_conf, data):
    obj = BackrefMultipleArrayReader(
        arrays=arrays, idxs_conf=idxs_conf)
    for d in data:
        arrays_content = d['arrays']
        expected = d['expected']
        for a, c in zip(arrays, arrays_content):
            a[:] = c
        assert expected == obj.read()

@pytest.mark.skip(reason='for optimizing for speed')
@pytest.mark.parametrize('arrays, idxs_conf, data', params_without_backref[-1:])
def test_read_without_backref_measure_time(arrays, idxs_conf, data):
    from datetime import datetime
    tick = datetime.now()
    obj = BackrefMultipleArrayReader(
        arrays=arrays, idxs_conf=idxs_conf)
    for d in data:
        arrays_content = d['arrays']
        expected = d['expected']
        for a, c in zip(arrays, arrays_content):
            a[:] = c
            for i in range(100000):
                obj.read()
    tock = datetime.now()
    diff = tock - tick
    print('time: {}'.format(diff.total_seconds()))

##__________________________________________________________________||
params_backref = (
    pytest.param([[ ], [ ]], ('*', None), [None, 0], [
        dict(arrays=[[ ], [ ]], expected=( )),
        dict(arrays=[[12], [104]], expected=((12, 104), )),
        dict(arrays=[[12], [ ]], expected=( )),
        dict(arrays=[[ ], [104]], expected=( )),
        dict(arrays=[[12, 13], [104, 105]], expected=((12, 104), (13, 105))),
        dict(arrays=[[12, 13], [104]], expected=((12, 104), )),
        dict(arrays=[[12], [104, 105]], expected=((12, 104), )),
        dict(arrays=[[12, 13, 14], [104, 105, 106]], expected=((12, 104), (13, 105), (14, 106))),
        dict(arrays=[[ ], [104, 105, 106]], expected=( )),
        dict(arrays=[[12, 13, 14], [104, 105]], expected=((12, 104), (13, 105))),
    ], id='1-wildcard-1-backref'),
    pytest.param(
        [[ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ]],
        (0, '*', None, '*', None, None, None, None),
        [None, None, 1, None, 3, 1, 1, 3],
        [
            dict(
                arrays=[
                    [1001],
                    [12,  13,  14,  15],
                    [104, 105, 106, 107],
                    [51, 52], # <- shorter
                    [84, 85, 86],
                    [403, 404, 405], # <- shorter
                    [207, 208, 209, 210],
                    [91, 92, 93],
                ],
                expected=(
                    (1001, 12, 104, 51, 84, 403, 207, 91),
                    (1001, 12, 104, 52, 85, 403, 207, 92),
                    (1001, 13, 105, 51, 84, 404, 208, 91),
                    (1001, 13, 105, 52, 85, 404, 208, 92),
                    (1001, 14, 106, 51, 84, 405, 209, 91),
                    (1001, 14, 106, 52, 85, 405, 209, 92)
                )),
        ], id='1-index-2-wildcards-2-backrefs'
    ),
)

@pytest.mark.parametrize('arrays, idxs_conf, backref_idxs, data', params_backref)
def test_read_backref(arrays, idxs_conf, backref_idxs, data):
    obj = BackrefMultipleArrayReader(
        arrays=arrays, idxs_conf=idxs_conf, backref_idxs=backref_idxs)
    for d in data:
        arrays_content = d['arrays']
        expected = d['expected']
        for a, c in zip(arrays, arrays_content):
            a[:] = c
        assert expected == obj.read()

@pytest.mark.skip(reason='for optimizing for speed')
@pytest.mark.parametrize('arrays, idxs_conf, backref_idxs, data', params_backref[-1:])
def test_read_backref_measure_time(arrays, idxs_conf, backref_idxs, data):
    import cProfile, pstats
    from datetime import datetime
    pr = cProfile.Profile()
    pr.enable()
    tick = datetime.now()
    obj = BackrefMultipleArrayReader(
        arrays=arrays, idxs_conf=idxs_conf, backref_idxs=backref_idxs)
    for d in data:
        arrays_content = d['arrays']
        expected = d['expected']
        for a, c in zip(arrays, arrays_content):
            a[:] = c
            for i in range(30000):
                obj.read()
    tock = datetime.now()
    pr.disable()
    diff = tock - tick
    print('time: {}'.format(diff.total_seconds()))
    sortby = 'cumulative'
    from io import StringIO, BytesIO
    try:
        s = StringIO()
        pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby).print_stats()
    except TypeError:
        s = BytesIO()
        pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby).print_stats()
    print(s.getvalue())

##__________________________________________________________________||
