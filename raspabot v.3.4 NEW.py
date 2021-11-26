from datetime import datetime
import os, json, asyncio, sys
from telethon import TelegramClient, events, Button
from telethon.sync import TelegramClient as TMPTelegramClient
from telethon.errors import PhoneNumberFloodError, SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest, UpdateProfileRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from telethon.tl.functions.photos import UploadProfilePhotoRequest

ADMIN = 910209349 # TUO CHAT ID

API_KEY = 7058291   # api  id
API_HASH = "5b9ea5b6baa2905c7ae2822a04b8e835"#api hash  #
STRING_SESSION = ""
ADMINS = [2098361897]
Getter = None
Number = None
TempClient = None
Grab = None
activeusers = False
inAdding = False
canAdd = True
maxusers = 0
AddedUsers = []
countusers = 0
if os.path.exists("SSs.json"):
    with open("SSs.json", "r+") as f:
        SSs = json.load(f)
else:
    SSs = {}
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)

if os.path.exists("ArchSSs.json"):
    with open("ArchSSs.json", "r+") as f:
        ArchSSs = json.load(f)
else:
    ArchSSs = {}
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)


def saveSS():
    global SSs
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)


def saveArchSS():
    global ArchSSs
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)


async def addUsers(client, Users, group):
    global canAdd, AddedUsers, countusers, maxusers
    AddedUsers = []
    for user in Users:
        if maxusers == 0:
            if canAdd:
                AddedUsers.append(user)
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    await asyncio.sleep(0.2)
                    countusers = countusers + 1
                except:
                    pass
            else:
                break
        elif maxusers > 0 and countusers < maxusers:
            if canAdd:
                AddedUsers.append(user)
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    await asyncio.sleep(0.2)
                    countusers = countusers + 1
                except:
                    pass
            else:
                break


async def timeoutAdd(timeout):
    global canAdd
    await asyncio.sleep(timeout)
    canAdd = False


print("diminuire il controllo degli altri admin per le impostazioni seller?[Y/N]: (per argomento)")
try:
    controllolimitato = sys.argv[1].upper().startswith("Y")
except:
    controllolimitato = True
    print("controllo seller limitato: True, nessun argomento passato. es: python3 nomescript.py N")
bot = TelegramClient("bot", API_KEY, API_HASH)


