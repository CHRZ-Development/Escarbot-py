
class RoleMuteNotAttribute(Exception):
    """ Exception raised for errors in the not have mute role attributed. """
    def __init__(self):
        self.message = f"""
        > The **role `mute`** is **not attribute** !
        Please, use this command `!attribute role` (You can see this command in the [wiki](https://github.com/NaulaN/Escarbot-py/wiki/Commandes#attribute-role))
        """
        super().__init__(self.message)
