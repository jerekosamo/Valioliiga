
import requests
from scipy.stats import poisson
import tkinter as tk
import Keys


def palautusprosentti(koti, tasapeli, vieras):
    #Jos luvut ovat kertoimia eli yli 1.00, niillä jaetaan ykköstä. JOs luvut prosentteina ne lisätään yhteen
    if koti > 1:
        x = (1/koti) + (1/tasapeli) + (1/vieras)
    else:
        x = (koti + tasapeli + vieras)

    return (1 / x)

def lambda_kerroin(games, goals, conceded):
    kerroin = (goals / games) / (conceded / games)
    return kerroin

def lambda_pisteet(pelit, pisteet):
    print(pisteet, pelit)
    kerroin = pisteet / pelit
    return kerroin

def poisson_kertoimet(lambda_home, lambda_away):
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

def poisson_kertoimet_pisteet(lambda_home, lambda_away):
    # Calculate the probability of each team scoring a specific number of goals
    prob_home_p = [poisson.pmf(i, lambda_home) for i in range(4)]
    prob_away_p = [poisson.pmf(i, lambda_away) for i in range(4)]

    # Calculate the probability of each scoreline
    scorelines_p = [[i, j] for i in range(4) for j in range(4)]
    scoreline_probabilities_p = [prob_home_p[i] * prob_away_p[j] for i, j in scorelines_p]

    # Calculate the probability of each outcome
    team1_wins_p = sum(
        [scoreline_probabilities_p[i] for i in range(len(scorelines_p)) if scorelines_p[i][0] > scorelines_p[i][1]])
    draw_p = sum([scoreline_probabilities_p[i] for i in range(len(scorelines_p)) if scorelines_p[i][0] == scorelines_p[i][1]])
    team2_wins_p = sum(
        [scoreline_probabilities_p[i] for i in range(len(scorelines_p)) if scorelines_p[i][0] < scorelines_p[i][1]])

    # Normalize the probabilities
    total_probability_p = team1_wins_p + team2_wins_p + draw_p
    team1_win_prob_p = team1_wins_p / total_probability_p
    team2_win_prob_p = team2_wins_p / total_probability_p
    draw_prob_p = draw_p / total_probability_p

    # Print the probabilities
    # print(f"Team 1 win probability: {team1_win_prob:.2%}", round(1 / team1_win_prob, 2))
    # print(f"Team 2 win probability: {team2_win_prob:.2%}", round(1 / team2_win_prob, 2))
    # print(f"Draw probability: {draw_prob:.2%}", round(1 / draw_prob, 2))

    return (team1_win_prob_p, draw_prob_p, team2_win_prob_p)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    f = open("matches.txt", "w")

    uri = 'https://api.football-data.org/v4/competitions/PL/matches?matchday=12'
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
        # Extract relevant information
        home_team = match_data['homeTeam']['name']
        away_team = match_data['awayTeam']['name']
        for standing in response1.json()['standings']:
             print(standing)
             if standing['type'] == 'TOTAL':
                #print(standing)
                table_data = standing['table']
                for team_data in table_data:
                    team_name = team_data['team']['name']
                    goal_difference = team_data['goalDifference']
                    pisteet = team_data['points']
                    #print(pisteet)
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

             if standing['type'] == 'HOME':
                #print(standing)
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





        #print(home_team,' vs ', away_team)

        #team1_lambda = lambda_kerroin(games, goals, conceded)
        #team2_lambda = lambda_kerroin(opp_games, opp_goals, opp_conceded)
        #team1_lambda_points = lambda_pisteet(games, points)
        #team2_lambda_points = lambda_pisteet(opp_games, opp_points)
        #team1_lambda_points = lambda_pisteet(games_home, points_home)
        #team2_lambda_points = lambda_pisteet(games_away, points_away)
        team1_lambda_koti = lambda_kerroin(games_home,goals_home, conceded_home)
        team2_lambda_vieras = lambda_kerroin(games_away,goals_away, conceded_away)



        #a = (round(1 / ((poisson_kertoimet(team1_lambda,team2_lambda)[0] + poisson_kertoimet(team1_lambda_points, team2_lambda_points)[0]) / 2), 2 ))
        #b = (round( 1 / ((poisson_kertoimet(team1_lambda, team2_lambda)[1] +
         #      poisson_kertoimet(team1_lambda_points, team2_lambda_points)[1]) / 2), 2))
        #c = (round( 1 / ((poisson_kertoimet(team1_lambda, team2_lambda)[2] +
         #      poisson_kertoimet(team1_lambda_points, team2_lambda_points)[2]) / 2), 2))
        a = (round(1 / (poisson_kertoimet(team1_lambda_koti, team2_lambda_vieras)[0]),2))
                         # + poisson_kertoimet_pisteet(team1_lambda_points, team2_lambda_points)[0]) / 2), 2))
        b = (round(1 / (poisson_kertoimet(team1_lambda_koti, team2_lambda_vieras)[1]),2))
                         # + poisson_kertoimet_pisteet(team1_lambda_points, team2_lambda_points)[1]) / 2), 2))
        c = (round(1 / (poisson_kertoimet(team1_lambda_koti, team2_lambda_vieras)[2]),2))
                         # + poisson_kertoimet_pisteet(team1_lambda_points, team2_lambda_points)[2]) / 2), 2))
        mylist = [home_team, away_team, str(a), str(b), str(c)]
        for i in range(len(mylist)):
            mylist[i] += "\n"
        f.writelines(mylist)


    f.close()

    # create a new window
    root = tk.Tk()


    # Create header for the file
    font = ("Helvetica", 16, "bold")
    header_info = "Ottelut peliviikko: 12 (1 / x / 2)"
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












