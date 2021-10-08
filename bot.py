import slack
import os
import time
import datetime
import pytz
from dotenv import load_dotenv
from flask import Flask, request, Response
from helpers.BuildTeams import build_teams
from helpers.Members import getMembers

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

def build_team_from_channel(data, without=False):
    team_members = data.get('text').split(' ') if without else []
    channel = data.get('channel_id')
    members = getMembers(channel)
    return build_teams(members, team_members)

@app.route('/assign-team', methods=['POST'])
def assign_team():
    data = request.form
    client.chat_postMessage(channel=data.get('channel_id'), text=build_team_from_channel(data))
    return Response(), 200

@app.route('/assign-team-without', methods=['POST'])
def assign_team_without():
    data = request.form
    client.chat_postMessage(channel=data.get('channel_id'), text=build_team_from_channel(data, True))
    return Response(), 200

# for channel_id in channels:
#     client.chat_scheduleMessage(
#         channel=channel_id,
#         text=teams,
#         post_at=schedule_timestamp
#     )

if __name__ == "__main__":
    app.run(debug=True)
