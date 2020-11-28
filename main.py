import discord
import os
import sys
import psutil
import logging
import time
from threads import ThreadManager

tm = ThreadManager()


#lista(int) -> processID
#crear sesion -> id a lista
#commando -> Escribir a consola con id lista


client = discord.Client()
#Kills all the bot threads
def restart_program():
	try:
		p = psutil.Process(os.getpid())
		for handler in p.open_files() + p.connections():
			os.close(handler.fd)
	except Exception as e:
		logging.error(e)

	python = sys.executable
	os.execl(python, python, *sys.argv)

@client.event
async def on_message(message):
    # Client is not the sender
    if client.user.id != message.author.id:
        channel = client.get_channel(message.channel.id)
        if message.content.startswith("!echo "):
            await channel.send(message.content[6:])
            return
        #Display current session name for this channel
        if message.content =="!session":
            # TM: send session if exists to Client
            await channel.send(await tm.get_session_name(message.channel.id))
            return
        #Create new session for this channel
        if message.content.startswith("!session -n"):
            # Client: send channel to TM
            name = message.content[12:]
            if len(name) < 1:
                await channel.send("Usage: !session -n \'name\'.")
            else:
                await tm.start_session(name, message.author.id, message.channel.id)
                await channel.send('Session '+name+' successfully created on this channel.')
            return
        #Clear current session for this channel
        if message.content.startswith("!session -c"):
            # Client: send TM order to clear the session for this channel
            await tm.clear_session(message.author.id, message.channel.id)
            return
        #Remove current session for this user
        if message.content.startswith("!session -r"):
            # Client: Remove the session for the current channel
            await tm.delete_session(message.author.id, message.channel.id)
            return
        #Add user to the session of the current channel
        if message.content.startswith("!user -a"):
            # Client: Send TM order to add user to the session
                    # Remove user from the session of the current channel
            name = message.content[12:]
            if len(name) < 1:
                await channel.send("Usage: !session -a \'@user\'.")
            print(message.content)
            print(message.author.id)
            return
        if message.content.startswith("!user -r"):
            # Client: Send TM order to remove user to the session
                    # Returns the list of users in the session
            return
        if message.content.startswith("!user -l"):
            #TM: Send client the list of users in the session
            return
        if message.content.startswith("!save"):
            if len(message.content[6:]) == 0:
                await channel.send("Usage: !save \'name\'.")
            else:
                result = await tm.save_session(message.content[6:], message.channel.id, message.author.id)
                await channel.send(result)
            return
        if message.content == '!restart':
            await channel.send('Opsie Wopsie, we made a fucky wucky and m-master is updating my code >/////<')
            print('Restarting at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            await client.logout()
            restart_program()
        if message.content == 'asas':
            await channel.send('Good night, nyaaster! ')
            time.sleep(10)
        # Client -> ThreadManager -> Run python command
        output = await tm.run_code(message.content, message.author.id, message.channel.id)
        if output:
            await channel.send('```\n'+output+'```')

@client.event
async def on_voice_state_update(before, after):
    return

@client.event
async def on_ready():
	print('Log in as')
	print(client.user.name)
	print('------')

if __name__ == '__main__':
    with open('./TOKEN', 'r') as f:
        TOKEN = f.readline()
    client.run(TOKEN)
