# Tai Sakuma <tai.sakuma@gmail.com>
import numpy as np
import collections

import pytest

from alphatwirl.summary.convert import key_vals_dict_to_tuple_list

##__________________________________________________________________||
@pytest.mark.parametrize(
    'key_vals_dict, tuple_list, kwargs', [
        pytest.param(
            collections.OrderedDict((
                ((1, 10), [(4, 6)]),
                ((2, 11), [ ]),
                ((3, 12), [(2, 3), (5, 7)]),
            )),
            [
                (1, 10, 4, 6),
                (3, 12, 2, 3),
                (3, 12, 5, 7),
            ],
            { },
            id='example'
        ),
        pytest.param({ }, [ ], { }, id='empty'),
        pytest.param(
            collections.OrderedDict((
                ((1, 10), [(4, 6, 2, 1)]),
                ((2, 11), [ ]),
                ((3, 12), [(2, 3, 4, 5), (5, 7)]),
                ((4, 13), [( ), ( )])
            )),
            [
                (1, 10, 4, 6, 2, 1),
                (3, 12, 2, 3, 4, 5),
                (3, 12, 5, 7, 0, 0),
                (4, 13, 0, 0, 0, 0),
                (4, 13, 0, 0, 0, 0),
            ],
            dict(fill=0),
            id='fill 0'
        ),
        pytest.param(
            collections.OrderedDict((
                ((1, 10), [np.array((4, 6))]),
                ((2, 11), [ ]),
                ((3, 12), [np.array((2, 3)), np.array((5, 7))]),
            )),
            [
                (1, 10, 4, 6),
                (3, 12, 2, 3),
                (3, 12, 5, 7),
            ],
            { },
            id='numpy'
        ),
        pytest.param(
            collections.OrderedDict((
                ((1, ), [(4, 6)]),
                (2, [ ]),
                (3, [(2, 3), (5, 7)]),
            )),
            [
                (1, 4, 6),
                (3, 2, 3),
                (3, 5, 7),
            ],
            { },
            id='key_not_tuple'
        ),
    ]
)
def test_convert(key_vals_dict, tuple_list, kwargs):
    assert tuple_list == key_vals_dict_to_tuple_list(key_vals_dict, **kwargs)

##__________________________________________________________________||
@pytest.mark.parametrize(
    'key_vals_dict, tuple_list', [
        pytest.param(
            collections.OrderedDict((
                ((1, 10), [(4, 6, 2, 1)]),
                ((2, 11), [ ]),
                ((3, 12), [(2, 3, 4, 5), (5, 7)]),
                ((4, 13), [( ), ( )])
            )),
            [
                (1, 10, 4, 6, 2, 1),
                (3, 12, 2, 3, 4, 5),
                (3, 12, 5, 7, float('nan'), float('nan')),
                (4, 13, float('nan'), float('nan'), float('nan'), float('nan')),
                (4, 13, float('nan'), float('nan'), float('nan'), float('nan')),
            ],
            id='fill_nan'),
    ]
)
@pytest.mark.skip(reason="nan == nan is False in python")
def test_convert_fill_nan(key_vals_dict, tuple_list):
    # note: nan == nan is False in python
    assert tuple_list == key_vals_dict_to_tuple_list(key_vals_dict)

##__________________________________________________________________||
