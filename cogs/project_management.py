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

import nextcord
from nextcord.ext import commands
from time import time, mktime
import asyncio
import datetime
import pytz

_DELAY = 60  # Delay between each check for reminders
_MAGIC_NUMBER = 0x12abcdef
_ASSIGNED_COLOR = 0x8e3b3b
_UNASSIGNED_COLOR = 0x0adbfc
_COMPLETED_COLOR = 0x00ff00
_OVERDUE_COLOR = 0xff0000
_NORMAL = 1
_COMPLETE = 2
_OVERDUE = 3
_TIME_ZONE = pytz.timezone('US/Eastern')


class mySnowFlake(nextcord.abc.Snowflake):
    def __init__(self, id):
        self.id = id


class _Task:
    def __init__(self, task_id, create=False):
        self.id = task_id
        if create:
            self.name = ""
            self.type = 0
            self.status = _NORMAL
            self.due_date = 0
            self.remind_date = 0
            self.assignees = []
            self.description = ""
            self.update()

        else:
            with open(f".pmp/{hex(task_id)[2:]}.task", "r") as f:
                self.name = f.readline().strip()
                self.type = int(f.readline().strip(), 16)
                self.status = int(f.readline().strip(), 16)
                self.due_date = int(f.readline().strip(), 16)
                self.remind_date = int(f.readline().strip(), 16)
                _assignees = f.readline().strip().split("\t")
                self.assignees = [int(id) for id in _assignees if id]
                self.description = f.read()

    def __bool__(self):
        return self.type != 0

    def __repr__(self):
        return f"<Task {hex(self.id)} {self.name}>"

    def update(self):
        with open(f".pmp/{hex(self.id)[2:]}.task", "w") as f:
            f.write(f"{self.name}\n{self.type}\n{self.status}\n")
            f.write(hex(self.due_date)[2:])
            f.write("\n")
            f.write(hex(self.remind_date)[2:])
            f.write("\n")
            f.write("\t".join(map(str, self.assignees)))
            f.write("\n")
            f.write(self.description)


