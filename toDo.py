import discord, calendar

async def add(ctx,day,item,client,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]

    dayPost = serverCollection.find_one({"_id":day.lower()})
    itemsArray = dayPost["items"]
    itemsArray.append(item)
    
    myQuery = {"_id":day.lower()}
    newValues = { "$set": {"items":itemsArray}}
    serverCollection.update_one(myQuery,newValues)
    
    toDochannel = client.get_channel(getChannelID(ctx,serversDB))
    messageID = getToDoMessageID(ctx,serversDB)
    message = await toDochannel.fetch_message(messageID)
    await message.edit(embed=toDoEmbed(ctx,serversDB))

async def remove(ctx,day,itemNumber,client,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]

    dayPost = serverCollection.find_one({"_id":day.lower()})
    itemsArray = dayPost["items"]
    itemsArray.pop(itemNumber)
    
    myQuery = {"_id":day.lower()}
    newValues = { "$set": {"items":itemsArray}}
    serverCollection.update_one(myQuery,newValues)
    
    toDochannel = client.get_channel(getChannelID(ctx,serversDB))
    messageID = getToDoMessageID(ctx,serversDB)
    message = await toDochannel.fetch_message(messageID)
    await message.edit(embed=toDoEmbed(ctx,serversDB))
    
    toDochannel = client.get_channel(getChannelID(ctx,serversDB))
    messageID = getToDoMessageID(ctx,serversDB)
    message = await toDochannel.fetch_message(messageID)
    await message.edit(embed=toDoEmbed(ctx,serversDB))

async def edit(ctx,day,itemNumber,edit,client,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]

    dayPost = serverCollection.find_one({"_id":day.lower()})
    itemsArray = dayPost["items"]
    itemsArray[itemNumber]=edit

    myQuery = {"_id":day.lower()}
    newValues = { "$set": {"items":itemsArray}}
    serverCollection.update_one(myQuery,newValues)
    toDochannel = client.get_channel(getChannelID(ctx,serversDB))
    messageID = getToDoMessageID(ctx,serversDB)
    message = await toDochannel.fetch_message(messageID)
    await message.edit(embed=toDoEmbed(ctx,serversDB))
    
    toDochannel = client.get_channel(getChannelID(ctx,serversDB))
    messageID = getToDoMessageID(ctx,serversDB)
    message = await toDochannel.fetch_message(messageID)
    await message.edit(embed=toDoEmbed(ctx,serversDB))

async def setTitle(ctx,title,client,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]
    myQuery = {"_id":"TO DO LIST"}
    newValues = { "$set": {
        "Title": title
    } }
    serverCollection.update_one(myQuery,newValues)

    toDochannel = client.get_channel(getChannelID(ctx,serversDB))
    messageID = getToDoMessageID(ctx,serversDB)
    message = await toDochannel.fetch_message(messageID)
    await message.edit(embed=toDoEmbed(ctx,serversDB))


async def setChannel(ctx,client,serversDB):    
    oldChannelID = getChannelID(ctx,serversDB)
    oldMessageID = getToDoMessageID(ctx,serversDB)

    await ctx.send("settodo")
    newToDoMessage = await ctx.send(embed=toDoEmbed(ctx,serversDB))
    
    serverCollection = serversDB[str(ctx.guild.id)]
    myQuery = {"_id":"TO DO LIST"}
    newValues = { "$set": {
        "To Do Message ID": newToDoMessage.id,
        "To Do Channel ID": newToDoMessage.channel.id
    } }
    serverCollection.update_one(myQuery,newValues)
    
    if oldMessageID != 0:
        await client.http.delete_message(oldChannelID, oldMessageID)

async def reset(ctx,serversDB):  
    print("resetting")
    serverCollection = serversDB[str(ctx.guild.id)]
    
    
    for day in range(7):
        print(calendar.day_name[day].lower())
        myQuery = {"_id":calendar.day_name[day].lower()}
        newValues = { "$set": {
            "items":[]
        } }
        serverCollection.update_one(myQuery,newValues)
    print("reset days")

    myQuery = {"_id":"other"}
    newValues = { "$set": {
        "items":[]
    } }
    serverCollection.update_one(myQuery,newValues)

    myQuery = {"_id":"TO DO LIST"}
    newValues = { "$set": {
        "Title":"To Do List"
    } }
    serverCollection.update_one(myQuery,newValues)
    
    print("reset other")

    newToDoMessage = await ctx.send(embed=toDoEmbed(ctx,serversDB))
    
    myQuery = {"_id":"TO DO LIST"}
    newValues = { "$set": {
        "To Do Message ID": newToDoMessage.id,
        "To Do Channel ID": newToDoMessage.channel.id
    } }
    serverCollection.update_one(myQuery,newValues)

def toDoEmbed(ctx,serversDB):
    print("making")
    serverCollection = serversDB[str(ctx.guild.id)]
 

    embed=discord.Embed(title=str(ctx.guild.name)+": `{}`".format(getTitle(ctx,serversDB)), description="Get to work!")
    embed.set_thumbnail(url=ctx.guild.icon_url)

    for day in range(7):
        dayPost = serverCollection.find_one({"_id":calendar.day_name[day].lower()})
        values = ""
        for item in dayPost["items"]:
            values += "`{}` - ".format(dayPost['items'].index(item))+item+"\n"

        if values == "":
            values = "Nothing today!"
        print(values)
        embed.add_field(name=calendar.day_name[day], value=values, inline=False)
    
    otherPost = serverCollection.find_one({"_id":"other"})
    otherValues = ""
    if len(otherPost["items"]) != 0:
        for item in otherPost["items"]:
            otherValues += "`{}` - ".format(otherPost['items'].index(item))+item+"\n"
    else:
        otherValues = "Nothing!"
    print(otherValues)
    embed.add_field(name="Other", value=otherValues, inline=False)

    embed.set_footer(text="Contact weewoo#6104 for support")
    print("reutnred")
    return embed

def getChannelID(ctx,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]
    serverInfoPost = serverCollection.find_one({"_id":"TO DO LIST"})
    channelID = serverInfoPost["To Do Channel ID"]
    return channelID

def getToDoMessageID(ctx,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]
    toDoPost = serverCollection.find_one({"_id":"TO DO LIST"})
    toDoMessageID = toDoPost["To Do Message ID"]
    return toDoMessageID

def getTitle(ctx,serversDB):
    serverCollection = serversDB[str(ctx.guild.id)]
    toDoPost = serverCollection.find_one({"_id":"TO DO LIST"})
    title = toDoPost["Title"]
    return title