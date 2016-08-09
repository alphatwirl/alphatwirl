# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class TableFileNameComposer(object):
    """Compose a name of a file to store the table from the column names
       and indices.


    For example, if column names are 'var1', 'var2', and 'var3' and
    indices are 1, None and 2, the file name will be
    'tbl_component_var1_1_var2_var3_2.txt'

    """
    def __init__(self, default_prefix = 'tbl_n_component', default_suffix = '.txt'):
        self.default_prefix = default_prefix
        self.default_suffix = default_suffix

    def __call__(self, columnNames, indices, prefix = None, suffix = None):
        prefix = self.default_prefix if prefix is None else prefix
        suffix = self.default_suffix if suffix is None else suffix

        # for example, if columnNames = ('var1', 'var2', 'var3') and indices = (1, None, 2),
        # l will be ['var1', '1', 'var2', 'var3', '2']
        if indices is not None:
            indices = [None if i == '*' else i for i in indices]
            indices = [None if i == '(*)' else i for i in indices]
            indices = [None if isinstance(i, basestring) and i.startswith('\\') else i for i in indices]
        l = columnNames if indices is None else [str(e) for sublist in zip(columnNames, indices) for e in sublist if e is not None]
        if l:
            ret = prefix + '_' + '_'.join(l) + suffix # e.g. "tbl_n_component_var1_1_var2_var3_2.txt"
        else:
            ret = prefix + suffix # e.g. "tbl_n_component.txt"
        return ret

##__________________________________________________________________||
