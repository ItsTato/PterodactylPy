from ..Objects import Consistent, TransformToObject
from ..Objects.Errors import RequestFailed
from ..Objects.Pterodactyl import User, Node

from json import dumps
from requests import Session, Response

class Application:
	def __init__(self,panel_url:str,api_key:str) -> None:
		"""
		Creates a new session for the /api/application endpoint set.
		:param panel_url: URL to the panel.
		:param api_key: Pterodactyl Application API Key.
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

		self.__cObj:Consistent = Consistent(self.__panel_url,self.__session)

		# Subclasses
		self.Users:Application.__Users = self.__Users(self.__cObj)
		self.Nodes:Application.__Nodes = self.__Nodes(self.__cObj)
		self.Locations:Application.__Locations = self.__Locations(self.__cObj)
		self.Servers:Application.__Servers = self.__Servers(self.__cObj)
		self.Nests:Application.__Nests = self.__Nests(self.__cObj)

	class __Users:
		def __init__(self,cObj:Consistent) -> None:
			self.__cObj:Consistent = cObj

		def get_users(self,list_all_pagination:bool=True,page:int=1) -> list[User]:
			if list_all_pagination:
				assert page == 1, "list_all_pagination means pages will not be used."

			users:list[User] = []

			req:Response = self.__cObj.session.get(f"{self.__cObj.panel_url}/api/application/users")
			if req.status_code != 200:
				TransformToObject(self.__cObj,req.json()) # If there's an error to deal with it, it will be raised. Otherwise, default "Get request fail!"
				raise RequestFailed("Unknown error!",req.status_code)

			req_json:dict = req.json()
			_ls:list = TransformToObject(self.__cObj,req_json)
			if not isinstance(_ls,list):
				raise Exception(f"Invalid request response!\n\nResponse: {dumps(req_json)}")
			for _u in _ls:
				users.append(TransformToObject(self.__cObj,_u))

			return users
		# Aliases
		list_users = get_users

		def get_user(self,user_id:int) -> User:
			"""
			Get a user based on their ID.
			:param user_id: The ID of the user.
			:return: Returns the User object or raises an exception (pterodactyl.Objects.Errors.NotFoundHttpException) if not found.
			"""

			# To-Add:
			# Include parameters:
			# - servers

			req:Response = self.__cObj.session.get(f"{self.__cObj.panel_url}/api/application/users/{user_id}")
			if req.status_code != 200:
				TransformToObject(self.__cObj,req.json()) # If there's an error to deal with it, it will be raised. Otherwise, default "Request failed!"
				raise RequestFailed("Unknown error!",req.status_code)

			req_json:dict = req.json()
			_u:User = TransformToObject(self.__cObj,req_json)

			return _u
		# Aliases
		get = get_user
		get_by_id = get_user
		get_user_by_id = get_user

		def get_by_external_id(self,external_id:str) -> User:
			"""
			Get a user based on their external ID (if set).
			:param external_id: The external ID of the user.
			:return: Returns the User object or raises an exception (pterodactyl.Objects.Errors.NotFoundHttpException) if not found.
			"""

			# To-Add:
			# Include parameters:
			# - servers

			req:Response = self.__cObj.session.get(f"{self.__cObj.panel_url}/api/application/users/external/{external_id}")
			if req.status_code != 200:
				TransformToObject(self.__cObj,req.json())
				raise RequestFailed("Unknown error!",req.status_code)

			req_json:dict = req.json()
			_u:User = TransformToObject(self.__cObj,req_json)

			return _u
		# Aliases
		get_user_by_external_id = get_by_external_id

		def create_user(self,email:str,username:str,first_name:str,last_name:str) -> User:
			"""
			Creates a new user with the provided information.
			:param email: The email of the user.
			:param username: The username of the user.
			:param first_name: The first name of the user.
			:param last_name: The last name of the user.
			:return: Returns the User object of the created user.
			"""

			payload:dict[str,str] = {
				"email": email,
				"username": username,
				"first_name": first_name,
				"last_name": last_name
			}

			req:Response = self.__cObj.session.post(f"{self.__cObj.panel_url}/api/application/users",data=payload)
			if req.status_code != 201:
				TransformToObject(self.__cObj,req.json())
				raise RequestFailed("Unknown error!",req.status_code)

			req_json:dict = req.json()
			_u:User = TransformToObject(self.__cObj,req_json)

			return _u
		# Aliases
		new = create_user
		create = create_user

		def update_user(self,user_id:int,field:str,new_value:str) -> User:
			"""
			Update a user's information.
			:param user_id: The ID of the user to be updated.
			:param field: Field to be updated. Can be any of the following: email,username,first_name,last_name,language,password
			:param new_value: New value for the field.
			:return: Returns the new User object with the updated information. (Will be the same as the passed user object if changed field is password).
			"""

			assert field in ["email","username","first_name","last_name","language","password"], "Invalid field! Can only be any of the following: email,username,first_name,last_name,language,password"

			payload:dict[str,str] = {
				field: new_value
			}

			req:Response = self.__cObj.session.patch(f"{self.__cObj.panel_url}/api/application/users/{user_id}",data=payload)
			if req.status_code != 200:
				TransformToObject(self.__cObj,req.json())
				raise RequestFailed("Unknown error!",req.status_code)

			req_json:dict = req.json()
			_u:User = TransformToObject(self.__cObj,req_json)

			return _u

		def delete_user(self,user_id:int) -> None:
			"""
			Deletes a user's account.
			:param user_id: ID of the user to be deleted.
			"""
			req:Response = self.__cObj.session.delete(f"{self.__cObj.panel_url}/api/applications/users/{user_id}")
			if req.status_code != 204:
				TransformToObject(self.__cObj,req.json())
				raise RequestFailed("Unknown error!",req.status_code)

	class __Nodes:
		def __init__(self,cObj:Consistent) -> None:
			self.__cObj:Consistent = cObj
		
		def get_nodes(self,list_all_pagination:bool=True,page:int=1) -> list[Node]:
			if list_all_pagination:
				assert page == 1, "list_all_pagination means pages will not be used."

			nodes:list[Node] = []

			req:Response = self.__cObj.session.get(f"{self.__cObj.panel_url}/api/application/nodes")
			if req.status_code != 200:
				TransformToObject(self.__cObj,req.json()) # If there's an error to deal with it, it will be raised. Otherwise, default "Get request fail!"
				raise RequestFailed("Unknown error!",req.status_code)

			req_json:dict = req.json()
			_ls:list = TransformToObject(self.__cObj,req_json)
			if not isinstance(_ls,list):
				raise Exception(f"Invalid request response!\n\nResponse: {dumps(req_json)}")
			for _n in _ls:
				nodes.append(TransformToObject(self.__cObj,_n))

			return nodes
		# Aliases
		list_nodes = get_nodes

	class __Locations:
		def __init__(self,cObj:Consistent) -> None:
			self.__cObj:Consistent = cObj

	class __Servers:
		def __init__(self,cObj:Consistent) -> None:
			self.__cObj:Consistent = cObj

	class __Nests:
		def __init__(self,cObj:Consistent) -> None:
			self.__cObj:Consistent = cObj
