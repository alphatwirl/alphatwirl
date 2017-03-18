# Tai Sakuma <tai.sakuma@cern.ch>

from .quote_string import quote_string

##__________________________________________________________________||
def listToAlignedText(src, formatDict = None):

        # e.g.,
        # src = [
        #     ('component', 'v1', 'nvar', 'n'),
        #     ('data1',  100, 6.0,   40),
        #     ('data1',    2, 9.0, 3.3),
        #     ('data1', 3124, 3.0, 0.0000001),
        #     ('data2',  333, 6.0, 300909234),
        #     ('data2',   11, 2.0, 323432.2234),
        # ]

        if not src: return '' # src = [ ]
        if not src[0]: return '' # e.g., src = [(), (), ()]

        transposed = [[r[i] for r in src] for i in range(len(src[0]))]
        # e.g.,
        # transposed = [
        #     ['component', 'data1', 'data1', 'data1', 'data2', 'data2'],
        #     ['v1', 100, 2, 3124, 333, 11],
        #     ['nvar', 6.0, 9.0, 3.0, 6.0, 2.0],
        #     ['n', 40, 3.3, 1e-07, 300909234, 323432.2234],
        #     ]

        transposed = [[int(e) if isinstance(e, float) and e.is_integer() else e for e in r] for r in transposed]
        transposed = [[str(e) for e in r] for r in transposed]

        transposed = [[quote_string(e) for e in r] for r in transposed]

        columnWidths = [max([len(e) for e in r]) for r in transposed]
        # e.g., columnWidths = [9, 2, 4, 1]

        formatList = ['{:>' + str(e) + 's}' for e in columnWidths]
        # e.g., formatList = ['{:>9s}', '{:>4s}', '{:>4s}', '{:>11s}']

        if formatDict is not None:
                # e.g., formatDict = {'n': '{}'}

                columnNames = src[0]
                # e.g., columnNames = ('component', 'v1', 'nvar', 'n')

                formatDict0 = dict(zip(columnNames, formatList))
                # e.g., formatDict0 = {'component':'{:>9s}', 'v1':'{:>4s}', 'nvar':'{:>4s}', 'n':'{:>11s}'}

                formatDict0.update(formatDict)
                # e.g., formatDict0 = {'component':'{:>9s}', 'v1':'{:>4s}', 'nvar':'{:>4s}', 'n':'{}'}

                formatList = [formatDict0[c] for c in columnNames]
                # e.g., formatList = ['{:>9s}', '{:>4s}', '{:>4s}', '{}']

        format = " " + " ".join(formatList)
        # e.g., format = "{:>9s} {:>4s} {:>4s} {:>11s}"

        ret = "\n".join([format.format(*row) for row in zip(*transposed)]) + "\n"
        # example ret
        # component   v1 nvar           n
        #     data1  100    6          40
        #     data1    2    9         3.3
        #     data1 3124    3       1e-07
        #     data2  333    6   300909234
        #     data2   11    2 323432.2234

        return ret

##__________________________________________________________________||
