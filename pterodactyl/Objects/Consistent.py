from requests import Session

class Consistent:
	def __init__(self,panel_url:str,session:Session) -> None:
		self.panel_url = panel_url.strip("/")
		self.session:Session = session