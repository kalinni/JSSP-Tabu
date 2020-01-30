import pickle
from searcher import tabu_search

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
	'yn1': 884, 'yn2': 904, 'yn3': 892, 'yn4': 968}

MORE_INSTANCES = ['abz7', 'abz8', 'abz9', 
	'ft20', 
	'la01', 'la02', 'la03', 'la04', 'la05', 'la06', 'la07', 'la08', 'la09', 'la10', 
	'la11', 'la12', 'la13', 'la14', 'la15', 
	'la21', 'la22', 'la23', 'la24', 'la25', 'la26', 'la27', 'la28', 'la29', 'la30', 
	'swv01', 'swv02', 'swv03', 'swv04', 'swv05', 'swv06', 'swv07', 'swv08', 'swv09', 'swv10', 
	'swv11', 'swv12', 'swv13', 'swv14', 'swv15', 'swv16', 'swv17', 'swv18', 'swv19', 'swv20'
]

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

# This function is used to perform tabu search on all benchmarked instances from the lecture
# It iterates over these instances and stores for all instances 
# 	the best time, 
# 	the best schedule 
# 	the resulting times from all other iterations of tabu search on this instance
def serial_experiments (instances = list(INSTANCES)):
	mode = 'Experimental' # For better comparison we work with fixed starting points
	result = dict()

	for instance in instances:
		print("#########################")
		print('Now running instance: '+ instance)
		print("#########################")

		result[instance] = tabu_search(instance, mode)

	storage = open('results/results.txt', 'wb')			# for persistency, the results are stored 
	pickle.dump(result, storage)				# to a txt file
	storage.close()

def output_serial_results (path = 'results/results.txt'):
	file = open(path, 'rb')
	result = pickle.load(file)

	for instance in result:
		print("For instance %s our best schedule takes %s time units" % (instance, result[instance][0]))
	
	file.close()

def performance(resfile='results/results.txt'):
	file = open(resfile, 'rb')
	result = pickle.load(file)
	differences = []
	optimal = 0
	better = []
	for instance in result:
		percent = round((result[instance][0]/INSTANCES_ALL[instance] -1)*100,1)
		differences.append(percent)
		if (result[instance][0] - INSTANCES_ALL[instance]) == 0 : 
			optimal += 1
		elif (result[instance][0] - INSTANCES_ALL[instance]) < 0: 
			better.append(instance)
		print("Instance %s ---- our best: %s ---- optimum: %s ---- difference in percent: %s " % (instance, result[instance][0], INSTANCES_ALL[instance], percent))
	print("On average our schedules take %s" % (round(sum(differences)/len(differences),2)) + "% more time.")
	print("%s out of %s schedules where optimal!" % (optimal, len(result)))
	if len(better) > 0:
		print("Caution! The following instances got schedules performing better than the best solution known so far!")
		for instance in better:
			print(instance)
