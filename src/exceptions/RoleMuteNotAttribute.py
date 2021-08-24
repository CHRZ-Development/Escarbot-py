
class RoleMuteNotAttribute(Exception):
    """ Exception raised for errors in the not have mute role attributed. """
    def __init__(self):
        self.message = f"The **role `mute`** is **not attribute** !"
        super().__init__(self.message)
