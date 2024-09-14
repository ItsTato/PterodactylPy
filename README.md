# PterodactylPy

> [!CAUTION]
> Package is still in very early development. Do not use in a production environment!

A Python wrapper for the Pterodactyl API.

## Example

```python title="get_user.py"
import pterodactyl

panel_url:str = "http://panel.example.com/"
pterodactyl_application_key:str = "ptla_shhhhhhhhhhhhhhhhhhhhh!"

Panel = pterodactyl.API.Application(panel_url,pterodactyl_application_key)

print(Panel.Users.get_user(1))
```
