# Neither finished nor used.

class Page:
	def __init__(self,count:int,list_object:list[dict]) -> None:
		self.__count:int = count
		self.__list_object:list[dict] = list_object
	
	@property
	def count(self) -> int:
		return self.__count
	
	@property
	def data(self) -> list[dict]:
		return self.__list_object

class PaginatedList:
	def __init__(self,total_items:int,total_pages:int,per_page:int,) -> None:
		self.__total_items:int = total_items
		self.__total_pages:int = total_pages
		self.__items_per_page:int = per_page

		self.__pages:dict[int,Page] = {}
	
	def add(self,page_number:int,page:Page) -> None:
		self.__pages[page_number] = page
		