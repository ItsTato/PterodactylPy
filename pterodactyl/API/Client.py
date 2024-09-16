# Work into the Client API has not started.

from requests import Session

class Client:
	def __init__(self,panel_url:str,api_key:str) -> None:
		"""
		Creates a new session for the /api/client endpoint set.
		:param panel_url: URL to the panel.
		:param api_key: User API Key.
		"""

		# Init
		self.__panel_url:str = panel_url.strip("/")
		self.__session:Session = Session()
		headers:dict[str,str] = {
			"Authorization": f"Bearer {api_key}",
			"Accept": "application/json",
			"Content-Type": "application/json"
		}
		self.__session.headers.update(headers)

		# Subclasses
		self.Account:Client.__Account = self.__Account(self.__panel_url,self.__session)

	class __Account:
		def __init__(self,panel_url:str,session:Session) -> None:
			self.__panel_url:str = panel_url
			self.__session:Session = session

		# to-add: Server and Server/*
