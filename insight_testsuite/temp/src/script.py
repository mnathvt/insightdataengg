#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 10:51:09 2018

@author: madhurima
"""



import sys
import os


def main(start_hour, end_hour, actual_file_path, predicted_file_path, compare_file_path):
	sum_error = 0.0
	sum_count = 0


	# open the files
	actual_file = open(actual_file_path, 'r')
	predicted_file = open(predicted_file_path, 'r')
	compare_file = open(compare_file_path, 'a')
	

	for hour in range(start_hour, end_hour+1):

		e, c = get_error_sum(hour, actual_file, predicted_file)
		sum_error += e
		sum_count += c

	try:
		avg_error = sum_error/sum_count
	except:
		avg_error = 'NA'
	
	if avg_error == 'NA':
		compare_file.write('{0}|{1}|{2}\n'.format(start_hour, end_hour, avg_error))
	else:
		#print('avg for hours {0}-{1}: {2:.2f}'.format(start_hour, end_hour, avg_error))
		compare_file.write('{0}|{1}|{2:.2f}\n'.format(start_hour, end_hour, avg_error))

	# close the files
	actual_file.close()
	predicted_file.close()
	compare_file.close()
	


def get_error_sum(hour, actual_file, predicted_file):
	'''returns the absolute error and count of entries/stocks for each hour'''
	
	# build a dictionary containing the stock ids and the actual price for every hour from the actual values file
	data = {}
	
	actual_fp = actual_file.tell()

	for line in iter(actual_file.readline, 'b'):
		
		if len(line.strip()) != 0:
			try:
				line_parts = line.split('|')
				line_hour = int(line_parts[0])

				if line_hour > hour:
					actual_file.seek(actual_fp)
					break

				elif line_hour == hour:
					stock = line_parts[1]
					data[stock] = float(line_parts[2])

				actual_fp = actual_file.tell()

			except:
				continue

			# try-except will catch for errors in case the lines in the files are not in the format "hour | stock_id | price"
	#print(data)

	# if the dictionary is not empty, now I check for the prices in the predicted file
	# read the predicted values and calculate sum of differences


	sum_diff = 0.0
	count = 0

	if data:
		pred_fp = predicted_file.tell()
		
		for line in iter(predicted_file.readline, 'b'):

			if len(line.strip()) != 0:
				try:
					line_parts = line.split('|')
					line_hour = int(line_parts[0])

					if line_hour > hour:
						predicted_file.seek(pred_fp)
						break

					elif line_hour == hour:
						stock = line_parts[1]
						if stock in data:
							pred_val = float(line_parts[2])
							act_val = data[stock]
							sum_diff += abs(act_val - pred_val)
							count += 1
					
					pred_fp = predicted_file.tell()

				except:
					continue

		return sum_diff, count


if __name__ == '__main__':
	input_dir = os.path.join(".", "input")
	actual_file_path = os.path.join(input_dir, "actual.txt")
	predicted_file_path = os.path.join(input_dir, "predicted.txt")
	window_file_path = os.path.join(input_dir, "window.txt")

	output_dir = os.path.join(".", "output")
	compare_file_path = os.path.join(output_dir, "comparison.txt")
	
	# 1 = window, 2 = actual, 3 = predicted, 4 = comparison

	with open(actual_file_path, 'r') as fin:
		start_hour = int(fin.readline().split('|')[0]) 		# in case start hour is not 1
		max_hour = int(list(fin)[-1].split('|')[0])

	with open(window_file_path) as f:
		time_range = int(f.readline().strip())

	for hour in range(start_hour, max_hour-time_range+1):
		main(hour, hour + time_range - 1, actual_file_path, predicted_file_path, compare_file_path)




