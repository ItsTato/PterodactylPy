from .Consistent import Consistent
from ..Objects import Errors

from datetime import datetime
from requests import Response
from typing import Any

def TransformToObject(cObj:Consistent,obj:dict[str,Any]) -> Any:
	assert isinstance(cObj,Consistent), "Unsupported consistent object."

	if "object" in obj:

		if obj["object"] == "list":
			return obj["data"]

		if obj["object"] == "user":
			if "admin" in obj["attributes"]:
				u:User = User(cObj,False,obj["attributes"]["id"],obj["attributes"]["admin"],obj["attributes"]["username"],obj["attributes"]["email"],obj["attributes"]["first_name"],obj["attributes"]["last_name"],obj["attributes"]["language"])
				return u
			if "root_admin" in obj["attributes"]:
				u:User = User(cObj,True,obj["attributes"]["id"],obj["attributes"]["root_admin"],obj["attributes"]["username"],obj["attributes"]["email"],obj["attributes"]["first_name"],obj["attributes"]["last_name"],obj["attributes"]["language"])
				u.uuid = obj["attributes"]["uuid"]
				u.external_identifier = obj["attributes"]["external_id"]
				u.has_2fa = obj["attributes"]["2fa"]
				u.created_at = datetime.fromisoformat(obj["attributes"]["created_at"])
				u.updated_at = datetime.fromisoformat(obj["attributes"]["updated_at"])

				return u

	if "errors" in obj:

		errors:list[dict[str,str]] = obj["errors"]
		for error in errors:
			if getattr(Errors,error["code"]):
				raise getattr(Errors,error["code"])(error["detail"],int(error["status"]))

	raise Exception("Missing required object/errors attribute or package cannot deal with unknown object.")

class User:
	def __init__(
			self,
			cObj:Consistent,
			isApplication:bool,
			user_id:int,
			admin:bool,
			username:str,
			email:str,
			first_name:str,
			last_name:str,
			language:str
			) -> None:
		self.__cObj = cObj

		self.id:int = user_id
		self.external_identifier:str|None=None
		self.uuid:str|None=None
		self.username:str = username
		self.email:str = email
		self.first_name:str = first_name
		self.last_name:str = last_name
		self.language:str = language
		self.admin:bool = admin
		self.has_2fa:bool|None=None
		self.created_at:datetime|None=None
		self.updated_at:datetime|None=None

		if isApplication:
			def update() -> None:
				"""
				Update the class's details by fetching the user's details.
				"""
				
				req:Response = self.__cObj.session.get(f"{self.__cObj.panel_url}/api/application/users/{self.id}")
				if req.status_code != 200:
					TransformToObject(self.__cObj,req.json())
					raise Errors.RequestFailed("Unknown error!",req.status_code)
				req_json:dict = req.json()
				_u:User = TransformToObject(self.__cObj,req_json)

				self.external_identifier = _u.external_identifier
				if _u.uuid != None:
					self.uuid = _u.uuid
				self.username = _u.username
				self.email = _u.email
				self.first_name = _u.first_name
				self.last_name = _u.last_name
				self.language = _u.language
				self.admin = _u.admin

				# These three raise VSCode warnings. Since we are doing a GET,
				# these fields WILL be assigned and won't have a value of None.
				self.two_factor_auth = _u.two_factor_auth#type:ignore
				self.created_at = _u.created_at#type:ignore
				self.updated_at = _u.updated_at#type:ignore

			def modify(field:str,new_value:str) -> None:
				"""
				Update the user's information.
				:param field: Field to be updated. Can be any of the following: email,username,first_name,last_name,language,password
				:param new_value: New value for the field.
				:return: Returns the new User object with the updated information. (Will be the same as the passed user object if changed field is password).
				"""

				assert field in ["email","username","first_name","last_name","language","password"], "Invalid field! Can only be any of the following: email,username,first_name,last_name,language,password"

				payload:dict[str,str] = {
					field: new_value
				}

				req:Response = self.__cObj.session.patch(f"{self.__cObj.panel_url}/api/application/users/{self.id}",data=payload)
				if req.status_code != 200:
					TransformToObject(self.__cObj,req.json())
					raise Errors.RequestFailed("Unknown error!",req.status_code)
				req_json:dict = req.json()
				_u:User = TransformToObject(self.__cObj,req_json)

				if field == "email": self.email = _u.email
				if field == "username": self.username = _u.username
				if field == "first_name": self.first_name = _u.first_name
				if field == "last_name": self.last_name = _u.last_name
				if field == "language": self.language = _u.language
			
			def delete() -> None:
				"""
				Deletes the user's account.
				"""
				req:Response = self.__cObj.session.delete(f"{self.__cObj.panel_url}/api/applications/users/{self.id}")
				if req.status_code != 204:
					TransformToObject(self.__cObj,req.json())
					raise Errors.RequestFailed("Unknown error!",req.status_code)
			
			self.update = update
			self.fetch = update
			self.set = modify
			self.modify = modify
			self.delete = delete

	def __str__(self) -> str:
		return f"User[id: {self.id}, username: {self.username}, email: {self.email}, admin: {self.admin}]"

