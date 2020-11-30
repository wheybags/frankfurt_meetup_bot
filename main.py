import discord
import reminders
import config


client = discord.Client()
guild: discord.Guild = None
channel: discord.GroupChannel = None

message_footer = "\nI'm a custom bot for this meetup discord. You can edit me here: https://github.com/wheybags/frankfurt_meetup_bot"

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print("All Guilds:", [guild.name for guild in client.guilds])

    global guild
    for _guild in client.guilds:
        if _guild.name == config.guild_name:
            guild = _guild

    assert guild is not None

    global channel
    for _channel in guild.text_channels:
        if _channel.name == config.channel_name:
            channel = _channel

    assert channel is not None

    reminders.run.start()


def main():
    client.run(config.bot_token)


if __name__ == "__main__":
    main()
