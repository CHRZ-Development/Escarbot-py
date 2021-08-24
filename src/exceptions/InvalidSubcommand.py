
class InvalidSubcommand(Exception):
    def __init__(self,subcommand_invalid):
        message = f"This subcommand `{subcommand_invalid}` is not exist !\nPlease look the Wiki (Check bot profile) or execute this command: `!help`"
        super().__init__(message)