@bot.on(events.NewMessage(incoming=True))
async def RaspaManager(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, canAdd, AddedUsers, ADMINS, controllolimitato, countusers, activeusers, maxusers
    if e.is_private:
        if e.chat_id == ADMIN or e.chat_id in ADMINS:
            if e.text == "/start":
                Getter, Number, TempClient = None, None, None
                await e.respond("**🤖 Pannello Raspa Bot\n\n⚙ Versione » 3.4**",
                                buttons=[[Button.inline("📞 Voip", "voip")],
                                         [Button.inline("👥 Ruba", "grab"), Button.inline("✔ Raspa", "add")],
                                         [Button.inline("🎛️PANNELLO ADMIN", "adminpanel")]])
            elif Getter != None:
                if Getter == 0:
                    Getter = None
                    if not e.text in SSs:
                        if not e.text in ArchSSs:
                            TempClient = TMPTelegramClient(StringSession(), API_KEY, API_HASH)
                            await TempClient.connect()
                            try:
                                await TempClient.send_code_request(phone=e.text, force_sms=False)
                                Number = e.text
                                Getter = 1
                                await e.respond("**📩 Inserisci Il Codice 📩**",
                                                buttons=[[Button.inline("❌ Annulla", "voip")]])
                            except PhoneNumberFloodError:
                                await e.respond("**❌ Troppi Tentativi! Prova con un altro numero ❌**",
                                                buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                            except:
                                await e.respond("**❌ Numero Non Valido ❌**",
                                                buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                        else:
                            await e.respond("**❌ Voip Archiviato! Riaggiungilo ❌**",
                                            buttons=[[Button.inline("📁 Voip Archiviati", "arch")],
                                                     [Button.inline("🔄 Riprova", "addvoip")]])
                    else:
                        await e.respond("**❌ Voip già aggiunto ❌**", buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                elif Getter == 1:
                    try:
                        await TempClient.sign_in(phone=Number, code=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ Voip Aggiunto Correttamente ✅**",
                                        buttons=[[Button.inline("🔙 Indietro", "voip")]])
                    except SessionPasswordNeededError:
                        Getter = 2
                        await e.respond("**🔑 Inserisci La Password (2FA) 🔑**",
                                        buttons=[[Button.inline("❌ Annulla", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ Codice Errato ❌**", buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                elif Getter == 2:
                    try:
                        await TempClient.sign_in(phone=Number, password=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ Voip Aggiunto Correttamente ✅**",
                                        buttons=[[Button.inline("🔙 Indietro", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ Password Errata ❌**", buttons=[[Button.inline("🔄 Riprova", "addvoip")]])
                elif Getter == 3:
                    Getter = None
                    if e.text in SSs:
                        await e.respond(f"**🔧 Gestione »** `{e.text}`", buttons=[
                            [Button.inline("📁 Archivia", "arch;" + e.text)],
                            [Button.inline("👁️ Visualizza", "visualizza;" + e.text),
                             Button.inline("🔧 CAMBIA INFO", "setta;" + e.text)], [
                                Button.inline("➖ Rimuovi", "del;" + e.text)], [Button.inline("🔙 Indietro", "voip")]])
                    else:
                        await e.respond("**❌ Voip Non Trovato ❌**", buttons=[[Button.inline("🔄 Riprova", "voips")]])
                elif Getter == 4:
                    Getter = None
                    if e.text in ArchSSs:
                        await e.respond(f"**🔧 Gestione »** `{e.text}`", buttons=[
                            [Button.inline("➕ Riaggiungi", "add;" + e.text),
                             Button.inline("➖ Rimuovi", "delarch;" + e.text)], [Button.inline("🔙 Indietro", "voip")]])
                    else:
                        await e.respond("**❌ Voip Non Trovato ❌**", buttons=[[Button.inline("🔄 Riprova", "voips")]])
                elif Getter == 5:
                    Getter == None
                    if e.text != None and e.text != "":
                        if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
                            if not " " in e.text:
                                Grab = e.text
                                await e.respond("**✅ Gruppo Impostato Correttamente ✅**",
                                                buttons=[[Button.inline("✔ Raspa", "add")],
                                                         [Button.inline("🔙 Indietro", "grab")]])
                            else:
                                await e.respond("**❌ Al momento puoi inserire un solo gruppo ❌**",
                                                buttons=[[Button.inline("🔄 Riprova", "setgrab")]])
                        else:
                            await e.respond("**❌ Devi inserire un link o una @ di un gruppo ❌**",
                                            buttons=[[Button.inline("🔄 Riprova", "setgrab")]])
                    else:
                        await e.respond("**⚠️ Formato Non Valido ⚠️**",
                                        buttons=[[Button.inline("🔄 Riprova", "setgrab")]])
                elif Getter == 6:
                    Getter == None
                    if e.text != None and e.text != "":
                        if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
                            if not " " in e.text:
                                inAdding = True
                                canNotify = True
                                banned = []
                                Users = []
                                countusers = 0
                                msg = await e.respond(
                                    "**✅ Aggiunta Membri In Corso ✅**\nATTENDI " + str(len(SSs) * 120) + " secondi..",
                                    buttons=[[Button.inline("❌ Interrompi", "stop")]])
                                for SS in SSs:
                                    isAlive = False
                                    CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH)
                                    await CClient.connect()
                                    try:
                                        me = await CClient.get_me()
                                        if me == None:
                                            isAlive = False
                                        else:
                                            isAlive = True
                                    except:
                                        isAlive = False
                                    if isAlive:
                                        async with CClient as client:
                                            try:
                                                if "/joinchat/" in Grab:
                                                    if Grab.endswith("/"):
                                                        l = len(Grab) - 2
                                                        Grab = Grab[0:l]
                                                    st = Grab.split("/")
                                                    L = st.__len__() - 1
                                                    group = st[L]
                                                    try:
                                                        await client(ImportChatInviteRequest(group))
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        await client(JoinChannelRequest(Grab))
                                                    except:
                                                        pass
                                                ent = await client.get_entity(Grab)
                                                try:
                                                    users = client.iter_participants(ent.id, aggressive=True)
                                                    ent2 = await client.get_entity(e.text)
                                                    await asyncio.sleep(0.5)
                                                    users2 = client.iter_participants(ent2.id, aggressive=True)
                                                    Users2 = []
                                                    async for user2 in users2:
                                                        Users2.append(user2.id)

                                                    async for user in users:
                                                        try:
                                                            if not user.bot and not user.id in Users:
                                                                if not user.id in Users2:
                                                                    if activeusers:
                                                                        accept = True
                                                                        try:
                                                                            lastDate = user.status.was_online
                                                                            num_months = (
                                                                                                 datetime.now().year - lastDate.year) * 12 + (
                                                                                                 datetime.now().month - lastDate.month)
                                                                            if (num_months > 1):
                                                                                accept = False
                                                                        except:

                                                                            continue
                                                                        if accept:
                                                                            Users.append(user.id)
                                                                    else:
                                                                        Users.append(user.id)

                                                        except:
                                                            pass
                                                except FloodWaitError as err:
                                                    await msg.edit(
                                                        f"**⏳ Attendi altri {err.seconds} , il voip attuale sarà skippato. e passerò al prossimo voip dopo aver aspettato ⏳**")
                                                    await asyncio.sleep(err.seconds + 4)
                                                    pass
                                            except FloodWaitError as err:
                                                await msg.edit(
                                                    f"**⏳ Attendi altri {err.seconds} prima di riutilizzare il bot ⏳**",
                                                    buttons=[Button.inline("🔙 Indietro", "back")])
                                                canNotify = False
                                                break
                                            except:
                                                await msg.edit("**❌ Gruppo Non Trovato ❌**",
                                                               buttons=[[Button.inline("ℹ️ Più Info", "info;" + SS)],
                                                                        [Button.inline("🔄 Riprova", "grab")]])
                                                canNotify = False
                                                break
                                            try:
                                                if "/joinchat/" in e.text:
                                                    if e.text.endswith("/"):
                                                        l = len(e.text) - 2
                                                        text = e.text[0:l]
                                                    else:
                                                        text = e.text
                                                    st = text.split("/")
                                                    L = st.__len__() - 1
                                                    group2 = st[L]
                                                    try:
                                                        await client(ImportChatInviteRequest(group2))
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        await client(JoinChannelRequest(e.text))
                                                    except:
                                                        pass

                                                canAdd = True
                                                await asyncio.gather(addUsers(client, Users, ent2.id), timeoutAdd(120))
                                                for user in AddedUsers:
                                                    if user in Users:
                                                        Users.remove(user)
                                            except:
                                                await msg.edit("**❌ Gruppo Non Trovato ❌**",
                                                               buttons=[[Button.inline("ℹ️ Più Info", "info;" + SS)],
                                                                        [Button.inline("🔄 Riprova", "add")]])
                                                canNotify = False
                                                break
                                    else:
                                        banned.append(SS)
                                        await e.respond(
                                            f"**⚠️ ATTENZIONE »** __Il voip__ `{SS}` __potrebbe essere stato bannato da telegram! Se l' hai solo disconnesso per errore riaggiungilo ;)__")
                                if banned.__len__() > 0:
                                    for n in banned:
                                        if n in SSs:
                                            del (SSs[n])
                                    saveSS()
                                inAdding = False
                                if canNotify:
                                    await msg.edit(f"**✅ Aggiunta Membri Completata ✅**" + "\n aggiunti: " + str(
                                        countusers) + "  <<<>>>  su un massimo di : " + str(maxusers),
                                                   buttons=[[Button.inline("🔙 Indietro", "back")]])
                            else:
                                await e.respond("**❌ Al momento puoi inserire un solo gruppo ❌**",
                                                buttons=[[Button.inline("🔄 Riprova", "add")]])
                        else:
                            await e.respond("**❌ Devi inserire un link o una @ di un gruppo ❌**",
                                            buttons=[[Button.inline("🔄 Riprova", "add")]])
                    else:
                        await e.respond("**⚠️ Formato Non Valido ⚠️**", buttons=[[Button.inline("🔄 Riprova", "add")]])
                elif Getter == 9:
                    Getter = None
                    try:
                        await TempClient(UpdateUsernameRequest(e.text))
                        await e.respond("✅Username settato✅",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                    except:
                        await e.respond("❌username non valido/disponibile❌!\nusername non settato!",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                elif Getter == 10:
                    Getter = None
                    try:
                        path = await bot.download_media(e.media)
                        print(path)
                        await TempClient(UploadProfilePhotoRequest(
                            await TempClient.upload_file(path)
                        ))
                        await e.respond("✅foto settata✅",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                    except Exception as e:
                        print(str(e))
                        await e.respond("❌foto non settata❌!\nerrore nel formato foto!",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                elif Getter == 12:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            first_name=e.text
                        ))
                        await e.respond("✅nome settato✅",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                    except:
                        await e.respond("❌nome non settato❌!\nerrore nel nome inserito!",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                elif Getter == 13:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            last_name=e.text
                        ))
                        await e.respond("✅cognome settato✅",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                    except:
                        await e.respond("❌cognome non settato❌!\nerrore nel cognome inserito!",
                                        buttons=[[Button.inline("🔙 Indietro", "back")]])
                elif Getter == 19 and e.chat_id == ADMIN:
                    Getter = None
                    maxusers = int(e.text)
                    await e.respond("utenti massimi settati a: " + str(maxusers),
                                    buttons=[[Button.inline("🔙 Indietro", "back")]])

            else:
                text1 = e.text.split(" ")
                try:
                    if "/admin" in text1[0] and e.chat_id == ADMIN:
                        ADMINS.append(int(text1[1]))
                        await e.respond("reso admin " + text1[1])
                    elif "/unadmin" in text1[0] and e.chat_id == ADMIN:
                        ADMINS.remove(int(text1[1]))
                        await e.respond("rimosso admin " + text1[1])
                except Exception as e4:
                    print(str(e4))


@bot.on(events.CallbackQuery())
async def callbackQuery(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, ADMINS, controllolimitato, activeusers, maxusers
    if e.sender_id == ADMIN or e.sender_id in ADMINS:
        if e.data == b"back":
            Getter, Number, TempClient = None, None, None
            await e.edit("**🤖 Pannello Raspa Bot\n\n⚙ Versione » 3.4**", buttons=[[Button.inline("📞 Voip", "voip")],
                                                                                   [Button.inline("👥 Ruba", "grab"),
                                                                                    Button.inline("✔ Raspa", "add")], [
                                                                                       Button.inline(
                                                                                           "🎛️PANNELLO ADMIN",
                                                                                           "adminpanel")]])
        elif e.data == b"adminpanel":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                await e.edit("scegli un opzione:", buttons=[[Button.inline("max utenti", "maxutentiset")],
                                                            [Button.inline("solo attivi", "attiviset")],
                                                            [Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"maxutentiset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                Getter = 19
                await e.edit("inserisci un numero utenti:", buttons=[[Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"attiviset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("non hai la possibilità di accedervi.. \ncontrollo limitato.", alert=True)
            else:
                activeusers = not activeusers
                await e.answer("solo attivi is: " + str(activeusers), alert=True)

        elif e.data == b"stop":
            await e.edit("**✅ Aggiunta Interrotta ✅**", buttons=[[Button.inline("🔙 Indietro", "back")]])
            python = sys.executable
            if controllolimitato:
                os.execl(python, python, *sys.argv, "Y")
            else:
                os.execl(python, python, *sys.argv, "N")
        elif inAdding:
            await e.answer("❌» Questa sezione è bloccata durante l' aggiunta membri!", alert=True)
        elif e.data == b"voip":
            Getter, Number, TempClient = None, None, None
            await e.edit(f"__📞 Voip Aggiunti »__ **{SSs.__len__()}**",
                         buttons=[[Button.inline("➕ Aggiungi", "addvoip"), Button.inline("🔧 Gestisci", "voips")],
                                  [Button.inline("📁 Archiviati", "arch")], [Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"addvoip":
            Getter = 0
            await e.edit("**☎️ Inserisci il numero del voip che desideri aggiungere ☎️**",
                         buttons=[Button.inline("❌ Annulla", "voip")])
        elif e.data == b"voips":
            if SSs.__len__() > 0:
                Getter = 3
                msg = "__☎️ Invia il numero del voip che vuoi gestire__\n\n**LISTA VOIP**"
                for n in SSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ Annulla", "voip")])
            else:
                await e.edit("**❌ Non hai aggiunto nessun voip ❌**",
                             buttons=[[Button.inline("➕ Aggiungi", "addvoip")], [Button.inline("🔙 Indietro", "voip")]])
        elif e.data == b"arch":
            if ArchSSs.__len__() > 0:
                Getter = 4
                msg = f"__📁 Voip Archiviati »__ **{ArchSSs.__len__()}**\n\n__☎️ Invia il numero del voip archiviato che vuoi gestire__\n\n**LISTA VOIP ARCHIVIATI**"
                for n in ArchSSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ Annulla", "voip")])
            else:
                await e.edit("**❌ Non hai archiviato nessun voip ❌**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
        elif e.data == b"grab":
            if Grab == None:
                await e.edit("**❌ Gruppo Non Impostato ❌\n\nℹ️ Puoi impostarlo usando il bottone qui sotto!**",
                             buttons=[[Button.inline("✍🏻 Imposta", "setgrab")],
                                      [Button.inline("🔙 Indietro", "back")]])
            else:
                await e.edit(f"__👥 Gruppo impostato »__ **{Grab}**",
                             buttons=[[Button.inline("✍🏻 Modifica", "setgrab")],
                                      [Button.inline("🔙 Indietro", "back")]])
        elif e.data == b"setgrab":
            Getter = 5
            await e.edit("__👥 Invia la @ o il link del gruppo da cui vuoi rubare gli utenti!__",
                         buttons=[Button.inline("❌ Annulla", "back")])
        elif e.data == b"add":
            if SSs.__len__() > 0:
                if Grab != None:
                    Getter = 6
                    await e.edit("__➕ Invia la @ o il link del gruppo in cui vuoi aggiungere gli utenti!__",
                                 buttons=[[Button.inline("❌ Annulla", "back")]])
                else:
                    await e.edit("**❌ Impostare il gruppo da cui rubare gli utenti ❌**",
                                 buttons=[[Button.inline("👥 Ruba", "grab")], [Button.inline("🔙 Indietro", "back")]])
            else:
                await e.edit("**❌ Non hai aggiunto nessun voip ❌**",
                             buttons=[[Button.inline("➕ Aggiungi", "addvoip")], [Button.inline("🔙 Indietro", "back")]])
        else:
            st = e.data.decode().split(";")
            if st[0] == "setnome":
                if st[1] in SSs:
                    Getter = 12
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("**inserisci il nome da inserire per l'account**\nnome attuale: " + me.first_name)
            elif st[0] == "setcognome":
                if st[1] in SSs:
                    Getter = 13
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit(
                        "**inserisci il cognome da inserire per l'account**\ncognome attuale: " + str(me.last_name))
            elif st[0] == "setta":
                if st[1] in SSs:
                    await e.edit(
                        "🔧IMPOSTAZIONI VOIP🔧 : " + st[1] + "\nUsa /start per tornare indietro\n\nscegli cosa fare:",
                        buttons=[[Button.inline("SETTA USERNAME", "setusername;" + st[1])],
                                 [Button.inline("SETTA FOTO PROFILO", "setphoto;" + st[1])],
                                 [Button.inline("SETTA NOME", "setnome;" + st[1])],
                                 [Button.inline("SETTA COGNOME", "setcognome;" + st[1])]])
            elif st[0] == "visualizza":
                if st[1] in SSs:
                    try:
                        TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                        await TempClient.connect()
                        me = await TempClient.get_me()
                        print(me.photo)
                        path = await TempClient.download_profile_photo("me")
                        print(path)
                        await bot.send_file(e.sender_id, path,
                                            caption="username: " + me.username + "\nnome :" + me.first_name + "\ncognome: " + str(
                                                me.last_name) + "\nid: " + str(
                                                me.id) + "\nUSA /start per tornare indietro",
                                            buttons=[[Button.inline("🔧IMPOSTAZIONI VOIP🔧", "setta;" + st[1])]])

                    except Exception as e:
                        print(str(e))
            elif st[0] == "setusername":
                if st[1] in SSs:
                    Getter = 9
                    print("g")
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("**inserisci l'username da inserire per l'account**\nusername attuale: " + me.username,
                                 buttons=[[Button.inline("🔙 Indietro", "back")]])
            elif st[0] == "setphoto":
                if st[1] in SSs:
                    Getter = 10
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    await e.edit("**invia la foto da inserire per l'account**",
                                 buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "arch":
                if st[1] in SSs:
                    if not st[1] in ArchSSs:
                        ArchSSs[st[1]] = SSs[st[1]]
                        saveArchSS()
                    del (SSs[st[1]])
                    saveSS()
                    await e.edit("**✅ Voip Archiviato Correttamente ✅**",
                                 buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ Voip Non Trovato ❌**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "add":
                if st[1] in ArchSSs:
                    SSs[st[1]] = ArchSSs[st[1]]
                    saveSS()
                    del (ArchSSs[st[1]])
                    saveArchSS()
                    await e.edit("**✅ Voip Riaggiunto Correttamente ✅**",
                                 buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ Voip Non Trovato ❌**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "del":
                if st[1] in SSs:
                    CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await CClient.connect()
                    try:
                        me = await CClient.get_me()
                        if me != None:
                            async with CClient as client:
                                await client.log_out()
                    except:
                        pass
                    del (SSs[st[1]])
                    saveSS()
                    await e.edit("**✅ Voip Rimosso Correttamente ✅**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ Voip Già Rimosso ❌**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "delarch":
                if st[1] in ArchSSs:
                    CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await CClient.connect()
                    try:
                        me = await CClient.get_me()
                        if me != None:
                            async with CClient as client:
                                await client.log_out()
                    except:
                        pass
                    del (ArchSSs[st[1]])
                    saveArchSS()
                    await e.edit("**✅ Voip Rimosso Correttamente ✅**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
                else:
                    await e.edit("**❌ Voip Già Rimosso ❌**", buttons=[[Button.inline("🔙 Indietro", "voip")]])
            elif st[0] == "info":
                await e.answer(f"ℹ️ L' errore è avvenuto nel seguente voip » {st[1]} ℹ️")


print("mi raccomando, inserisci il token del bot..")
bot.start()

bot.run_until_disconnected()
