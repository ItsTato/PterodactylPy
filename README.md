# PterodactylPy

> [!CAUTION]
> Package is still in very early development. Do not use in a production environment!

> [!WARNING]
> All current code and structure is subject to change.

A Python wrapper for the Pterodactyl API.

## Random Notes
- [ ] [User].update(), [Node].delete(), etc.
- [ ] Implement pagination
- [ ] Add include arguments to everything
- [ ] Improve update_user to allow for multiple fields at once

## Example

```python title="get_user.py"
import pterodactyl

panel_url:str = "http://panel.example.com/"
pterodactyl_application_key:str = "ptla_shhhhhhhhhhhhhhhhhhhhh!"

Panel = pterodactyl.API.Application(panel_url,pterodactyl_application_key)

user = Panel.Users.get_user(1)
user.update("first_name","Tato")
```
