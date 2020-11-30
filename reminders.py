import datetime
import pytz
import typing
import asyncio
import main
import discord.ext.tasks

timezone = pytz.timezone('Europe/Berlin')
TESTING = False


class CronRunner:
    def __init__(self, hour: int, minute: int, callback):
        self.last_run: typing.Optional[datetime.datetime] = None
        self.hour = hour
        self.minute = minute
        self.callback = callback

    async def try_run(self, override_time: typing.Optional[datetime.datetime] = None):
        now = override_time or datetime.datetime.now(timezone)

        if self.last_run is not None:
            if now - self.last_run < datetime.timedelta(minutes=2):
                return

        target_time = timezone.localize(datetime.datetime(year=now.year,
                                        month=now.month,
                                        day=now.day,
                                        hour=self.hour,
                                        minute=self.minute))

        if now >= target_time and now - target_time <= datetime.timedelta(minutes=1):
            self.last_run = now
            await self.callback(now)


def is_meetup_day(dt: datetime.datetime):
    """ Last Thursday of the month """
    if dt.weekday() != 3:
        return False

    tmp = dt
    while tmp.month == dt.month:
        tmp = tmp + datetime.timedelta(days=1)
        if tmp.weekday() == 3:
            return False

    return True


async def remind_day_before_meetup(now: datetime.datetime):
    tomorrow = now + datetime.timedelta(days=1)
    if not is_meetup_day(tomorrow):
        return

    if TESTING:
        global accepted_times
        accepted_times.append(now)
    else:
        await main.channel.send("@everyone Meetup tomorrow at 6!" + main.message_footer)

day_before_reminder_runner = CronRunner(18, 0, remind_day_before_meetup)



@discord.ext.tasks.loop(seconds=30)
async def run():
    for runner in [day_before_reminder_runner]:
        await runner.try_run()


def test():
    global TESTING
    TESTING = True

    assert is_meetup_day(datetime.datetime(2020, 11, 26))
    assert not is_meetup_day(datetime.datetime(2020, 11, 27))
    assert not is_meetup_day(datetime.datetime(2020, 11, 19))

    global accepted_times
    accepted_times = []

    async def start_test_runners():
        test_dt = datetime.datetime(2020, 10, 1)
        while test_dt < datetime.datetime(2020, 12, 31):
            await day_before_reminder_runner.try_run(timezone.localize(test_dt))
            test_dt += datetime.timedelta(seconds=30)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_test_runners())
    loop.close()

    assert len(accepted_times) == 3
    assert accepted_times[0] == timezone.localize(datetime.datetime(2020, 10, 28, 18))
    assert accepted_times[1] == timezone.localize(datetime.datetime(2020, 11, 25, 18))
    assert accepted_times[2] == timezone.localize(datetime.datetime(2020, 12, 30, 18))


if __name__ == "__main__":
    test()
