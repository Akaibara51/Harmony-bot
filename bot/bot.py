#cd C:\Users\olive\OneDrive\Desktop\Music Bot\openjdk-13.0.2_windows-x64_bin\jdk-13.0.2\bin
#java -jar lavalink.jar
from pathlib import Path

import discord
from discord.ext import commands



class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob(cd "your bots directory here")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Cogs loaded")

    def run(self):
        self.setup()
        print(self._cogs)
        print("Running bot...")

        super().run("Your bots token here", reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    # async def on_error(self, err, *args, **kwargs):
    #     raise

    # async def on_command_error(self, ctx, exc):
    #     raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
        print("Bot ready.")


    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(">")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
