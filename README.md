# Pterodactyl.py

> [!CAUTION]
> Package is still in very early development. Do not use in a production environment!

> [!WARNING]
> All current code and structure is subject to change.

A Python wrapper for the Pterodactyl API.

## Random Notes (Ordered in priority)

I've switched to a different development methodology. Instead of building this blindly, I'm going to make use of it in another project. This way, I can slowly add what I really need and fix the most important bugs. I think this gives me the right to call it, "purpose-built" as well, no?

- [x] Remove bloat
- [x] ~~Rewrite into async. Yes, that's right. I'm doing that.~~ No, I'm not doing that. Mind fog cleared.
- [ ] Remove all methods like "update_user". Make them more specific.
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
