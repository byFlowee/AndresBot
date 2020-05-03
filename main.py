import discord
import signal
import ctypes
import os
import sys
import psutil
import logging
import subprocess
import threading
from AndresBot.threads import ThreadManager
from time import gmtime, strftime

tm = ThreadManager()

if __name__ == '__main__':
    TOKEN = 'NDI3NTQyNDUxODYzOTQ1MjM3.DZmEJg.hgWHLXsnDb0_dkymYbGuscE11HM'
    client = discord.Client()
    client.run(TOKEN)

#lista(int) -> processID
#crear sesion -> id a lista
#commando -> Escribir a consola con id lista

@client.event
async def on_message(message):
    # Client is not the sender
    if client.user.id != message.author.id:
        channel = client.get_channel(message.channel.id)
        if message.content.startswith("!echo "):
            await channel.send(message.content)
            return
        #Display current session name for this channel
        if message.content.startswith("!session"):
            # TM: send session if exists to Client
            await tm.get_session_name(message.channel.id)
            return
        #Create new session for this channel
        if message.content.startswith("!session -n"):
            # Client: send channel to TM
            name = message.content[12:]
            if len(name) < 1:
                await channel.send("Usage: !session -n \'name\'")
                return

            tm.start_session(name, message.author.id, message.channel.id)
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
            return
        # Remove user from the session of the current channel
        if message.content.startswith("!user -r"):
            # Client: Send TM order to remove user to the session
            return
        # Returns the list of users in the session
        if message.content.startswith("!user -l"):
            #TM: Send client the list of users in the session
            return

        # Client -> ThreadManager -> Run python command
        await tm.run_code(message.content, message.author.id, message.channel.id)

@client.event
async def on_voice_state_update(before, after):
    return

@client.event
async def on_ready():
	print('Log in as')
	print(client.user.name)
	#print(client.user.id)
	print('------')
    # Create a thread for session management