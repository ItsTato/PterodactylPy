from .Consistent import Consistent
from ..Objects import Errors

from datetime import datetime
from requests import Response
from typing import Any

def TransformToObject(cObj:Consistent,obj:dict[str,Any]) -> Any:
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
				u.two_factor_auth = obj["attributes"]["2fa"]
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

		self.__id:int = user_id
		self.__external_identifier:str|None=None
		self.__uuid:str|None=None
		self.__username:str = username
		self.__email:str = email
		self.__first_name:str = first_name
		self.__last_name:str = last_name
		self.__language:str = language
		self.__admin:bool = admin
		self.__2fa:bool|None=None
		self.__created_at:datetime|None=None
		self.__updated_at:datetime|None=None

		if isApplication:
			def update() -> None:
				"""
				Update the class's details by fetching the user's details.
				"""
				
				req:Response = self.__cObj.session.get(f"{self.__cObj.panel_url}/api/application/users/{self.__id}")
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
				self.root_admin = _u.root_admin

				# These tree raise warnings. Worry not, since we are doing a GET on User details,
				# these fields will be assigned and not None.
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

				req:Response = self.__cObj.session.patch(f"{self.__cObj.panel_url}/api/application/users/{self.__id}",data=payload)
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
		return f"User[id: {self.__id}, username: {self.__username}, email: {self.__email}, admin: {self.__admin}]"

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id

	@property
	def external_identifier(self) -> str|None:
		return self.__external_identifier
	@external_identifier.setter
	def external_identifier(self,ext_id:str|None) -> None:
		self.__external_identifier = ext_id

	@property
	def uuid(self) -> str|None:
		return self.__uuid
	@uuid.setter
	def uuid(self,new_uuid:str) -> None:
		self.__uuid = new_uuid

	@property
	def username(self) -> str:
		return self.__username
	@username.setter
	def username(self,new_username:str) -> None:
		self.__username = new_username

	@property
	def email(self) -> str:
		return self.__email
	@email.setter
	def email(self,new_email:str) -> None:
		self.__email = new_email

	@property
	def first_name(self) -> str:
		return self.__first_name
	@first_name.setter
	def first_name(self,new_first_name:str) -> None:
		self.__first_name = new_first_name

	@property
	def last_name(self) -> str:
		return self.__last_name
	@last_name.setter
	def last_name(self,new_last_name:str) -> None:
		self.__last_name = new_last_name

	@property
	def language(self) -> str:
		return self.__language
	@language.setter
	def language(self,new_language:str) -> None:
		self.__language = new_language

	@property
	def admin(self) -> bool:
		return self.__admin
	@admin.setter
	def admin(self,new_value:bool) -> None:
		self.__admin = new_value

	@property
	def root_admin(self) -> bool:
		return self.admin
	@root_admin.setter
	def root_admin(self,new_value:bool) -> None:
		self.admin = new_value

	@property
	def is_admin(self) -> bool:
		return self.admin

	@property
	def two_factor_auth(self) -> bool|None:
		return self.__2fa
	@two_factor_auth.setter
	def two_factor_auth(self,new_value:bool) -> None:
		self.__2fa = new_value

	@property
	def two_factor_auth_enabled(self) -> bool|None:
		return self.two_factor_auth
	@two_factor_auth_enabled.setter
	def two_factor_auth_enabled(self,new_value:bool) -> None:
		self.two_factor_auth = new_value

	@property
	def created_at(self) -> datetime|None:
		return self.__created_at
	@created_at.setter
	def created_at(self,new_date:datetime) -> None:
		self.__created_at = new_date

	@property
	def updated_at(self) -> datetime|None:
		return self.__updated_at
	@updated_at.setter
	def updated_at(self,new_date:datetime) -> None:
		self.__updated_at = new_date

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
		self.__id:int = allocation_id
		self.__ip:str = ip
		self.__port:int = port
		self.__assigned:bool = assigned
		self.__alias:str|None = alias
		self.__notes:str|None = notes

	def __str__(self) -> str:
		return f"Allocation[id: {self.__id}, ip: {self.__ip}, port: {self.__port}, assigned: {self.__assigned}]"

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id
	
	@property
	def ip(self) -> str:
		return self.__ip
	@ip.setter
	def ip(self,new_ip:str) -> None:
		self.__ip = new_ip
	
	@property
	def port(self) -> int:
		return self.__port
	@port.setter
	def port(self,new_port) -> None:
		self.__port = new_port
	
	@property
	def assigned(self) -> bool:
		return self.__assigned
	@assigned.setter
	def assigned(self,new_value:bool) -> None:
		self.__assigned = new_value
	
	@property
	def alias(self) -> str|None:
		return self.__alias
	@alias.setter
	def alias(self,new_alias:str) -> None:
		self.__alias = new_alias
	
	@property
	def notes(self) -> str|None:
		return self.__notes
	@notes.setter
	def notes(self,new_notes:str) -> None:
		self.__notes = new_notes

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
		self.__id:int = location_id
		self.__short:str = short
		self.__long:str|None = long
		self.__updated_at:datetime = updated_at
		self.__created_at:datetime = created_at

	def __str__(self) -> str:
		return f"Location[id: {self.__id}, short: {self.__short}]"

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id
	
	@property
	def short(self) -> str:
		return self.__short
	@short.setter
	def short(self,new_short:str) -> None:
		self.__short = new_short
	
	@property
	def long(self) -> str|None:
		return self.__long
	@long.setter
	def long(self,new_long:str) -> None:
		self.__long = new_long

	@property
	def created_at(self) -> datetime|None:
		return self.__created_at
	@created_at.setter
	def created_at(self,new_date:datetime) -> None:
		self.__created_at = new_date

	@property
	def updated_at(self) -> datetime|None:
		return self.__updated_at
	@updated_at.setter
	def updated_at(self,new_date:datetime) -> None:
		self.__updated_at = new_date

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
		self.__id:int = node_id
		self.__uuid:str = uuid
		self.__public:bool = public
		self.__name:str = name
		self.__description:str|None = description
		self.__location_id:int = location_id
		self.__fqdn:str = fqdn
		self.__url_scheme:str = url_scheme
		self.__behind_proxy:bool = behind_proxy
		self.__maintenance_mode:bool = maintenance_mode
		self.__memory:int = memory
		self.__memory_overallocate:int = memory_overallocate
		self.__disk:int = disk
		self.__disk_overallocate:int = disk_overallocate
		self.__upload_size:int = upload_size
		self.__daemon_listen:int = daemon_listen
		self.__daemon_sftp:int = daemon_sftp
		self.__daemon_base:str = daemon_base
		self.__created_at:datetime = created_at
		self.__updated_at:datetime = updated_at
		self.__allocated_memory:int = allocated_memory
		self.__allocated_disk:int = allocated_disk

		self.__servers:list[Server] = []
		self.__allocations:list[Allocation] = []
		self.__location:Location|None = None

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id

	@property
	def uuid(self) -> str:
		return self.__uuid
	@uuid.setter
	def uuid(self,new_uuid:str) -> None:
		self.__uuid = new_uuid

	@property
	def public(self) -> bool:
		return self.__public
	@public.setter
	def public(self,new_value:bool) -> None:
		self.__public = new_value
	
	@property
	def name(self) -> str:
		return self.__name
	@name.setter
	def name(self,new_name:str) -> None:
		self.__name = new_name

	@property
	def description(self) -> str|None:
		return self.__description
	@description.setter
	def description(self,new_description:str) -> None:
		self.__description = new_description

	@property
	def location_id(self) -> int:
		return self.__location_id
	@location_id.setter
	def location_id(self,new_id:int) -> None:
		self.__location_id = new_id
	
	@property
	def fqdn(self) -> str:
		return self.__fqdn
	@fqdn.setter
	def fqdn(self,new_fqdn:str) -> None:
		self.__fqdn = new_fqdn
	
	@property
	def url_scheme(self) -> str:
		return self.__url_scheme
	@url_scheme.setter
	def url_scheme(self,new_scheme:str) -> None:
		assert new_scheme in ["http","https"], "Invalid scheme"
		self.__url_scheme = new_scheme

class Server:
	pass