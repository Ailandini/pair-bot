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


@app.route('/assign-team', methods=['GET','POST'])
def assign_team():
    data = request.form
    print(data.get('text'))
    team_members = data.get('text').split(', ')
    teams = build_teams(team_members, [])
    client.chat_postMessage(channel="#test", text=teams)
    return Response(), 200


# channels = []
# try:
#     for result in client.users_conversations():
#         channels = [channel['id'] for channel in result["channels"]]
            
# except SlackApiError as e:
#     print(f"Error: {e}")

# for channel_id in channels:
#     client.chat_scheduleMessage(
#         channel=channel_id,
#         text=teams,
#         post_at=schedule_timestamp
#     )

if __name__ == "__main__":
    app.run(debug=True)
