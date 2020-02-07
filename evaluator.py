import pickle
import math
import numpy as np
import matplotlib.pyplot as plt

from searcher import tabu_search

# all instances with the optimal times given 
# here: https://pdfs.semanticscholar.org/1d26/47ac792c6f199bfd4893692648c437c0bab2.pdf 
# and here: https://books.google.de/books?id=xj00CwAAQBAJ&pg=PA565&lpg=PA565&dq=job+shop+scheduling+abz5-abz9+benchmarks&source=bl&ots=8j7oSEcsqq&sig=ACfU3U2DWype-Kv7ixGnl8TFpDp2zYZe4g&hl=de&sa=X&ved=2ahUKEwj8hvL61ILnAhUSy6QKHXSDD9wQ6AEwAHoECAkQAQ#v=onepage&q=job%20shop%20scheduling%20abz5-abz9%20benchmarks&f=false

INSTANCES_ALL = {'abz5': 1234, 'abz6': 943, 'abz7': 656, 'abz8': 665, 'abz9': 679, 
	'ft06': 55, 'ft10': 930, 'ft20': 1165, 
	'la01': 666, 'la02': 655, 'la03': 597, 'la04': 590, 'la05': 593, 
	'la06': 926, 'la07': 890, 'la08': 863, 'la09': 951, 'la10': 958, 
	'la11': 1222, 'la12': 1039, 'la13': 1150, 'la14': 1292, 'la15': 1207, 
	'la16': 945, 'la17': 784, 'la18': 848, 'la19': 842, 'la20': 902, 
	'la21': 1046, 'la22': 927, 'la23': 1032, 'la24': 935, 'la25': 977, 
	'la26': 1218, 'la27': 1235, 'la28': 1216, 'la29': 1153, 'la30': 1355, 
	'la31':1784, 'la32':1850, 'la33':1719, 'la34':1721, 'la35':1888, 
	'la36':1268, 'la37':1397, 'la38':1196, 'la39':1233, 'la40':1222,
	'orb01': 1059, 'orb02': 888, 'orb03': 1005, 'orb04': 1005, 'orb05': 887, 
	'orb06': 1010, 'orb07': 397, 'orb08': 899, 'orb09': 934, 'orb10': 944, 
	'swv01': 1407, 'swv02': 1475, 'swv03': 1398, 'swv04': 1470, 'swv05': 1424, 
	'swv06': 1675, 'swv07': 1594, 'swv08': 1755, 'swv09': 1661, 'swv10': 1743, 
	'swv11': 2983, 'swv12': 2979, 'swv13': 3104, 'swv14': 2968, 'swv15': 2886, 
	'swv16': 2924, 'swv17': 2794, 'swv18': 2852, 'swv19': 2843, 'swv20': 2823, 
	'yn1': 884, 'yn2': 904, 'yn3': 892, 'yn4': 968
}

INSTANCES = [
	'ft06', # 6x6
	'la01', 'la05', # 10x5
	'la07', 'la10', # 15x5
	'abz5', 'la18', 'orb01', 'orb04', 'orb10', # 10x10
	'ft20', 'la13', # 20x5
	'la23', 'la25', # 15x10
	'la27', 'la28', 'swv01', 'swv05', # 20x10
	'la38', 'la39', # 15x15
	'la31', 'la34', # 30x10
	'abz9', 'swv07', 'swv08', # 20x15 
	'yn4', #20x20
	'swv12', 'swv13', 'swv18' #50x10
]

SOME_INSTANCES = [
	'ft06', # 6x6
	'la01', 'la05', # 10x5
	'la07', # 15x5
	'abz5', 'orb10', # 10x10
	'ft20', 'la13', # 20x5
	'la23', # 15x10
	'swv01', # 20x10
	'la39', # 15x15
	'la31', # 30x10
	'abz9', 'swv07', # 20x15 
	'yn4', #20x20
	'swv13', 'swv18' #50x10
]

# This function is used to perform tabu search on all benchmarked instances from the lecture
# It iterates over these instances and stores for all instances 
# 	the best time, 
# 	the best schedule 
# 	the resulting times from all other iterations of tabu search on this instance
def serial_experiments (instances = list(INSTANCES_ALL), path = 'results/results.txt'):
	mode = 'Experimental' # For better comparison we work with fixed starting points
	result = dict()

	for instance in instances:
		print("#########################")
		print('Now running instance: '+ instance)
		print("#########################")

		result[instance] = tabu_search(instance, mode)

	storage = open(path, 'wb')			# for persistency, the results are stored 
	pickle.dump(result, storage)				# to a txt file
	storage.close()

#The result from serial experiments is stored in a binary file
#This function outputs all the results in a readable format
def output_serial_results (path = 'results/results.txt'):
	file = open(path, 'rb')
	result = pickle.load(file)

	for instance in result:
		print("For instance %s our best schedule takes %s time units" % (instance, result[instance][0]))
	
	file.close()

