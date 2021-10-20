import ssl
import os
import mysql.connector
import time
import discord
from discord import channel
from discord.ext import commands

ssl._create_default_https_context = ssl._create_unverified_context
bot = commands.Bot(command_prefix='s!')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Syrax Web Forum"))
    for guild in bot.guilds:
       await guild.me.edit(nick="s! | Syrax Verifica    ")
    print('il bot è stato caricato perfettamente \nautore: Filippo Poma')
    

@bot.command()
async def verifica(ctx, *, arg):
    channel = bot.get_channel(881652067016523838)
    id = ctx.message.channel.id
    channeldm = bot.get_channel(id)
    if channeldm != channel:
        x = await channeldm.send('> {} '.format(ctx.message.author.mention) + '\n> {} ' .format('**CHAT SBAGLIATA**\n') + '> {}'.format('fai **s!verifica** ||{}|| su <#881652067016523838>').format(' **CODICE** '))
        time.sleep(9)
        await ctx.message.delete()
        await x.delete()
    else:
        mydb = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
        database = os.getenv("DATABASE")
        )
        #se esiste il codice
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id_utente FROM utente WHERE id_utente = %s" %(arg))
        myresult = mycursor.fetchall()
        if myresult:
            #se l'account è gia connesso
            id_utente = myresult[0][0]
            mycursor = mydb.cursor()
            mycursor.execute("SELECT connessione FROM utente WHERE id_utente = %s" %(id_utente))
            myresult = mycursor.fetchall()
            connessione_sy = myresult[0][0]
            if connessione_sy==False :
                pfp = ctx.message.author.avatar_url
                id_discord = ctx.message.author
                #update profilo
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE utente SET id_discord = '%s', profilo_img = '%s' WHERE id_utente = %s" %(id_discord,pfp,id_utente))
                mydb.commit()
                #update connessione
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE utente SET connessione = TRUE")
                mydb.commit()
                await ctx.message.delete()
                x = await channeldm.send('> {}'.format(ctx.message.author.mention) +'\n > {}'.format("**HA AGGIORNATO IL SUO ACCOUNT SYRAX**")+'\n > {}'.format("*ricorda di riloggare nell'account per poter vedere i cambiamenti*")+'\n > {}'.format('https://localhost/syraxcheck/web/php/login.php'))
            else:
                await ctx.message.delete()
                x = await channeldm.send('> {}'.format(ctx.message.author.mention)+'\n > {}'.format("**NON HAI ATTIVATO IL CODICE DELL'ACCOUNT**")+'\n > {}'.format("*premi su attiva il codice e copia il comando che ti appare su*")+"\n > {}".format("https://localhost/syraxcheck/web/php/impostazioni.php"))
                
        else:
            await ctx.message.delete()
            x = await channeldm.send('> {}'.format(ctx.message.author.mention)+'\n > {}'.format('**IL CODICE É SBAGLIATO VAI SU**')+'\n > {}'.format("https://localhost/syraxcheck/web/php/impostazioni.php"))


@verifica.error
async def verifica_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        id = ctx.message.channel.id
        channeldm = bot.get_channel(id)
        await ctx.message.delete()
        x = await channeldm.send('> {}'.format(ctx.message.author.mention)+'\n > {}'.format('**HA DIMENTICATO IL CODICE**\n')+'> {}'.format('fai **s!verifica** ||{}||').format(' **CODICE** ')+"su <#881652067016523838>")
        time.sleep(6)
        await x.delete()

if __name__== "__main__":
    bot.run(os.getenv("DPY"))
