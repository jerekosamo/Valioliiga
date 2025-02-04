
import requests
from scipy.stats import poisson
import tkinter as tk
import Keys

def return_rate(koti, tasapeli, vieras):
    # Calculates the precentage of return, aiming for 100% for the best return
    # If numbers are multipliers ie. > 1.0 they are changed to precent. If numbers are in precent format they  are added together.
    if koti > 1:
        x = (1/koti) + (1/tasapeli) + (1/vieras)
    else:
        x = (koti + tasapeli + vieras)

    return (1 / x)

def lambda_multiplier(games, goals, conceded):
    kerroin = (goals / games) / (conceded / games)
    return kerroin

def poisson_multiplier(lambda_home, lambda_away):
    # Calculate the probability of each team scoring a specific number of goals
    prob_home = [poisson.pmf(i, lambda_home) for i in range(6)]
    prob_away = [poisson.pmf(i, lambda_away) for i in range(6)]

    # Calculate the probability of each scoreline
    scorelines = [[i, j] for i in range(6) for j in range(6)]
    scoreline_probabilities = [prob_home[i] * prob_away[j] for i, j in scorelines]

    # Calculate the probability of each outcome
    team1_wins = sum(
        [scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] > scorelines[i][1]])
    draw = sum([scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] == scorelines[i][1]])
    team2_wins = sum(
        [scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] < scorelines[i][1]])

    # Normalize the probabilities
    total_probability = team1_wins + team2_wins + draw
    team1_win_prob = team1_wins / total_probability
    team2_win_prob = team2_wins / total_probability
    draw_prob = draw / total_probability

    # Print the probabilities
    #print(f"Team 1 win probability: {team1_win_prob:.2%}", round(1 / team1_win_prob, 2))
    #print(f"Team 2 win probability: {team2_win_prob:.2%}", round(1 / team2_win_prob, 2))
    #print(f"Draw probability: {draw_prob:.2%}", round(1 / draw_prob, 2))

    return (team1_win_prob, draw_prob, team2_win_prob)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    f = open("matches.txt", "w")
    # uri takes data of selected gameweeks matches to count the probabilities
    uri = 'https://api.football-data.org/v4/competitions/PL/matches?matchday=25'
    # uri1 takes the data of the selected premier league seasons played matches
    uri1 = 'https://api.football-data.org/v4/competitions/PL/standings?season=2024'
    headers = {'X-Auth-Token': Keys.API_KEY}

    games = 0
    goals = 0
    conceded = 0
    points = 0
    points_home = 0
    games_home = 0
    goals_home = 0
    conceded_home = 0
    points_away = 0
    games_away = 0
    goals_away = 0
    conceded_away = 0
    opp_games = 0
    opp_goals = 0
    opp_conceded = 0
    opp_points = 0

    response1 = requests.get(uri1, headers=headers)
    response = requests.get(uri, headers=headers)

    for match in response.json()['matches']:
        #print (match)
        match_data = match
        # Extract relevant information from data
        home_team = match_data['homeTeam']['name']
        away_team = match_data['awayTeam']['name']
        for standing in response1.json()['standings']:
             print(standing)
             if standing['type'] == 'TOTAL':
                table_data = standing['table']
                for team_data in table_data:
                    team_name = team_data['team']['name']
                    goal_difference = team_data['goalDifference']
                    pisteet = team_data['points']
                    maalit = team_data['goalsFor']
                    paastetyt = team_data['goalsAgainst']
                    pelit = team_data['playedGames']

                    if home_team == team_name:
                        games = pelit
                        goals = maalit
                        conceded = paastetyt
                        points = pisteet
                    if away_team == team_name:
                        opp_games = pelit
                        opp_goals = maalit
                        opp_conceded = paastetyt
                        opp_points = pisteet
             # Extract relevant information from data for home games
             if standing['type'] == 'HOME':
                table_data_home = standing['table']
                for team_data in table_data_home:
                    team_name = team_data['team']['name']

                    maalit_koti = team_data['goalsFor']
                    paastetyt_koti = team_data['goalsAgainst']
                    pelit_koti = team_data['playedGames']
                    pisteet_koti = team_data['points']

                    if home_team == team_name:
                        games_home = pelit_koti
                        goals_home = maalit_koti
                        conceded_home = paastetyt_koti
                        points_home = pisteet_koti
             # Extract relevant information from data for away games
             if standing['type'] == 'AWAY':
                table_data_away = standing['table']
                for team_data in table_data_away:
                    team_name = team_data['team']['name']

                    maalit_vieras = team_data['goalsFor']
                    paastetyt_vieras = team_data['goalsAgainst']
                    pelit_vieras = team_data['playedGames']
                    pisteet_vieras = team_data['points']

                    if away_team == team_name:
                        games_away = pelit_vieras
                        goals_away = maalit_vieras
                        conceded_away = paastetyt_vieras
                        points_away = pisteet_vieras

        team1_lambda_koti = lambda_multiplier(games_home,goals_home, conceded_home)
        team2_lambda_vieras = lambda_multiplier(games_away,goals_away, conceded_away)

        a = (round(1 / (poisson_multiplier(team1_lambda_koti, team2_lambda_vieras)[0]),2))

        b = (round(1 / (poisson_multiplier(team1_lambda_koti, team2_lambda_vieras)[1]),2))

        c = (round(1 / (poisson_multiplier(team1_lambda_koti, team2_lambda_vieras)[2]),2))

        mylist = [home_team, away_team, str(a), str(b), str(c)]
        for i in range(len(mylist)):
            mylist[i] += "\n"
        f.writelines(mylist)

    f.close()

    # create a new window
    root = tk.Tk()

    # Create header for the file
    font = ("Helvetica", 16, "bold")
    header_info = "Ottelut peliviikko: 25 (1 / x / 2)"
    tk.Label(root, text=header_info, font=font).pack()

    # create a label for each match
    with open("matches.txt", "r") as f:
        i = 0
        for line in f:
            if i % 5 == 0:
                home_team = line.strip()
            elif i % 5 == 1:
                away_team = line.strip()
            elif i % 5 == 2:
                home_win = float(line.strip())
            elif i % 5 == 3:
                draw = float(line.strip())
            elif i % 5 == 4:
                away_win = float(line.strip())

                # create a label with the match information
                match_info = f"{home_team} vs {away_team}: {home_win} / {draw} / {away_win}"
                tk.Label(root, text=match_info).pack()
            i += 1
    # run the window
    root.mainloop()












