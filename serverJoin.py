import discord
import calendar

async def joinServer(guild,serversDB):
    if guild.system_channel.permissions_for(guild.me).send_messages:
        embed=discord.Embed(title="Hi! Hola! 你好! Bonjour! 안녕하세요! Honk!", description="I am Study Goose, a Student Helper Discord Bot!", color=0xffffff)
        embed.set_thumbnail(url="https://i.ibb.co/BtFqFJK/oie-1215237v1-YVUAUp.gif")
        embed.add_field(name="Getting Started", value="My default prefix is `?`. Use `?help` to get started and see what I can do!", inline=False)
        embed.set_footer(text="Contact weewoo#6104 for support.")
        await guild.system_channel.send(embed=embed)

    if not str(guild.id) in serversDB.list_collection_names():
        print("server not in db")
        newServerCollection = serversDB[str(guild.id)]
        
        serverInitPost = {
            "_id":"SERVER INFO",
            "Server ID":guild.id,
            "Server name":guild.name,
            "Prefix":"?"
        }

        toDoPost = {
            "_id":"TO DO LIST",
            "Program":None,
            "To Do Channel ID":0,
            "To Do Message ID":0,
            "Title":"To Do List"
        }
        
        newServerCollection.insert_many([serverInitPost,toDoPost])
        
        for day in range(7):
            dayPost = {
                "_id":calendar.day_name[day].lower(),
                "items":[]
            }
            newServerCollection.insert_one(dayPost)

        otherPost = {
                "_id":"other",
                "items":[]
            }
        newServerCollection.insert_one(otherPost)