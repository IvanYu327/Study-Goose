import discord

#HELP EMBED
def help(cmd,prefix):
    helpDescriptionsDict={
    "To-Do":"`settodo`  `reset`  `add`  `remove`  `edit`",
    "Music":"`play`  `pause`  `resume`  `stop`  `disconnect`",
    "Study tools":"`imagetotext`  `pin`  `question`  `cry`  `scream`",
    "Misc.":"`@me`  `help`  `setprefix`  `suggest`",
    "Detailed Command Help":"For help about a specific command, use `{}help [command].` \nExample: `{}help help`".format(prefix,prefix)
    }

    commandDescriptionsDict={
        "settodo":
            ["Moves the to do list to the current channel",
            f"`{prefix}settodo`"],
        "reset":
            ["Resets the to do list, creating a fresh blank one while leaving the previous one in the channel for reference.",
            f"`{prefix}reset`"],
        "add":
            ["Adds an item to the current to do list based on the day or heading",
            f"`{prefix}add [day][your item to do]`\n`{prefix}add monday quiz`\n`{prefix}add other do survey`"],
        "remove":
            ["Adds an item to the current to do list based on the day and item reference number.",
            f"`{prefix}remove[heading][item number]`\n`{prefix}remove monday 1`"],
        "edit":
            ["Edits an item to the current to do list based on the day and item reference number.",
            f"`{prefix}edit[heading][item number][item to do]`\n`{prefix}edit tuesday 2 exam`"],
        
        "play":
            ["Plays music into the voice channel of the user that calls it.",
            f"`{prefix}play [url]`\n`{prefix}play [title]`\n`{prefix}p [url]`"],
        "p":
            ["Plays music into the voice channel of the user that calls it.",
            f"`{prefix}play [url]`\n`{prefix}play [title]`\n`{prefix}p [url]`"],
        "pause":
            ["Pauses the music if playing.",
            f"`{prefix}pause`"],
        "resume":
            ["Resumes the music if paused.",
            f"`{prefix}resume`"],
        "stop":
            ["Stops the music playing from the bot if it is playing music.",
            f"`{prefix}stop`"],
        "disconnect":
            ["Disconnects the bot from the voice channel if it is currently in one.",
            f"`{prefix}disconnect`\n`{prefix}dc`"],
        "dc":
            ["Disconnects the bot from the voice channel if it is currently in one.",
            f"`{prefix}disconnect`\n`{prefix}dc`"],
        
        "imagetotext":
            ["",
            f"`{prefix}imagetotext`"],
        "pin":
            ["Allows regular members to pin important messages so they don't need an admin to do so everytime.",
            f"`{prefix}pin [important information]`\n`{prefix}pin Hey everyone here is the link to the zoom meet today.`"],
        "question":
            ["Ask questions in the chat, saving time from searching on google or bing, and also generating discussion as the answer is available for everyone to see",
            f"`{prefix}wolfram [question]`\n`{prefix}wolfram What is 1+1?`"],
        "scream":
            ["Allow the bot to express its pain and frustration for you in creative ways.",
            f"`{prefix}scream`"],
        "cry":
            ["Allow the bot to express its pain and frustration for you in creative ways.",
            f"`{prefix}cry`"],

        "@Study Goose":
            ["Talk to me! Ask me questions about myself and I will do my best to answer using my advanced chatbot AI!",
            f"`@Study Goose What do you do?`\n`study gooe I failed a test!`"],
        "help":
            ["List all commands or get specific info about a specific command.\n\n(You're already using this command.)",
            f"`{prefix}help`\n`{prefix}help [command]`"],
        "setprefix":
            ["Changes the prefix of the bot for this server.\n\n❗Only server admins may use this command",
            f"`{prefix}setprefix [new prefix]`"],
        "suggest":
            ["Sends a suggestion to the weewoo#6104 for new additions or feature suggestions to the bot.",
            f"`{prefix}suggest [your suggestion]`"]
    }

    if cmd == None:
        embed=discord.Embed(title="Help", color=0xfbff00)
        for key in helpDescriptionsDict:
            embed.add_field(name=key, value=helpDescriptionsDict[key], inline=False)
    elif cmd in commandDescriptionsDict:
        embed=discord.Embed(title="Command Help", color=0xfbff00)
        embed.add_field(name=f"{cmd} command", value=commandDescriptionsDict[cmd][0], inline=False)
        embed.add_field(name="Example Usage", value=commandDescriptionsDict[cmd][1], inline=False)
    else:
        embed=discord.Embed(title=f"What is `{cmd}`?", color=0xff0000)
        embed.add_field(name=cmd, value="This command does not exist, try using an actual command or learning how to spell.", inline=False)

    embed.set_footer(text="Contact weewoo#6104 for support.")
    return embed
