from sona import sona
import asyncio
from aiohttp import ClientSession
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME, PASSWORD, DISC_URL = (
    os.getenv("USERNAME"),
    os.getenv("PASSWORD"),
    os.getenv("DISC_URL"),
)


async def main():
    async with ClientSession() as session:
        try:
            await session.post(DISC_URL, data={"content": "Started", "username": "sona-bot"})
            while True:
                async with sona(USERNAME, PASSWORD, session) as session:
                    while True:
                        r = await session.get(
                            "https://bu.sona-systems.com/all_exp_participant.aspx"
                        )
                        if r.url == "https://bu.sona-systems.com/default.aspx":
                            break  # session expired, retry
                        # print(await (await session.post("https://bu.sona-systems.com/AjaxMethods.asmx/RenewSession")).text())
                        if "No studies are available at this time." in await r.text():
                            print("No studies available :(")
                        else:
                            print("Study available!")
                            await session.post(
                                DISC_URL,
                                data={
                                    "content": "Study available!",
                                    "username": "sona-bot",
                                },
                            )
                        await asyncio.sleep(10)
        except Exception as e:
            await session.post(
                DISC_URL,
                data={"content": f"Error: {e}", "username": "sona-bot"},
            )
        finally:
            await session.post(
                DISC_URL,
                data={"content": "Stopped", "username": "sona-bot"},
            )


if __name__ == "__main__":
    asyncio.run(main())
