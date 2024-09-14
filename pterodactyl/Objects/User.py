from datetime import datetime

class User:
	def __init__(
			self,
			user_id:int,
			admin:bool,
			username:str,
			email:str,
			first_name:str,
			last_name:str,
			language:str
			) -> None:
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
	def two_factor_auth(self) -> bool:
		return self.__2fa
	@two_factor_auth.setter
	def two_factor_auth(self,new_value:bool) -> None:
		self.__2fa = new_value

	@property
	def two_factor_auth_enabled(self) -> bool:
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
