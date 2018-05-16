# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class Branch(object):
    """This class encloses an array.array object, which is typically used
    to set the address of a branch of a ROOT TTree. This class is
    useful for fast access to contents of TTree.

    While TTree can hold many types of data, including objects of user
    defined classes, this class can be used only for objects of simple
    types, such as Int_t, Double_t, and arrays of simple types.


    Examples
    --------
    Suppose jet_pt is an instance of this class and the corresponding
    object in TTree is an array.

    >>> len(jet_pt)
    3

    >>> [v for v in jet_pt]
    [127.16558074951172, 68.16969299316406, 53.75463104248047]

    When the corresponding object in TTree is not an array but a
    simple type, the length is 1 and the only element is the value.

    >>> len(mht)
    1

    >>> mht[0]
    73.7677


    """


    def __init__(self, name, array, countarray):
        self.name = name
        self.array = array
        self.countarray = countarray

    def __repr__(self):
        return '{}(name={!r}, array={!r}, countarray={!r})'.format(
            self.__class__.__name__,
            self.name,
            self.array,
            self.countarray
        )

    def __getitem__(self, i):
        if self.countarray is None and 0 != i:
            raise IndexError('the index should be zero for this branch: {}[{}]'.format(self.name, i))
        if self.countarray is not None and i >= self.countarray[0]:
            raise IndexError('the index is out of range: {}[{}]'.format(self.name, i))
        return self.array[i]

    def __len__(self):
        if self.countarray is None: return 1
        return self.countarray[0]

##__________________________________________________________________||
