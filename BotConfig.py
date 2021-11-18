import discord, re, aiohttp, os, traceback, logging, aiosqlite
from discord.ext import commands

async def get_prefix(client, message):
  extras = ["smg4*", "smg*", "s*"]
  comp = re.compile("^(" + "|".join(map(re.escape, extras)) + ").*", flags = re.I)
  match = comp.match(message.content)

  if match is not None:
    extras.append(match.group(1))
  return commands.when_mentioned_or(*extras)(client, message)


class SMG4Bot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def start(self, *args, **kwargs):
    self.session = aiohttp.ClientSession()
    self.sus_users = await aiosqlite.connect('sus_users.db')
    cur = await self.sus_users.cursor()
    cursor=await cur.execute("SELECT * FROM RTFM_DICTIONARY")
    self.rtfm_libraries = dict(await cursor.fetchall())
    await super().start(*args, **kwargs)

  async def close(self):
    await self.session.close()
    await self.sus_users.close()
    await super().close() 

bot = SMG4Bot(command_prefix = (get_prefix),intents = discord.Intents.all())

client = discord.Client(intents = discord.Intents.all())

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    try:
      bot.load_extension(f'cogs.{filename[:-3]}')
    except commands.errors.ExtensionError:
      traceback.print_exc()

logging.basicConfig(level = logging.INFO)