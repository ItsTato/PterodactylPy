from .Objects import Consistent, Errors
from .Objects.Pterodactyl import User

from typing import Any
from datetime import datetime

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
