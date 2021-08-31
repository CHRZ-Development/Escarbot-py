
class InvalidSubcommand(Exception):
    def __init__(self,subcommand_invalid):
        self.message = f"""❗ This subcommand `{subcommand_invalid}` is not exist !
        Please look the [wiki](https://github.com/NaulaN/Escarbot-py/wiki/Commandes) or execute this command -> `!help` or `/help` for a fast documentation."""
        super().__init__(self.message)
