import pickle
from searcher import tabu_search

INSTANCES_ALL = ['abz5', 'abz6', 'abz7', 'abz8', 'abz9', 'ft06', 'ft10', 'ft20', 
	'la01', 'la02', 'la03', 'la04', 'la05', 'la06', 'la07', 'la08', 'la09', 'la10', 
	'la11', 'la12', 'la13', 'la14', 'la15', 'la16', 'la17', 'la18', 'la19', 'la20', 
	'la21', 'la22', 'la23', 'la24', 'la25', 'la26', 'la27', 'la28', 'la29', 'la30', 
	'orb01', 'orb02', 'orb03', 'orb04', 'orb05', 'orb06', 'orb07', 'orb08', 'orb09', 'orb10', 
	'swv01', 'swv02', 'swv03', 'swv04', 'swv05', 'swv06', 'swv07', 'swv08', 'swv09', 'swv10', 
	'swv11', 'swv12', 'swv13', 'swv14', 'swv15', 'swv16', 'swv17', 'swv18', 'swv19', 'swv20', 
	'yn1', 'yn2', 'yn3', 'yn4']

MORE_INSTANCES = ['la31', 'la32', 'la33', 'la34', 'la35', 'la36', 'la37', 'la38', 'la39', 'la40']

INSTANCES = ['abz5', 'abz9', 'ft06', 'ft20', 
	'la01', 'la05', 'la07', 'la10', 'la13', 'la18', 'la23', 'la25', 'la27', 'la28', 
	'orb01', 'orb04', 'orb10', 'swv01', 'swv05', 'swv07', 'swv08',
	'swv12', 'swv13', 'swv18', 'yn4']

# This function is used to perform tabu search on all benchmarked instances from the lecture
# It iterates over these instances and stores for all instances 
# 	the best time, 
# 	the best schedule 
# 	the resulting times from all other iterations of tabu search on this instance
def serial_experiments ():
	mode = 'Experimental' # For better comparison we work with fixed starting points
	result = dict()

	for instance in INSTANCES:
		print("#########################")
		print('Now running instance: '+ instance)
		print("#########################")

		result[instance] = tabu_search(instance, mode)

	storage = open('results/results.txt', 'wb')			# for persistency, the results are stored 
	pickle.dump(result, storage)				# to a txt file
	storage.close()

def output_serial_results ():
	file = open('results/results.txt', 'rb')
	result = pickle.load(file)

	for instance in result:
		print("For instance %s our best schedule takes %s time units" % (instance, result[instance][0]))
	
	file.close()