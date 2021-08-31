
class NoRoleAttribute(Exception):
    """ Exception raised for errors in the not have role attributed. """
    def __init__(self):
        self.message = """❗ You have not role attribute ! Please use `!attribute role`"""
        super().__init__(self.message)
