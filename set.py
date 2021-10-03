def prefix(ctx,newPrefix,serversDB):
    print("prefix: "+newPrefix)
    serverCollection = serversDB[str(ctx.guild.id)]
    
    myQuery = {"_id":"SERVER INFO"}
    newValues = { "$set": { "Prefix": newPrefix } }
    serverCollection.update_one(myQuery,newValues)


