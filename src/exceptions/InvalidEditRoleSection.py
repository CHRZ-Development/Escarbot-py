
class InvalidEditRoleSection(Exception):
    def __init__(self,section):
        self.message = f"""
        ❗ This settings "{section}" isn't exist !
        You can see in the [wiki](https://github.com/NaulaN/Escarbot-py/wiki/Commandes#edit-role) what is available as be can edited.
        """
        super().__init__(self.message)
