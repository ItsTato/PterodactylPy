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

class RequestFailed(PterodactylException):
	# Used for when we don't have an exception based on the panel's ones
	pass

# Exceptions based on actual errors the panel may return.
# If you know of any missing exceptions here, please just add it and submit a pull request!

class NotFoundHttpException(PterodactylException):
	pass

class ValidationException(PterodactylException):
	pass
