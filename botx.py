import discord
import re
import random
import string
import requests
import json
import pickle
import requests

client = discord.Client()

active = True
mock  = False

memories = []
memories_file = 'memories.pk'

bot_command = "?"

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    help_list = []
    #msgin = re.findall(r"[\w']+", message.content)
    msgin_original = message.content #some functions need case sensitive input
    msgin = message.content.lower()
    msgin = msgin.split(" ")
    msgin_original = msgin_original.split(" ")
    print(msgin)

    global active, mock, memories, memories_file, bot_command

    tag = '{0.author.mention} : \n'.format(message)

    if message.author == client.user:
        return

    help_list.append(["!bot","Turns the bot on and off."])
    if ((bot_command+'!bot') in msgin[0]):
        active = not active
        msgout = 'Bot on = ' + str(active)
        await client.send_message(message.channel, msgout)

    
    if  active == False:
        return

    help_list.append(["hello","Just says hello!"])
    if ((bot_command+'hello') in msgin[0]):
        msgout = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msgout)

    help_list.append(["remember","Remember the following\nExample: remember Dre sellout or greatest ever?"])
    if ((bot_command+'remember') in msgin[0]):
        subject = msgin[1]
        memory = ' '.join(msgin_original[2:])
        msgout = tag+'Remembered '+subject+" as "+memory
        memories.append([subject, memory])
        #open a pickle file
        with open(memories_file, 'wb') as fi:
        # dump your data into the file
            pickle.dump(memories, fi)
        await client.send_message(message.channel, msgout)

    help_list.append(["recall","recall a memory"])
    if ((bot_command+'recall') in msgin[0]):
        with open(memories_file, 'rb') as fi:
            memories = pickle.load(fi)
        for x in memories:
            if x[0] == msgin[1]:
                subject = x[0]
                memory = x[1]
        msgout = tag+"Recalled "+subject+" as "+memory
        await client.send_message(message.channel, msgout)

    help_list.append(["purge_all!","DELETES ALL THE MESSAGES IN THE CHAN. THIS ACTION CAN NOT BE STOPPED!!!"])
    if ((bot_command+'purge_all!') in msgin[0]):
        counter = 0
        async for message in client.logs_from(message.channel, limit=999999999):
            if message.author != "SuperUser":
                await client.delete_message(message)
                counter += 1
        msgout = tag+" STAY FRESH"
        await client.send_message(message.channel, msgout)

    help_list.append(["wiki","searches wikipedia"])
    if ((bot_command+'wiki') in msgin[0]):
        r = requests.get("https://en.wikipedia.org/w/api.php?action=opensearch&search="+' '.join(msgin[1:])+"&limit=1&namespace=0&format=json");
        msgout = json.loads(r.text)
        msgout = tag+str(msgout[3]).strip("[\"']")
        await client.send_message(message.channel, msgout)

    help_list.append(["google","I'm feeling lucky"])
    if ((bot_command+'google') in msgin[0]):
        r = requests.get("http://www.google.com/search?q="+' '.join(msgin[1:])+"&btnI");
        msgout = r.url
        msgout = tag+str(msgout)
        await client.send_message(message.channel, msgout)

    help_list.append(["test","This is just a test, outputs the second argument."])
    if ((bot_command+'test') in msgin[0]):
        msgout = tag+msgin[1]
        await client.send_message(message.channel, msgout)

    help_list.append(["add","adds two numbers. \nExample: add 1 2\nOutputs: 3"])
    if ((bot_command+'add') in msgin[0]):
        msgout = tag+str(int(msgin[1])+int(msgin[2]))
        await client.send_message(message.channel, msgout)

    help_list.append(["is X cool?","X being any single word. Question mark is superficial."])
    if ((bot_command+'is') in msgin[0]) and ('cool' in msgin[2]):
        msgout = "Maybe... but {0.author.mention} is actually quite lame.".format(message)
        await client.send_message(message.channel, msgout)

    help_list.append(["Hi zb1","Say hi."])
    if ((bot_command+'hi') in msgin[0]):
        msgout = "Hello {0.author.mention}!".format(message)
        await client.send_message(message.channel, msgout)

    help_list.append(["flip","Flips a coin.\nExample: flip\nOutput: HEADS\nAlso supports the commans 'flip a coin' and 'flip a bitcoin'. However I do not recommend the last one due to its unstable nature."])
    if ((bot_command+'flip') in msgin[0]):
        if ('bitcoin' in msgin[1]):
            msgout = tag+random.choice(['I fliped a Bitcoin and it landed on \n\nHEADS.','I fliped a Bitcoin and it landed on \n\nTAILS.', 'I flipped a Bitcoin and it landed on its side and just kind of sat there. What are these things made out of anyways??'])
            await client.send_message(message.channel, msgout)
        elif ('coin' in msgin[1]):
            msgout = tag+random.choice(['I fliped a coin and it landed on \n\nHEADS.','I fliped a coin and it landed on \n\nTails.'])
        else:
            msgout = tag+random.crhoice(['\nHEADS.','\nTails.'])

    help_list.append(["choose","Helps you make a choice. \nExample: choose Starcraft Unreal CS:GO\nOutput: Starctaft"])
    if ((bot_command+'choose') in msgin[0]):
        print("choose")
        msgin = msgin[1:]
        print(msgin)
        msgout = tag+"Choosing from: "+', '.join(msgin)+"\n"+random.choice(msgin)
        await client.send_message(message.channel, msgout)

    help_list.append(["roll","Example: roll 1d3"])
    if ((bot_command+'roll') in msgin[0]):
        msgin = msgin[1].split("d")
        result = ""
        results = ""
        for x in range(int(msgin[0])):
            result = random.randrange( 0, int(msgin[1]) ) +1
            results += str(result)+"\n"
        msgout = tag+results
        await client.send_message(message.channel, msgout)


    help_list.append(["bored","Just don't."])
    if ((bot_command+'bored') in msgin[0]):
        if len(msgin) > 1:
            amt = msgin[1]
        else:
            amt = 1
        for x in range(int(amt)):
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            link = "https://imgur.com/"+key+".jpg"
            try:
                r = requests.get(link)
                
                while r.url == "https://i.imgur.com/removed.png":
                    print("BAD LINK")
                    key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                    link = "https://imgur.com/"+key+".jpg"
                    r = requests.get(link)
                    print(r.url)
                    
                # prints the int of the status code. Find more at httpstatusrappers.com :)
            except requests.ConnectionError:
                print("failed to connect")
            
            msgout = r.url
            await client.send_message(message.channel, msgout)


    help_list.append(["!mock","Just don't."])
    if ((bot_command+'!mock') in msgin[0]):
        mock = not mock
        msgout = 'mock = ' + str(mock)
        await client.send_message(message.channel, msgout, tts=True)

    help_list.append(["help","Displays Help!"])
    if ((bot_command+'help') in msgin[0]):
        msgout = "```\nYET ANOTHER DISCORD BOT v0.3\n--------\n"
        for x in sorted(help_list):
            msgout += bot_command+':\n'.join(x).replace("\n", "\n--")+"\n\n"
        msgout += "\n```"
        await client.send_message(message.channel, msgout)

    if (mock == True):
        m = ''.join(random.choice((str.upper,str.lower))(x) for x in message.content)
        m = "*"+m+"*"
        await client.send_message(message.channel, m, tts=True)


#urllib.request.urlopen("http://example.com/foo/bar").read()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



client.run('MzUwNTgyMjQyOTg2NDI2MzY4.DQOJng.1a3SbxWG15tA2clq0EQVYwS8bBY')

