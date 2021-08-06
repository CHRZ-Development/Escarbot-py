from discord import Game


class Activities(Game):

	def __init__(self,version,msg="✅ 𝘾𝙃𝙍𝙕 𝘋𝘦𝘷𝘦𝘭𝘰𝘱𝘮𝘦𝘯𝘵'𝘴 𝘉𝘰𝘵"):
		Game.__init__(self,name=f"{msg} | {version}")
