from requests import Session

class Consistent:
	def __init__(self,panel_url:str,session:Session) -> None:
		self.__panel_url = panel_url.strip("/")
		self.__session:Session = session
	@property
	def panel_url(self) -> str:
		return self.__panel_url
	@property
	def session(self) -> Session:
		return self.__session
	@session.setter
	def session(self,new_obj:Session) -> None:
		self.__session = new_obj