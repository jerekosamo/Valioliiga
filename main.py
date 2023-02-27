import pandas as pd
import numpy as np
import requests
import json
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tabulate import tabulate


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

def kerroin(h_win, h_tie, h_loss, v_win, v_tie, v_loss):
    h_matches = (h_win + h_tie + h_loss)
    v_matches = (v_win + v_tie + v_loss)
    h_win_factor = h_win / h_matches
    h_tie_factor = h_tie / h_matches
    h_loss_factor = h_loss / h_matches
    v_win_factor = v_win / v_matches
    v_tie_factor = v_tie / v_matches
    v_loss_factor = v_loss / v_matches
    h_factor = 1 / ((h_win_factor + v_loss_factor) / 2)
    t_factor = 1 / ((h_tie_factor + v_tie_factor) / 2)
    v_factor = 1 / ((h_loss_factor + v_win_factor) / 2)
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
    print((ManU.tmaalit) - (ManC.pmaalit))

    uri = 'https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED'
    uri1 = 'https://api.football-data.org/v4/competitions/PL/standings'
    headers = {'X-Auth-Token': '74c7b6e85a8b49a9991a4b0a0158d38f'}
    Ottelut = []
    wins = 0
    draws = 0
    losses = 0
    opp_wins = 0
    opp_draws = 0
    opp_losses = 0
    response = requests.get(uri, headers=headers)
    response1 = requests.get(uri1, headers=headers)
    for x in response1.json()['standings']:
        print (x)
        table_data = x['table']
        for team_data in table_data:
            team_name = team_data['team']['name']
            goal_difference = team_data['goalDifference']
            print(f"{team_name}: {goal_difference}")





    for match in response.json()['matches']:
        #print (match)

        match_data = match
        # Extract relevant information
        home_team = match_data['homeTeam']['name']
        away_team = match_data['awayTeam']['name']
        goal_difference = match_data['score']['fullTime']['home'] - match_data['score']['fullTime']['away']
        winner = match_data['score']['winner']
        Ottelut.append({'home_team': [home_team],
                           'away_team': [away_team],
                           'goal_difference': [goal_difference],
                           'winner': [winner]})
        if home_team == 'Arsenal FC':
            if winner == 'HOME_TEAM':
                wins += 1
            elif winner == "DRAW":
                draws += 1
            elif winner == "AWAY_TEAM":
                losses += 1
        if away_team == 'Arsenal FC':
            if winner == 'HOME_TEAM':
                losses += 1
            elif winner == "DRAW":
                draws += 1
            elif winner == "AWAY_TEAM":
                wins += 1
        if home_team == 'Everton FC':
            if winner == 'HOME_TEAM':
                opp_wins += 1
            elif winner == "DRAW":
                opp_draws += 1
            elif winner == "AWAY_TEAM":
                opp_losses += 1
        if away_team == 'Everton FC':
            if winner == 'HOME_TEAM':
                opp_losses += 1
            elif winner == "DRAW":
                opp_draws += 1
            elif winner == "AWAY_TEAM":
                opp_wins += 1


    #print (Ottelut)
    print (kerroin(wins, draws, losses, opp_wins, opp_draws, opp_losses))
    #print(palautusprosentti(1.548387, 5.3333333, 5.9999999))
    print("tää on joku testi")








