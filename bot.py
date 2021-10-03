import slack
import os
import time
import datetime
import pytz
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from BuildTeams import build_teams

load_dotenv()
app = Flask(__name__)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

teams = build_teams()

tomorrow = datetime.date.today()
scheduled_time = datetime.time(hour=1, minute=25)
schedule_timestamp = datetime.datetime.combine(tomorrow, scheduled_time).strftime('%s')

print(schedule_timestamp)

channels = []
try:
    for result in client.users_conversations():
        channels = [channel['id'] for channel in result["channels"]]
            
except SlackApiError as e:
    print(f"Error: {e}")

for channel_id in channels:
    client.chat_scheduleMessage(
        channel=channel_id,
        text=teams,
        post_at=schedule_timestamp
    )

if __name__ == "__main__":
    app.run(debug=True)
