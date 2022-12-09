from contextlib import asynccontextmanager
import aiohttp
import re


@asynccontextmanager
async def sona(username: str, password: str, session: aiohttp.ClientSession):
    r = await session.get("https://bu.sona-systems.com/default.aspx")
    matches = re.findall(r'<input type="hidden" name="(.+)" id.+value="(.+)"', await r.text())
    data = dict(matches) | {
        "ctl00$ContentPlaceHolder1$userid": username,
        "ctl00$ContentPlaceHolder1$pw": password,
        "ctl00$ContentPlaceHolder1$default_auth_button": "Log In",
    }
    await session.post("https://bu.sona-systems.com/default.aspx", data=data)
    yield session