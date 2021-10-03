import slack
import os
import random
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from coolname import generate

team_members = ['Ansel', 'Noe', 'Kyle', 'Milo', 'Meridith', 'Tori', 'David', 'Travis']
random.shuffle(team_members)
it = iter(team_members)
pairs = [' & '.join([x, next(it)]) for x in it]
team_names = [' '.join(x.capitalize() for x in generate(2)) for pair in pairs]
team_combos = [f'•  {team_names[i]}:\t{pairs[i]}\n' for i in range(len(pairs))]

print(''.join(team_combos))

# table = [team_names, pairs]

# output = ''
# for row in table:
#     output+=("{:<20} " * len(pairs)).format(*row) + '\n'



load_dotenv()

app = Flask(__name__)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client.chat_postMessage(channel="#test", text=''.join(team_combos))


# if __name__ == "__main__":
#     app.run(debug=True)