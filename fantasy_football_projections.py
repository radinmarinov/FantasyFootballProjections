# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:43:09 2019

@author: Radin
"""
import pandas as pd
import numpy as np

def new_projection_df(pos):
    df = pd.DataFrame.from_csv("C:/Users/Radin/Documents/FantasyFootballProjections/FantasyPros_Fantasy_Football_Projections_" + pos.upper() + ".csv")
    df = df.reset_index()
    df = df[['Player', 'FPTS']]
    df = df.dropna()
    injury = pd.DataFrame.from_csv("C:/Users/Radin/Documents/FantasyFootballProjections/" + pos + "_injury.csv")
    injury = injury.reset_index()
    total_df = df.merge(injury, how='left', on='Player')
    avg_games_missed = np.mean(injury['Projected Games Missed'])
    total_df.loc[total_df['Projected Games Missed'].isna(), 'Projected Games Missed'] = avg_games_missed
    total_df['PPG'] = total_df.FPTS / 16
    total_df['Projected_Points_With_Injury'] = total_df.PPG * (16 - total_df['Projected Games Missed'])
    total_df['PPG_With_Injury'] = total_df['Projected_Points_With_Injury'] / 16
    total_df['Position'] = pos
    total_df = total_df.sort_values(by=['PPG_With_Injury'], ascending=False)
    total_df = total_df.reset_index()
    if pos == 'qb' or pos == 'te':
        baseline = 12
    else:
        baseline = 24
    total_df['PPG_Over_Position_Baseline'] = total_df['PPG_With_Injury'] - total_df['PPG_With_Injury'][baseline]    
    return total_df

projections_df = pd.DataFrame()
for pos in ['qb', 'rb', 'wr', 'te']:
    projections_df = projections_df.append(new_projection_df(pos))

projections_df = projections_df[['Player'
                                 ,'Position'                              
                                 , 'PPG_Over_Position_Baseline'
                                 , 'Projected Games Missed'
                                 , 'PPG'
                                 , 'PPG_With_Injury']]
projections_df.to_csv("C:/Users/Radin/Documents/FantasyFootballProjections/projections_df.csv")