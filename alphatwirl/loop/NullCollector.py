# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class NullCollector:
    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def collect(self, *_, **__):
        pass

##__________________________________________________________________||
