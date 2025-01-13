class PterodactylException(Exception):
	def __init__(self,detail:str,status:int):
		self.detail:str = detail
		self.status:int = status
		self.message:str = f"[{self.status}] {self.detail}"
		super().__init__(self.message)

class RequestFailed(PterodactylException):
	# Used for when we don't have an exception based on the panel's ones
	pass

# Exceptions based on actual errors the panel may return.
# If you know of any missing exceptions here, please just add it and submit a pull request!

class NotFoundHttpException(PterodactylException):
	pass

class ValidationException(PterodactylException):
	pass
