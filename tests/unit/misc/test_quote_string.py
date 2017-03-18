import unittest

from alphatwirl import quote_string

##__________________________________________________________________||
class TestQuoteString(unittest.TestCase):

    def test_one(self):

        text = 'AAA'
        expected = 'AAA'
        actual = quote_string(text)
        self.assertEqual(expected, actual)

    def test_empty(self):

        text = ''
        expected = '""'
        actual = quote_string(text)
        self.assertEqual(expected, actual)

    def test_space(self):

        text = 'AA A' # space in text
        expected = '"AA A"' # double quoted
        actual = quote_string(text)
        self.assertEqual(expected, actual)

        text = ' AAA' # space at the beginning
        expected = '" AAA"' # double quoted
        actual = quote_string(text)
        self.assertEqual(expected, actual)

        text = 'AAA ' # space at the end
        expected = '"AAA "' # double quoted
        actual = quote_string(text)
        self.assertEqual(expected, actual)

    def test_quoted(self):

        text = '"AAA"' # already double quoted
        expected = r'"\"AAA\""' # escaped and double quoted
        actual = quote_string(text)
        self.assertEqual(expected, actual)

        text = '"AA A"' #
        expected = r'"\"AA A\""' #
        actual = quote_string(text)
        self.assertEqual(expected, actual)

        text = 'AA "ab cde" BB' #
        expected = r'"AA \"ab cde\" BB"' #
        actual = quote_string(text)
        self.assertEqual(expected, actual)

##__________________________________________________________________||
