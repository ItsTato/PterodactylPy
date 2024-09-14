class PterodactylException(Exception):
	def __init__(self,detail:str,status:int):
		self.__detail:str = detail
		self.__status:int = status
		self.__message:str = f"[{self.__status}] {self.__detail}"
		super().__init__(self.__message)
	@property
	def detail(self) -> str:
		return self.__detail
	@property
	def status(self) -> int:
		return self.__status
	@property
	def message(self) -> str:
		return self.__message

class NotFoundHttpException(PterodactylException):
	def __init__(self,detail:str,status:int):
		super().__init__(detail,status)

class ValidationException(PterodactylException):
	def __init__(self,detail:str,status:int):
		super().__init__(detail,status)
