from .Consistent import Consistent
from ..TransformToObject import TransformToObject
from ..Objects.Errors import RequestFailed

from datetime import datetime
from requests import Response

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
			def update(field:str,new_value:str) -> None:
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
					raise RequestFailed("Unknown error!",req.status_code)
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
					raise RequestFailed("Unknown error!",req.status_code)
				
			self.update = update
			self.delete = delete

	def __str__(self) -> str:
		return f"User[id: {self.__id}, username: {self.__username}, email: {self.__email}]"

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

class Node:
	def __init__(
			self,
			cObj:Consistent,
			node_id:int,
			uuid:str,
			public:bool,
			name:str,
			description:str,
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
			updated_at:datetime
			) -> None:
		self.__cObj:Consistent = cObj
		self.__id:int = node_id

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id
