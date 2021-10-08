import slack
import os

from dotenv import load_dotenv

load_dotenv()
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']

def _getMemberName(c, m):
    return client.users_info(channel=c, user=m)['user']['profile']['first_name'] or client.users_info(channel=c, user=m)['user']['profile']['name']

def _getMemberNames(channel, members):
    member_names = [_getMemberName(channel,m) for m in members]
    return member_names

def getMembers(channel):
    members = client.conversations_members(channel=channel)['members']
    members.remove(BOT_ID)
    member_names = _getMemberNames(channel, members)
    return member_names
