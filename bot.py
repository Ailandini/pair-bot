import slack
import os
import time
import datetime
import pytz
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from BuildTeams import build_teams

load_dotenv()
app = Flask(__name__)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

tomorrow = datetime.date.today()
scheduled_time = datetime.time(hour=1, minute=25)
schedule_timestamp = datetime.datetime.combine(tomorrow, scheduled_time).strftime('%s')


# def getChannels():
#     channels = []
#     try:
#         for result in client.users_conversations():
#             channels = [channel['id'] for channel in result["channels"]]

#     except SlackApiError as e:
#         print(f"Error: {e}")
#     return channels


BOT_ID = client.api_call("auth.test")['user_id']

def getMemberName(c, m):
    return client.users_info(channel=c, user=m)['user']['profile']['first_name'] or client.users_info(channel=c, user=m)['user']['profile']['name']

def getMemberNames(channel, members):
    member_names = [getMemberName(channel,m) for m in members]
    return member_names


def build_team_from_channel(data, without=False):
    team_members = data.get('text').split(' ') if without else []
    channel = data.get('channel_id')
    members = client.conversations_members(channel=channel)['members']
    members.remove(BOT_ID)
    member_names = getMemberNames(channel, members)
    return build_teams(member_names, team_members)

@app.route('/assign-team', methods=['POST'])
def assign_team():
    data = request.form
    channel = data.get('channel_id')
    client.chat_postMessage(channel=channel, text=build_team_from_channel(data))
    return Response(), 200

@app.route('/assign-team-without', methods=['POST'])
def assign_team_without():
    data = request.form
    channel = data.get('channel_id')
    client.chat_postMessage(channel=channel, text=build_team_from_channel(data, True))
    return Response(), 200

# for channel_id in channels:
#     client.chat_scheduleMessage(
#         channel=channel_id,
#         text=teams,
#         post_at=schedule_timestamp
#     )

if __name__ == "__main__":
    app.run(debug=True)