def performance(resfile='results/results.txt',weights='[no weights known]'):
	'''
	Given a result file produced for example by the serial_experiments() method 
	(a dict() containing results per instances pickelt as a txt file)
	this method prints an overview of the results to the command line,
	calculates how much longer our schedules take on average,
	checks how many optimal schedules we found 
	and generates a chart containing 
		- the best times known
		- the best times from our run
		- the mean of our times
		- the standard deviation to that mean for our times

	The chart is saved as a png with the same name as the given results file
	'''
	file = open(resfile, 'rb')
	result = pickle.load(file)

	# For calculating some stats
	differences = []
	differences_mean = []
	optimal = 0
	better = []

	# Lists for the stacked bar chart
	optimals = []
	our_best = [] # needed to stack means on top of our best
	our_best_diff = [] # difference our best to optimals
	means_diff = [] # difference our mean to our best
	deviations = [] # standard deviations to the mean


	for instance in result:
		optimals.append(INSTANCES_ALL[instance])
		our_best_diff.append(result[instance][0] - INSTANCES_ALL[instance])
		our_best.append(result[instance][0])

		# calculate mean
		all_times = result[instance][2]
		mean = sum(all_times)/len(all_times)
		means_diff.append(mean-result[instance][0])

		# calculate standard deviation
		st_dev = 0
		for time in all_times:
			st_dev += (time - mean)**2
		st_dev /= len(all_times)
		st_dev = math.sqrt(st_dev)
		deviations.append(st_dev)

		# calculate how much longer our schedules take and how many optimal times we found
		percent = round((result[instance][0]/INSTANCES_ALL[instance] -1)*100,1)
		percent_mean = round((mean/INSTANCES_ALL[instance]-1)*100,1)
		differences.append(percent)
		differences_mean.append(percent_mean)
		if (result[instance][0] - INSTANCES_ALL[instance]) == 0 : 
			optimal += 1
		# Check, whether some results seem to be better then the optimal known so far
		elif (result[instance][0] - INSTANCES_ALL[instance]) < 0: 
			better.append(instance)
		print("Instance %s ---- our best: %s ---- optimum: %s ---- difference in percent: %s " % (instance, result[instance][0], INSTANCES_ALL[instance], percent))
	
	print("On average our best schedules take %s" % (round(sum(differences)/len(differences),2)) + "% more time.")
	print("On average our schedules take %s" % (round(sum(differences_mean)/len(differences_mean),2)) + "% more time.")
	print("%s out of %s schedules where optimal!" % (optimal, len(result)))
	
	if len(better) > 0:
		print("Caution! The following instances got schedules performing better than the best solution known so far!")
		for instance in better:
			print(instance)

	# Generate the bar chart
	N = len(result)
	ind = np.arange(N)
	width = 0.5
	plt.rcParams.update({'font.size': 9})
	plt.figure(figsize=(((0.1*len(result))+8),6.5))

	p1 = plt.bar(ind, optimals, width)
	p2 = plt.bar(ind, our_best_diff, width, bottom=optimals)
	p3 = plt.bar(ind, means_diff, width, bottom=our_best, yerr=deviations)

	plt.ylabel('Time')
	plt.title('Results for %s' % str(weights) 
		+ "\n On average our best schedules take %s" % (round(sum(differences)/len(differences),2)) + "% more time."
		+ "\n On average our schedules take %s" % (round(sum(differences_mean)/len(differences_mean),2)) + "% more time."
		+ "\n %s out of %s schedules where optimal!" % (optimal, len(result)))
	plt.xticks(ind, list(result), rotation='vertical')
	plt.yticks(np.arange(0, 5000, 500))
	plt.legend((p1[0], p2[0], p3[0]), ('Optimal', 'Our Best', 'Our Mean with Standard Deviation'))

	plt.savefig(resfile.replace('.txt','.png'), dpi=500)

def parameter_checker(instances=SOME_INSTANCES):
	'''
	This is a function for playing around with the influence of our parameters. 
	'''
	mode = 'Experimental' # For better comparison we work with fixed starting points
	list_of_weights = [(0.5, 2, 0.3),(1, 2, 0.3),(0.5, 4, 0.3),(0.5, 2, 0.6),(0.5, 2, 0.15)]
	for weights in list_of_weights:

		result = dict()

		for instance in instances:
			print("#########################")
			print('Now running instance: '+ instance + ' for weights ' + str(weights))
			print("#########################")

			result[instance] = tabu_search(instance, mode, weights)
		resfile = 'results/results'+str(weights)+'.txt'
		storage = open(resfile, 'wb')			# for persistency, the results are stored 
		pickle.dump(result, storage)				# to a txt file
		storage.close()
		performance(resfile,weights)