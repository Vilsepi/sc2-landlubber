import json
from pathlib import Path

import sc2

# Bots are created as classes and they need to have on_step method defined
class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    # On_step method is invoked each game-tick and should not take more than
    # 2 seconds to run, otherwise the bot will timeout and cannot receive new
    # orders.
    # It is important to note that on_step is asynchronous - meaning practices
    # for asynchronous programming should be followed.
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")
