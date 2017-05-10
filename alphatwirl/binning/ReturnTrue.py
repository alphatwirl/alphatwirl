# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ReturnTrue(object):
    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def __call__(self, *_, **__):
        return True

##__________________________________________________________________||
