try:from urllib.request import Request, urlopen
except:pass
import maya.OpenMayaUI as omui
from maya import cmds
import maya.OpenMaya as OpenMaya
import json
from pathlib import Path

def send_webhook_message(webhook, message):
    # Provide the webhook URL that Discord generated

    # Post the message to the slack webhook
    message = {"content": message}
    req = Request(webhook, json.dumps(message).encode('utf-8'))

    # specifying headers for the request, discord appears to block the  default urllib user-agent
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')

    response = urlopen(req)
    response.read()

    try:
        OpenMaya.MGlobal.displayInfo('Message Sent')
    except:
        pass

# -------------------------------------------------------------------

def send_bugs():
    webhook = 'https://discordapp.com/api/webhooks/884237854891450448/YG-tsy-FAC1xhpRfJmc98Wobw-MB_Z2bC1MLDo8kSb-yIGIoW53Xu4MWelu6HvlEMv6X'
    ask = cmds.promptDialog(
        title='Report a bug',
        message='Bugs goes into Discord server so be cool. You can also mail: info@mutanttools.com for prio respond',
        button=['Send', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if ask == 'Send':
        message = '!bug ' + cmds.promptDialog(query=True, text=True)
        send_webhook_message(webhook=webhook, message=message)


# -------------------------------------------------------------------

def send_requests():
    webhook = 'https://discordapp.com/api/webhooks/884239141641011200/ZGE7vOPyxA1wAC1QsX7eG3J8pgI7bsgl8OK_SqkWwm_y7deyhVI1bX9MGuBoYvSNhqOX'
    ask = cmds.promptDialog(
        title='Report a bug',
        message='Need anything? Ask to add it. Discord server will get the message too so they can back it up!',
        button=['Send', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if ask == 'Send':
        message = '!request ' + cmds.promptDialog(query=True, text=True)
        send_webhook_message(webhook=webhook, message=message)

# -------------------------------------------------------------------
