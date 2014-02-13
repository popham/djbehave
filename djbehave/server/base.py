from subbehave.command import Command

class Db(Command):

    """
    Instances of `Db` take a `TestServerProxy` as their command argument.

    """

    def __call__(self, return_queue, proxy):
        raise NotImplementedError
