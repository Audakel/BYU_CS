import argparse
import sys
import re
from pyspark import SparkContext, SparkConf
from scipy import stats
import math
import numbers
import numpy as np
import pandas as pd


"""
Headers

['color', 'director_name', 'num_critic_for_reviews', 'duration', 'director_facebook_likes', 'actor_3_facebook_likes', 'actor_2_name', 'actor_1_facebook_likes', 'gross', 'genres', 'actor_1_name', 'movie_title', 'num_voted_users', 'cast_total_facebook_likes', 'actor_3_name', 'facenumber_in_poster', 'plot_keywords', 'movie_imdb_link', 'num_user_for_reviews', 'language', 'country', 'content_rating', 'budget', 'title_year', 'actor_2_facebook_likes', 'imdb_score', 'aspect_ratio', 'movie_facebook_likes']
"""

drop_cols = ['color', 'director_name', 'actor_2_name', 'genres','actor_1_name', 'movie_title', 'actor_3_name', 'plot_keywords', 'movie_imdb_link', 'language', 'country', 'content_rating', 'title_year']


def init_argparse():
	# Gives linux like comand line help and parsing ability 
	parser = argparse.ArgumentParser(description='Finds trends in IMDb database with Lasso regression')
	parser.add_argument('in_file', nargs='+') #, type=argparse.FileType('r'), default=sys.stdin)
	parser.add_argument('out_file')
	parser.add_argument('-f', '--full', action='store_true', help='Full model: All predictors (identified for model inclusion during the data preprocessing step) included. No variable selection conducted.')
	parser.add_argument('-s','--stepwise', action='store_true', help='Using backwards stepwise regression (start with full model, eliminate one variable at a time based on the variable with the largest p-value, until only variables with a p-value < 0.05 remain)' )
	parser.add_argument('-l', '--lasso', action='store_true', help='Model obtained using LASSO regression.')
	args = parser.parse_args()


	def full_reg():
		pass


	def stepwise_reg():
		pass


	def lasso_reg():
		pass
	
	
	def prep_data(csv):
		df = pd.read_csv(csv, header=None)
		df = df.drop(drop_cols, axis=1)		
		#df = df.dropna()
	
	def graph():
		# specifies the parameters of our graphs
		fig = plt.figure(figsize=(18,6), dpi=1600) 
		alpha=alpha_scatterplot = 0.2 
		alpha_bar_chart = 0.55
		
		# lets us plot many diffrent shaped graphs together 
		ax1 = plt.subplot2grid((2,3),(0,0))
		# plots a bar graph of budget vs gross
		df.Survived.value_counts().plot(kind='bar', alpha=alpha_bar_chart)
		# this nicely sets the margins in matplotlib to deal with a recent bug 1.3.1
		ax1.set_xlim(-1, 2)
		# puts a title on our graph
		plt.title("Distribution of Survival, (1 = Survived)")    

		plt.subplot2grid((2,3),(0,1))
		plt.scatter(df.Survived, df.Age, alpha=alpha_scatterplot)
		# sets the y axis lable
		plt.ylabel("Age")
		# formats the grid line style of our graphs                          
		plt.grid(b=True, which='major', axis='y')  
		plt.title("Survival by Age,  (1 = Survived)")
		

if __name__ == "__main__":
	init_argparse()

	if args.f:
		full_reg()

	elif args.s:
		stepwise_reg()

	elif args.l:
		lasso_reg()
	
	elif args.g:
		graph()

	else:
		print('Error, did you choose a regression?')
		exit(1)


