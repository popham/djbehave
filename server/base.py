from subbehave.command import Command

class Db(Command):
    def __call__(self, return_queue, proxy):
        raise NotImplementedError
