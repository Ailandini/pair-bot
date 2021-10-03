
import random
from coolname import generate

def build_teams():
    team_members = ['Ansel', 'Noe', 'Kyle', 'Milo', 'Meridith', 'Tori', 'David', 'Travis']
    random.shuffle(team_members)

    it = iter(team_members)
    pairs = [' & '.join([x, next(it)]) for x in it]
    team_names = [' '.join(x.capitalize() for x in generate(2)) for pair in pairs]
    team_combos = [f'•  {team_names[i]}:\t{pairs[i]}\n' for i in range(len(pairs))]

    return ''.join(team_combos)