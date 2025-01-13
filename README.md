# PterodactylPy

> [!CAUTION]
> Package is still in very early development. Do not use in a production environment!

> [!WARNING]
> All current code and structure is subject to change.

A Python wrapper for the Pterodactyl API.

## Random Notes
- [ ] Remove bloat
- [ ] Remove all methods like "update_user"
- [ ] Rewrite into async. Yes, that's right. I'm doing that.
- [ ] [User].update(), [Node].delete(), etc.
- - [x] User
- - [ ] Allocations
- - [ ] Nodes
- [ ] Implement pagination
- [ ] Add include arguments to everything

## Example

```python title="get_user.py"
import pterodactyl

panel_url:str = "http://panel.example.com/"
pterodactyl_application_key:str = "ptla_shhhhhhhhhhhhhhhhhhhhh!"

Panel = pterodactyl.API.Application(panel_url,pterodactyl_application_key)

user = Panel.Users.get_user(1)
user.set("first_name","Tato")
```
