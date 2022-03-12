"""
Project management section of the bot.

Files: 
    .pmp/cache -- cache file for directories
    .pmp/<id>.task -- task file for each task

<id> is the 32 bit task id in hexadecimal format.
.task file containing the following fields:
    - task name
    - type
    - status
    - due_date
    - remind_date
    - assignee(s), tab separated
    - description (could be multiple lines)
"""


import cmath
import nextcord
from nextcord.ext import commands
from time import time
import asyncio

_DELAY = 60 # Delay between each check for reminders
_MAGIC_NUMBER = 0x00abcdef

class _Task:
    def __init__(self, task_id, create=False):
        self.id             = task_id
        self.name           = ""
        self.type           = 0
        self.status         = 0
        self.date           = 0
        self.remind_date    = 0
        self.assignees      = []
        self.description    = ""

        if create:
            with open(f".pmp/{task_id}.task", "w") as f:
                f.write(f"{self.name}\n{self.type}\n{self.status}\n{self.date}\n{self.remind_date}\n{self.assignees}\n{self.description}")
            
        else:
            with open(f".pmp/{task_id}.task", "r") as f:
                self.name           = f.readline().strip()
                self.type           = int(f.readline().strip(), 16)
                self.status         = int(f.readline().strip(), 16)
                self.date           = int(f.readline().strip(), 16)
                self.remind_date    = int(f.readline().strip(), 16)
                self.assignees      = f.readline().strip().split("\t")
                self.description    = f.read()

    def __bool__(self):
        return self.type != 0

    def __repr__(self):
        return f"<Task {self.id} {self.name}>"


class ProjectManagement(commands.Cog):
    def __init__(self) -> None:
        self._read_cache()
        self._read_type_cache()
    

    def _read_cache(self):
        with open(".pmp/cache", "r") as cache_file:
            cache_strs = cache_file.read().splitlines()
        self.cache = set([_Task(int(t, 16)) for t in cache_strs]) # previous cached messages

    def _read_type_cache(self):
        with open(".pmp/types", "r") as cache_file:
            cache_strs = cache_file.read().splitlines()
        
        self.types = dict()
        for cache_str in cache_strs:
            cache_str = cache_str.split("|")
            self.types[cache_str[0]] = cache_str[1]

    async def _start(self):
        # TODO: check any task need to send reminder
        await asyncio.sleep(_DELAY)

    @commands.command()
    async def describe(ctx, *, msg):
        pass

    @commands.command()
    async def assign(ctx, member: nextcord.Member = None, *, msg):
        pass

    @commands.command()
    async def add_task(ctx, *, msg):
        if any(c.isspace() for c in msg):
            await ctx.send("Task name cannot contain spaces.")
            return
        if msg.startswith("__"):
            await ctx.send("Task name cannot start with double underscore.")
            return

        task_id = hex(int(time()))[2:] - _MAGIC_NUMBER
        # check task does not have the same name
        if any(t.name == msg for t in self.cache):
            await ctx.send("Task name already exists.")
            return
        
        # add task to cache
        ctx.cache.add(_Task(task_id, True))


    @commands.command(aliases=['categlorize', 'add_to_category', 'set_type'])
    async def cat(ctx, *, msg):
        pass

    @commands.command(aliases=['due_date', 'set_due_date'])
    async def due(ctx, *, msg):
        pass

    @commands.command(aliases=['set_reminder'])
    async def remind(ctx, *, msg):

        pass

    @commands.command()
    async def remove_task(ctx, *, msg):
        pass
