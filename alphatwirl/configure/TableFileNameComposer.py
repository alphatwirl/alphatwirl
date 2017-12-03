# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class TableFileNameComposer(object):
    """Compose a name of a file to store the table from the column names
       and indices.

    For example, if column names are 'var1', 'var2', and 'var3' and
    indices are 1, None and 2, the file name will be
    'tbl_n_component.var1-1.var2.var3-2.txt'

    """
    def __init__(self,
                 default_prefix = 'tbl_n',
                 default_suffix = 'txt',
                 default_var_separator = '.',
                 default_idx_separator = '-',
    ):
        self.default_prefix = default_prefix
        self.default_suffix = default_suffix
        self.default_var_separator = default_var_separator
        self.default_idx_separator = default_idx_separator

    def __call__(self, columnNames, indices = None,
                 prefix = None, suffix = None,
                 var_separator = None, idx_separator = None
    ):
        prefix = self.default_prefix if prefix is None else prefix
        suffix = self.default_suffix if suffix is None else suffix
        var_separator = self.default_var_separator if var_separator is None else var_separator
        idx_separator = self.default_idx_separator if idx_separator is None else idx_separator

        if not columnNames:
            return prefix + '.' + suffix # e.g. "tbl_n_component.txt"

        if indices is None:
            colidxs = columnNames
            # e.g., ('var1', 'var2', 'var3'),

            middle = var_separator.join(colidxs)
            # e.g., 'var1.var2.var3'

            ret = prefix + var_separator + middle + '.' + suffix
            # e.g., 'tbl_n_component.var1.var2.var3.txt'

            return ret

        # e.g.,
        # columnNames = ('var1', 'var2', 'var3', 'var4', 'var5'),
        # indices = (1, None, '*', '(*)', '\\1')

        idx_str = indices
        # e.g., (1, None, '*', '(*)', '\\1')

        idx_str = ['w' if i == '*' else i for i in idx_str]
        # e..g, [1, None, 'w', '(*)', '\\1']

        idx_str = ['wp' if i == '(*)' else i for i in idx_str]
        # e.g., [1, None, 'w', 'wp', '\\1']

        idx_str = ['b{}'.format(i[1:]) if isinstance(i, str) and i.startswith('\\') else i for i in idx_str]
        # e.g., [1, None, 'w', 'wp', 'b1']

        idx_str = ['' if i is None else '{}{}'.format(idx_separator, i) for i in idx_str]
        # e.g., ['-1', '', '-w', '-wp', '-b1']

        colidxs = [n + i for n, i in zip(columnNames, idx_str)]
        # e.g., ['var1-1', 'var2', 'var3-w', 'var4-wp', 'var5-b1']

        middle = var_separator.join(colidxs)
        # e.g., 'var1-1.var2.var3-w.var4-wp.var5-b1'

        ret =  prefix + var_separator + middle + '.' + suffix
        # e.g., tbl_n_component.var1-1.var2.var3-w.var4-wp.var5-b1.txt

        return ret

##__________________________________________________________________||
