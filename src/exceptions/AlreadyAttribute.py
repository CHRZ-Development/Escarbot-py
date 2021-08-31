
class AlreadyAttribute(Exception):
    def __init__(self,what):
        self.message = f"""
        Your are already attribute this "{what}" !
        Tips: `!get roles "{what}"`
        """
        super().__init__(self.message)
