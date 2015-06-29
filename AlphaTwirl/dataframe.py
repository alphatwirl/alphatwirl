
## class Dataframe(object):
##     """
## 
##     """
##     def __init__(self):
##         self.keynames
##         self.valnames
##         self.data = { }

class Dataframe(dict):
    """

    {
        ('data1', 1): [4.0, 6.0],
        ('data1', 2): [3.0, 9.0],
        ('data1', 3): [2.0, 3.0],
    }

    """
    def __init__(self, keynames = None, valnames = None, data = { }):
        self.keynames = keynames
        self.valnames = valnames
        super(Dataframe, self).__init__(data)
