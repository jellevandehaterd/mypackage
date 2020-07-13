class AnyArg(object):
    """AnyArg for wildcard mock assertions"""

    def __eq__(self, b: any):
        return True