class ProjectManagement(commands.Cog):
    @staticmethod
    def embed_task_summary(task):
        if task.due_date:
            due_date_timestamp = datetime.datetime.fromtimestamp(
                float(task.due_date), tz=_TIME_ZONE)
            due_date_str = due_date_timestamp.strftime('%m/%d/%Y %H:%M')
        else:
            due_date_str = "N/A"

        dict_embed = nextcord.Embed(
            title=task.name,
            description=f"Due Date: {due_date_str}\n" +
            f"Description: {task.description}\n",
            colour=_COMPLETED_COLOR if task.status == _COMPLETE else _ASSIGNED_COLOR
        )
        dict_embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/952037974420385793/952038039457267712/Eve_Code_Ultimate_2.png")
        dict_embed.set_footer(
            text="Github: https://github.com/jonah-chen/eve-bot")

        return dict_embed

    @commands.command(aliases=["dummy2"])
    async def dummy(self, ctx, member: nextcord.Member = None, *, msg):
        try:
            await ctx.send(f"One second...{msg}")
            channel = await self.client.create_dm(mySnowFlake(member.id))
            await channel.send(f"asdflkj")
            print("user")

        except Exception as e:
            print(e)

    def __init__(self, client) -> None:
        self.client = client
        self.reminders = False
        self._read_cache()
        self._read_type_cache()

    def __del__(self):
        self._write_cache()

    def _write_cache(self):
        with open(".pmp/cache", "w") as cache_file:
            cache_file.write("\n".join([hex(t.id)[2:] for t in self.cache]))

    def _read_cache(self):
        with open(".pmp/cache", "r") as cache_file:
            cache_strs = cache_file.read().splitlines()
        self.cache = set([_Task(int(t, 16))
                         for t in cache_strs])  # previous cached messages

    def _read_type_cache(self):
        with open(".pmp/types", "r") as cache_file:
            cache_strs = cache_file.read().splitlines()

        self.types = dict()
        for cache_str in cache_strs:
            cache_str = cache_str.split("|")
            self.types[cache_str[0]] = cache_str[1]

    @commands.command(aliases=["live_update", "realtime", "realtime_updates", "live_updates", "realtime_update"])
    async def toggle_live(self, ctx):
        self.reminders = not self.reminders
        await ctx.send(f"Live updates are now {'enabled' if self.reminders else 'disabled'}.")

        while self.reminders:
            events = [t for t in self.cache if (
                t.remind_date <= time() and t.remind_date >= time() - _DELAY)]
            for task in events:
                if task.assignees and task.status != _COMPLETE:
                    emb = ProjectManagement.embed_task_summary(task)
                    for assignee in task.assignees:
                        channel = await self.client.create_dm(mySnowFlake(assignee))
                        await channel.send(embed=emb)

            await asyncio.sleep(_DELAY)

    @commands.command(aliases=['toggle_reminder'])
    async def toggle_reminders(self, ctx):
        self.reminders = not self.reminders
        await ctx.send(f"Reminders are now {'enabled' if self.reminders else 'disabled'}")

    @commands.command(aliases=['timeline'])
    async def todo(self, ctx):
        tasks = [t for t in self.cache if t.status != _COMPLETE]
        tasks.sort(key=lambda t: t.due_date)
        if not tasks:
            await ctx.send("No task to show")
            return

        embed = nextcord.Embed(title="Todo List", color=0x555555)
        for task in tasks:
            embed.add_field(name=f"{task.name}",
                            value=f"{task.due_date}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['info'])
    async def describe(self, ctx, *, msg):
        for task in self.cache:
            if task.name == msg:
                emb = ProjectManagement.embed_task_summary(task)
                await ctx.send(embed=emb)
                return
        await ctx.send("Task not found.")

    @commands.command()
    async def assign(self, ctx, member: nextcord.Member = None, *, msg):
        try:
            for task in self.cache:
                if task.name == msg:
                    if member is None:
                        await ctx.send("Please specify a member.")
                        return
                    if member.id in task.assignees:
                        await ctx.send("Member already assigned.")
                        return
                    task.assignees.append(member.id)
                    task.update()
                    await ctx.send(f"`{member.name}` has been assigned to `{task.name}`.")
                    return
        except Exception as e:
            print(e)
        await ctx.send("Task not found.")

    @commands.command(aliases=['task', 'new_task', 'create', 'add'])
    async def add_task(self, ctx, *, msg):
        if any(c.isspace() for c in msg):
            await ctx.send("Task name cannot contain spaces.")
            return
        if msg.startswith("__"):
            await ctx.send("Task name cannot start with double underscore.")
            return

        task_id = int(time()) - _MAGIC_NUMBER
        # check task does not have the same name
        if any(t.name == msg for t in self.cache):
            await ctx.send("Task name already exists.")
            return

        # add task to cache
        my_task = _Task(task_id, True)
        my_task.name = msg
        my_task.update()
        self.cache.add(my_task)
        self._write_cache()
        await ctx.send(f"Task `{msg}` has been created.")

    @commands.command(aliases=['+', 'description'])
    async def add_description(self, ctx, *, msg):
        fpos = msg.find(" ")
        task = msg[:fpos]
        description = msg[fpos+1:]
        for t in self.cache:
            if t.name == task:
                t.description = description
                t.update()
                await ctx.send(f"Description for `{t.name}` has been updated.")
                return

        await ctx.send("Task not found.")

    @commands.command(aliases=['categlorize', 'add_to_category', 'set_type'])
    async def cat(ctx, *, msg):
        await ctx.send("Not implemented.")

    @commands.command(aliases=['due_date', 'set_due_date', 'deadline', 'set_deadline'])
    async def due(self, ctx, *, msg):
        now = datetime.datetime.now(_TIME_ZONE)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + datetime.timedelta(days=1)
        task = msg.split()[0]
        parts = msg[len(task):].split()
        for t in self.cache:
            if t.name == task:
                task = t
                break

        if type(task) is not _Task:
            await ctx.send("Task not found.")
            return

        if 'today' in msg.lower():
            tgt_date = today
        elif 'tmrw' in msg.lower() or 'tomorrow' in msg.lower() or 'tom' in msg.lower() or 'tmr' in msg.lower():
            tgt_date = tomorrow
        elif 'mon' in msg.lower():  # next monday
            tgt_date = today + datetime.timedelta(days=7 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        elif 'tue' in msg.lower():  # next tuesday
            tgt_date = today + datetime.timedelta(days=1 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        elif 'wed' in msg.lower():  # next wednesday
            tgt_date = today + datetime.timedelta(days=2 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        elif 'thu' in msg.lower():  # next thursday
            tgt_date = today + datetime.timedelta(days=3 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        elif 'fri' in msg.lower():  # next friday
            tgt_date = today + datetime.timedelta(days=4 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        elif 'sat' in msg.lower():  # next saturday
            tgt_date = today + datetime.timedelta(days=5 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        elif 'sun' in msg.lower():  # next sunday
            tgt_date = today + datetime.timedelta(days=6 - today.weekday())
            if tgt_date < today:
                tgt_date += datetime.timedelta(days=7)
        else:
            date_cand = [p for p in parts if p.find('/') != -1]
            if len(date_cand) != 1:
                await ctx.send("Invalid date format. Must be in M/D, M/DD, or MM/DD format.")
                return
            date_cand = date_cand[0].split('/')
            month = int(date_cand[0])
            day = int(date_cand[1])
            if month < 1 or month > 12 or day < 1 or day > 31:
                await ctx.send("Invalid date")
                return
            tgt_date = datetime.datetime(
                now.year, month, day, 0, 0, 0, 0, _TIME_ZONE)
            if tgt_date < now:
                tgt_date.year += 1

        time_cand = [p for p in parts if p.find(':') != -1]
        if len(time_cand) != 1:
            await ctx.send("Invalid time format.")
            return
        time_cand = time_cand[0].split(':')
        hour = int(time_cand[0])
        minute = int(time_cand[1])
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            await ctx.send("Invalid time")
            return
        tgt_date = tgt_date.replace(hour=hour, minute=minute)

        task.due_date = int(mktime(tgt_date.timetuple()))
        task.update()
        await ctx.send(f"Task {task.name} is now due on {tgt_date.strftime('%m/%d/%Y %H:%M')}")

    @commands.command(aliases=['set_reminder'])
    async def remind(self, ctx, *, msg):
        task = msg.split()[0]
        msg = msg[len(task):]
        for t in self.cache:
            if t.name == task:
                task = t
                break

        if type(task) is not _Task:
            await ctx.send("Task not found.")
            return

        if task.due_date <= 0:
            await ctx.send("Cannot set reminder for task with no due date.")
            return

        number = ''.join([c for c in msg if c.isdigit()])
        if not number:
            await ctx.send("Invalid reminder time.")
            return
        number = int(number)
        if number < 1:
            await ctx.send("Reminder time must be positive.")
            return

        if 'min' in msg.lower() or 'm' in msg:
            number *= 60
        elif 'h' in msg.lower():
            number *= 3600
        elif 'd' in msg.lower():
            number *= 86400
        elif 'w' in msg.lower():
            number *= 604800
        elif 'mo' in msg.lower() or 'M' in msg:
            number *= 2592000
        else:
            await ctx.send("Invalid reminder time.")
            return

        task.remind_date = task.due_date - number
        task.update()

        date = datetime.datetime.fromtimestamp(task.remind_date, _TIME_ZONE)
        await ctx.send(f"Task {task.name} will be reminded on {date.strftime('%m/%d/%Y %H:%M')}")

    @commands.command(aliases=['complete', 'completed', 'finish', 'finish_task', 'finished'])
    async def done(self, ctx, *, msg):
        for t in self.cache:
            if t.name == msg:
                t.status = _COMPLETE
                t.update()
                await ctx.send(f"Marked {t.name} as complete.")
                return
        await ctx.send("Task not found.")


def setup(client):
    client.add_cog(ProjectManagement(client))
