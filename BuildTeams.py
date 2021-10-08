import random
from coolname import generate

def build_teams(team_members, OOO_members=[]):
    random.shuffle(team_members)
    team_members += _build_spirits(OOO_members)

    if len(team_members) % 2 != 0:
        team_members.append(f'Spirit of {_an_animal()}')

    it = iter(team_members)
    pairs = [' & '.join([x, next(it)]) for x in it]
    team_names = [' '.join(x.capitalize() for x in generate(2)) for pair in pairs]
    team_combos = _build_team_combos(team_names, pairs)
    

    return ''.join(team_combos)

def _build_spirits(OOO_members):
    return [f'Spirit of {member}' for member in OOO_members]


def _an_animal():
    animal = generate(2)[1].capitalize()
    return f'{_a_or_an(animal)} {animal}'

def _build_team_combos(team_names, pairs):
    team_combos = []
    for i in range(len(pairs)):
        team_combo = f'{team_names[i]}:\t{pairs[i]}\n'
        if _is_a_spirit_team(pairs[i]):
            team_combo = f'Spirit of {_a_or_an(team_combo)} {team_combo}'
        team_combo = f'•  {team_combo}'

        team_combos.append(team_combo)
    return team_combos

def _a_or_an(next_word):
    return 'an' if next_word[0] in ['A', 'E', 'I', 'O', 'U'] else 'a'

def _is_a_spirit_team(pairs):
    member = pairs.split(' & ')
    return 'Spirit' in member[0] and 'Spirit' in member[1]
