
class ArgumentError(Exception):
    def __init__(self,args):
        self.message = f"""
        ❗ You are enter a wrong argument {args}
        please check the [wiki](https://github.com/NaulaN/Escarbot-py/wiki/Commandes)
        """
        super().__init__(self.message)
