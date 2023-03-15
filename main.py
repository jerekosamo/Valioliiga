
import requests
from scipy.stats import poisson


class Joukkue:
    def __init__(self, nimi, pisteet, tmaalit, pmaalit):
        self.nimi = nimi
        self.pisteet = pisteet
        self.tmaalit = tmaalit
        self.pmaalit = pmaalit

def palautusprosentti(koti, tasapeli, vieras):
    if koti > 1:
        x = (1/koti) + (1/tasapeli) + (1/vieras)
    else:
        x = (koti + tasapeli + vieras)

    return (1 / x)

def lambda_kerroin(games, goals, conceded):
    kerroin = (goals / games) / (conceded / games)
    return kerroin

def lambda_pisteet(pelit, pisteet):
    kerroin = pisteet / pelit
    return kerroin

def kerroin(h_win, h_tie, h_loss, v_win, v_tie, v_loss):
    h_matches = (h_win + h_tie + h_loss)
    v_matches = (v_win + v_tie + v_loss)
    h_win_factor = h_win / h_matches
    h_tie_factor = h_tie / h_matches
    h_loss_factor = h_loss / h_matches
    v_win_factor = v_win / v_matches
    v_tie_factor = v_tie / v_matches
    v_loss_factor = v_loss / v_matches
    #print(h_tie, v_tie)
    #print(h_win,v_win, h_loss, v_loss)
    #print(h_tie_factor,v_tie_factor)
    h_factor = 1 / ((h_win_factor + v_loss_factor) / 2)
    v_factor = 1 / ((h_loss_factor + v_win_factor) / 2)
    t_factor = 1 / ((h_tie_factor + v_tie_factor) / 2)
    #t_factor = 1 / (1 - (((h_loss_factor + v_win_factor) / 2) + ((h_win_factor + v_loss_factor) / 2)))
    return (h_factor, t_factor, v_factor)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Arsenal = Joukkue("Arsenal FC", 50, 45, 16)
    ManC = Joukkue("Manchester City FC", 45, 53, 20)
    Newcastle = Joukkue("Newcastle United FC", 39, 33, 11)
    ManU = Joukkue("Manchester United FC", 39, 32, 25)
    Tottenham = Joukkue("Tottenham Hotspur FC", 36, 40, 31)
    Brighton = Joukkue("Brighton & Hove Albion FC", 31, 37, 27)
    Fulham = Joukkue("Fulham FC", 31, 32, 30)
    Brentford = Joukkue("Brentford FC", 30, 32, 28)
    Liverpool = Joukkue("Liverpool FC", 29, 34, 25)
    Chelsea = Joukkue("Chelsea FC", 29, 22, 21)
    AstonVilla = Joukkue("Aston Villa FC", 28, 23, 27)
    CrystalPalace = Joukkue("Crystal Palace FC", 24, 18, 27)
    Nottingham = Joukkue("Nottingham Forest FC", 21, 16, 35)
    Leicester = Joukkue("Leicester City FC", 18, 28, 35)
    Leeds = Joukkue("Leeds United FC", 18, 26, 33)
    Westham = Joukkue("West Ham United FC", 18, 17, 25)
    wolves = Joukkue("Wolverhampton Wanderers FC", 17, 12, 30)
    Bournemouth = Joukkue("AFC Bournemouth", 17, 19, 42)
    Everton = Joukkue("Everton FC", 15, 15, 28)
    Southampton = Joukkue("Southampton FC", 15, 17, 35)
    #print((ManU.tmaalit) - (ManC.pmaalit))

    # # Define the lambda values for each team
    # team1_lambda = 0.725  # expected goals scored per match for team 1 / expected goals conceded per match
    # team2_lambda = 1.48  # expected goals scored per match for team 2 / expected goals conceded per match
    #
    # # Calculate the probability of each team scoring a specific number of goals
    # team1_goals = [poisson.pmf(i, team1_lambda) for i in range(6)]
    # team2_goals = [poisson.pmf(i, team2_lambda) for i in range(6)]
    #
    # # Calculate the probability of each scoreline
    # scorelines = [[i, j] for i in range(6) for j in range(6)]
    # scoreline_probabilities = [team1_goals[i] * team2_goals[j] for i, j in scorelines]
    #
    # # Calculate the probability of each outcome
    # team1_wins = sum(
    #     [scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] > scorelines[i][1]])
    # team2_wins = sum(
    #     [scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] < scorelines[i][1]])
    # draw = sum([scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] == scorelines[i][1]])
    #
    # # Normalize the probabilities
    # total_probability = team1_wins + team2_wins + draw
    # team1_win_prob = team1_wins / total_probability
    # team2_win_prob = team2_wins / total_probability
    # draw_prob = draw / total_probability
    #
    # # Print the probabilities
    # print(f"Team 1 win probability: {team1_win_prob:.2%}")
    # print(f"Team 2 win probability: {team2_win_prob:.2%}")
    # print(f"Draw probability: {draw_prob:.2%}")

    # Print the probabilities of each scoreline
    #for scoreline, probability in zip(scorelines, scoreline_probabilities):
        #print(f"{scoreline[0]}-{scoreline[1]}: {probability:.2%}")

    uri = 'https://api.football-data.org/v4/competitions/PL/matches?matchday=28'
    uri1 = 'https://api.football-data.org/v4/competitions/PL/standings?type=TOTAL'
    headers = {'X-Auth-Token': '74c7b6e85a8b49a9991a4b0a0158d38f'}

    wins = 0
    draws = 0
    losses = 0
    opp_wins = 0
    opp_draws = 0
    opp_losses = 0
    games = 0
    goals = 0
    conceded = 0
    points = 0
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
             #print (standing)
             if standing['type'] == 'TOTAL':
                table_data = standing['table']
                for team_data in table_data:
                    team_name = team_data['team']['name']
                    goal_difference = team_data['goalDifference']
                    pisteet = team_data['points']
                    maalit = team_data['goalsFor']
                    paastetyt = team_data['goalsAgainst']
                    pelit = team_data['playedGames']
                    voitot = team_data['won']
                    tasapelit = team_data['draw']
                    tappiot = team_data['lost']

                    if home_team == team_name:
                        wins = voitot
                        draws = tasapelit
                        losses = tappiot
                        games = pelit
                        goals = maalit
                        conceded = paastetyt
                        points = pisteet
                    if away_team == team_name:
                        opp_wins = voitot
                        opp_draws = tasapelit
                        opp_losses = tappiot
                        opp_games = pelit
                        opp_goals = maalit
                        opp_conceded = paastetyt
                        opp_points = pisteet



                 # print(f"{team_name}: {goal_difference}")
        print(home_team,' vs ', away_team)
        #print(kerroin(wins, draws, losses, opp_wins, opp_draws, opp_losses))

        team1_lambda = lambda_kerroin(games, goals, conceded)
        team2_lambda = lambda_kerroin(opp_games, opp_goals, opp_conceded)
        team1_lambda_points = lambda_pisteet(games, points)
        team2_lambda_points = lambda_pisteet(opp_games, opp_points)
        # Calculate the probability of each team scoring a specific number of goals
        team1_goals = [poisson.pmf(i, team1_lambda) for i in range(6)]
        team2_goals = [poisson.pmf(i, team2_lambda) for i in range(6)]
        team1_points = [poisson.pmf(i, team1_lambda_points) for i in range(6)]
        team2_points = [poisson.pmf(i, team2_lambda_points) for i in range(6)]

        # Calculate the probability of each scoreline
        scorelines = [[i, j] for i in range(6) for j in range(6)]
        scoreline_probabilities = [team1_goals[i] * team2_goals[j] for i, j in scorelines]
        scorelines_points = [[i, j] for i in range(6) for j in range(6)]
        scoreline_probabilities_points = [team1_points[i] * team2_points[j] for i, j in scorelines_points]

        # Calculate the probability of each outcome
        team1_wins = sum(
            [scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] > scorelines[i][1]])
        team2_wins = sum(
            [scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] < scorelines[i][1]])
        draw = sum([scoreline_probabilities[i] for i in range(len(scorelines)) if scorelines[i][0] == scorelines[i][1]])

        team1_wins_points = sum(
            [scoreline_probabilities_points[i] for i in range(len(scorelines_points)) if scorelines_points[i][0] > scorelines_points[i][1]])
        team2_wins_points = sum(
            [scoreline_probabilities_points[i] for i in range(len(scorelines_points)) if scorelines_points[i][0] < scorelines_points[i][1]])
        draw_points = sum([scoreline_probabilities_points[i] for i in range(len(scorelines_points)) if scorelines_points[i][0] == scorelines_points[i][1]])

        # Normalize the probabilities
        total_probability = team1_wins + team2_wins + draw
        team1_win_prob = team1_wins / total_probability
        team2_win_prob = team2_wins / total_probability
        draw_prob = draw / total_probability

        total_probability_points = team1_wins_points + team2_wins_points + draw_points
        team1_win_prob_points = team1_wins_points / total_probability_points
        team2_win_prob_points = team2_wins_points / total_probability_points
        draw_prob_points = draw_points / total_probability_points

        # Print the probabilities
        print(f"Team 1 win probability: {team1_win_prob:.2%}", round(1 / team1_win_prob, 2))
        print(f"Team 2 win probability: {team2_win_prob:.2%}", round(1 / team2_win_prob, 2))
        print(f"Draw probability: {draw_prob:.2%}", round(1 / draw_prob, 2))

        print(f"Team 1 win probability: {team1_win_prob_points:.2%}", round(1 / team1_win_prob_points, 2))
        print(f"Team 2 win probability: {team2_win_prob_points:.2%}", round(1 / team2_win_prob_points, 2))
        print(f"Draw probability: {draw_prob_points:.2%}", round(1 / draw_prob_points, 2))


    #print (Ottelut)
    #print (kerroin(wins, draws, losses, opp_wins, opp_draws, opp_losses))
    #print(palautusprosentti(1.548387, 5.3333333, 5.9999999))









