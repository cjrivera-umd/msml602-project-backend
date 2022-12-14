import csv
from datetime import datetime

SECONDS_FOR_8YEARS = 251596800
WC22_TEAMS = ['Qatar', 'Brazil', 'Belgium', 'France', 'Argentina', 'England', 'Spain', 'Portugal', 'Mexico',
        'Netherlands', 'Denmark', 'Germany', 'Uruguay', 'Switzerland', 'United States', 'Croatia', 
        'Senegal', 'Iran', 'Japan', 'Morocco', 'Serbia', 'Poland', 'South Korea', 'Tunisia', 'Cameroon',
        'Canada', 'Ecuador', 'Saudi Arabia', 'Ghana', 'Wales', 'Costa Rica', 'Australia']


def main():
    matches = get_matches()
    write_csv(matches)


def write_csv(matches):
    with open('preprocessed_results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)

        header = [
            'epoch',
            'home_team',
            'away_team',
            'tournament',
            'neutral',
            'home_team_win_percent',
            'away_team_win_percent',
            'winner'
        ]
        writer.writerow(header)

        for i, match in enumerate(matches):
            hteam = match['home_team']
            ateam = match['away_team']

            match_to_row = []
            for col in header:
                if col == 'home_team':
                    match_to_row.append(f'H-{match[col]}')
                elif col == 'away_team':
                    match_to_row.append(f'A-{match[col]}')
                elif col == 'neutral':
                    match_to_row.append('T' if match[col] == 'TRUE' else 'F')
                else:
                    match_to_row.append(match[col])
            
            writer.writerow(match_to_row)


def get_matches():
    matches = []
    with open('results.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            d = dict(row)

            hteam = d['home_team']
            ateam = d['away_team']

            if hteam not in WC22_TEAMS and ateam not in WC22_TEAMS: continue

            matches.append(d)

            hscore = d['home_score']
            ascore = d['away_score']
            if hscore == ascore:
                d['winner'] = 'Tie'
            elif hscore > ascore:
                d['winner'] = 'Home'
            else:
                d['winner'] = 'Away'

            date = datetime.strptime(row['date'], '%Y-%m-%d')
            epoch = date.timestamp()
            d['epoch'] = epoch

            limit = epoch - SECONDS_FOR_8YEARS
            hteam_wp, ateam_wp = get_win_percents(matches, hteam, ateam, limit)

            d['home_team_win_percent'] = hteam_wp
            d['away_team_win_percent'] = ateam_wp

    return matches


def get_win_percents(matches, hteam, ateam, limit):
    hteam_stats = {
        'total_games': 0,
        'total_wins': 0
    }
    ateam_stats = {
        'total_games': 0,
        'total_wins': 0
    }

    for match in reversed(matches[:-1]):
        # Break if limit exceeded
        if match['epoch'] < limit: break

        match_teams = [match['home_team'], match['away_team']]
        if hteam not in match_teams and ateam not in match_teams:
            continue

        if hteam in match_teams:
            hteam_stats['total_games'] += 1
            if (match['winner'] == 'Home' and hteam == match['home_team']) or (match['winner'] == 'Away' and hteam == match['away_team']):
                    hteam_stats['total_wins'] += 1

        if ateam in match_teams:
            ateam_stats['total_games'] += 1
            if (match['winner'] == 'Home' and ateam == match['home_team']) or (match['winner'] == 'Away' and ateam == match['away_team']):
                    ateam_stats['total_wins'] += 1


    hteam_wp = 0.0 if not hteam_stats['total_games'] else hteam_stats['total_wins'] / hteam_stats['total_games']
    ateam_wp = 0.0 if not ateam_stats['total_games'] else ateam_stats['total_wins'] / ateam_stats['total_games']
    return hteam_wp, ateam_wp


if __name__ == '__main__':
    main()