class Allocation:
	def __init__(
			self,
			cObj:Consistent,
			allocation_id:int,
			ip:str,
			port:int,
			assigned:bool,
			alias:str|None=None,
			notes:str|None=None
			) -> None:
		self.__cObj:Consistent = cObj

		self.id:int = allocation_id
		self.ip:str = ip
		self.port:int = port
		self.assigned:bool = assigned
		self.alias:str|None = alias
		self.notes:str|None = notes

	def __str__(self) -> str:
		return f"Allocation[id: {self.id}, ip: {self.ip}, port: {self.port}, assigned: {self.assigned}]"

class Location:
	def __init__(
			self,
			cObj:Consistent,
			location_id:int,
			short:str,
			long:str|None,
			updated_at:datetime,
			created_at:datetime
			) -> None:
		self.__cObj:Consistent = cObj

		self.id:int = location_id
		self.short:str = short
		self.long:str|None = long
		self.updated_at:datetime = updated_at
		self.created_at:datetime = created_at

	def __str__(self) -> str:
		return f"Location[id: {self.id}, short: {self.short}]"

class Node:
	def __init__(
			self,
			cObj:Consistent,
			node_id:int,
			uuid:str,
			public:bool,
			name:str,
			description:str|None,
			location_id:int,
			fqdn:str,
			url_scheme:str,
			behind_proxy:bool,
			maintenance_mode:bool,
			memory:int,
			memory_overallocate:int,
			disk:int,
			disk_overallocate:int,
			upload_size:int,
			daemon_listen:int,
			daemon_sftp:int,
			daemon_base:str,
			created_at:datetime,
			updated_at:datetime,
			allocated_memory:int,
			allocated_disk:int
			) -> None:
		self.__cObj:Consistent = cObj

		self.id:int = node_id
		self.uuid:str = uuid
		self.public:bool = public
		self.name:str = name
		self.description:str|None = description
		self.location_id:int = location_id
		self.fqdn:str = fqdn
		self.__url_scheme:str = url_scheme
		self.behind_proxy:bool = behind_proxy
		self.maintenance_mode:bool = maintenance_mode
		self.memory:int = memory
		self.memory_overallocate:int = memory_overallocate
		self.disk:int = disk
		self.disk_overallocate:int = disk_overallocate
		self.upload_size:int = upload_size
		self.daemon_listen_port:int = daemon_listen
		self.daemon_sftp_port:int = daemon_sftp
		self.daemon_base:str = daemon_base
		self.created_at:datetime = created_at
		self.updated_at:datetime = updated_at
		self.allocated_memory:int = allocated_memory
		self.allocated_disk:int = allocated_disk

		self.servers:list[Server] = []
		self.allocations:list[Allocation] = []
		self.location:Location|None = None
	
	@property
	def url_scheme(self) -> str:
		return self.__url_scheme
	@url_scheme.setter
	def url_scheme(self,new_scheme:str) -> None:
		assert new_scheme in ["http","https"], "Invalid scheme"
		self.__url_scheme = new_scheme

class Server:
	pass