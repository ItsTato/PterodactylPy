from datetime import datetime

class Node:
	def __init__(
			self,
			node_id:int,
			uuid:str,
			public:bool,
			name:str,
			description:str,
			location_id:int,
			fqdn:str,
			scheme:str,
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
		self.__id:int = node_id

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id