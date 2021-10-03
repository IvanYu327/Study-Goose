# Study-Goose
Discord bot with chatbot AI, to do lists, music, image processing, and more!

# Inspiration
During the pandemic, many schools from primary to post secondary have been forced online. As a result, students are finding new ways to connect, manage, and engage in the virtual environment, and communication platforms like Discord have skyrocketed in usage and at many schools like the University of Waterloo, every program, class, and club have a Discord. However, Discord is not a common app for all students, as the platform was originally targeted for gamers. As a result, it can be a confusing place to navigate on top of all the other online platforms.

We created Study Goose, an all inclusive Discord Bot for students and beyond! (Called study goose because like the Canadian Geese infestation at our school, Study Goose is everywhere)

# What it does
Study Goose does many things, and we’ll go over each of its features and commands associated with each category.

**To do list**
Study Goose manages a to-do list for the server that is meant to be managed by server admins in class settings where representatives of the class can update it with new tasks that the class has for the week, something that is already being done widely in our school. Students can see their class deliverables for the week and let each other know if anything is missing. Teamwork makes the dreamwork!

In addition, whenever Study Goose joins a server, it automatically creates a dedicated to do list for each one.

**Associated Commands:**
settodo: Moves the to do list to the current channel
          Ex: ?settodo
**reset**: Resets the to do list, creating a fresh blank one while leaving the previous one in the channel for future reference
          Ex: ?reset
**add**: Adds an item to the current to do list based on the day or heading,
          Ex: ?add day [your item to do], ?add monday quiz, ?add other do survey
**remove**:
            Adds an item to the current to do list based on the day and item reference number.,
          Ex: ?remove [heading] [item number],  ?remove monday 1,
**edit**: Edits an item to the current to do list based on the day and item reference number.,
          Ex: edit [heading][item number][item to do], ?edit tuesday 2 exam

**Chatbot AI**
If any message mentions @Study Goose or says the words “study goose”, study goose responds to their message using it’s trained Machine Learning model, specifically trained on common phrases that a new member may have such as “who are you” “What do you do”  “hi” and many more. Because Study Goose’s chatbot uses ML to figure out what the user is asking, new users can learn more about the bot without having to worry about finding the right command or spelling it correctly. The Study Goose ML model is ~99%+ accurate.
 INSERT PICTURE

**Music Bot**
Studying with music is a must and with the recent shutdown of Groovy and Rythm, students who aren’t as familiar with other bots may not be able to find other smaller bots. So, we included that into Study Goose too! Study Goose has a simple music playing feature, allowing you to play songs from a Youtube URL or song titles and search words. 

Unlike Groove and Rythm, Study Goose does not offer paid services, which were the main reason these bots violated Google ToS by profiting through the use of Google services. Study Goose is and will always be free to use.

**Associated Commands**: play[url], pause, resume, stop, join, disconnect

**Question**
Need to answer a math question? Geography? Ask Study Goose! Simply ask Study Goose and it will answer, being able to complete complex mathematical equations and answer a wide range of question.
**Associated Commands**: ?question[your question]

**imageToText**:
One issue with school is note taking. With Study Goose’s image to text feature, simply use the command, upload your image, and study goose will extract all the text for you!
**Associated Commands**: ?imagetotext and then follow prompt to upload image

**Other features**:
**?pin**: Allow regular members to pin important content without needing server admins or permissions
**?cry and ?scream**: Study Goose sends gifs and memes to help you expression your pain and frustration in school
**?help**: help display
**?help [command]**: Displays help details for every command and how to use it
**?setprefix**: Allows server admins to update the prefix

## How we built it
Study Goose has a lot of features, so we will go over each of the groups and how they were built and what technologies it uses. Study Goose itself is a Discord Bot, written in python using the discord.py API, all the features and commands use the discord API in order to communicate with users and bot output.

Specific features that used other technologies were:
**To do list features and setprefix**
The to-do list and prefix was stored with MongoDB, providing a robust way to store large amounts of data in an organized fashion and save it should the bot ever need to reboot. The to-do list's location in the server is also stored, enabling commands like settodo to accurately locate and move the to-do list to a new channel. Everytime Study Goose joins a server, it creates a new collection for it on the database.
**Music Bot**
The music bot features were made with discord.py[voice] and youtube_dl
I**mage to Text**
The image to text feature was made using pytesseract and PIL (Python Imaging Library)
**Chatbot**
The chatbot was built with tensorflow, numpy, tflearn, and nltk (Natural Language Toolkit) and used a custom training set that we created to train the model. We created our own neural network and model instead of using a pretrained one from the internet in order to fit the context of the bot.
**Questions**
We used the wolfram API to make use of its computational power and vast question and answer base

Full list of technologies: Python, discord.py API, MongoDB, discord.py [voice], youtube_dl, pytesseract, PIL (Python Imaging Library), numpy, tensorflow, tflearn, nltk, wolfram API
