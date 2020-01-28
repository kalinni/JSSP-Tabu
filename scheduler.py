import sys
from os import path
import math
import time
import copy
import pickle

from instanceparser import parse_instance
from realize_plan import realize_plan
from neighbourhood import generate_complex_neighbour
from planner import random_plan, fixed_plan

NO_IMPROVE_MAX = 20 	# How many iterations without improvement before we stop?
TRIES = 10 				# From how many different starting schedules do we run the tabu search?

MODE = 'Experimental'	# MODE variable shows whether the program is supposed to measure performance 
						# on a preset list of plans ('Experimental') or supposed to run for arbitrary plans ('Active')

INSTANCES = ['abz5', 'abz6', 'abz7', 'abz8', 'abz9', 'ft06', 'ft10', 'ft20', 
	'la01', 'la02', 'la03', 'la04', 'la05', 'la06', 'la07', 'la08', 'la09', 'la10', 
	'la11', 'la12', 'la13', 'la14', 'la15', 'la16', 'la17', 'la18', 'la19', 'la20', 
	'la21', 'la22', 'la23', 'la24', 'la25', 'la26', 'la27', 'la28', 'la29', 'la30', 
	'orb01', 'orb02', 'orb03', 'orb04', 'orb05', 'orb06', 'orb07', 'orb08', 'orb09', 'orb10', 
	'swv01', 'swv02', 'swv03', 'swv04', 'swv05', 'swv06', 'swv07', 'swv08', 'swv09', 'swv10', 
	'swv11', 'swv12', 'swv13', 'swv14', 'swv15', 'swv16', 'swv17', 'swv18', 'swv19', 'swv20', 
	'yn1', 'yn2', 'yn3', 'yn4']

# This function identifies any inconsistency in a given schedule 
# if no inconsistency is present, it instead displays the schedule 
def print_schedule(schedule, plan):
	timetable = [ [ 0 for s in range(plan['steps']) ] for j in range(plan['jobs']) ]
	if schedule['time'] < 0: 
		print("Couldn't schedule all jobs with this plan")
	else:
		print("Schedule takes %s time intervals" % schedule['time'])
		for m in range(plan['machines']):
			print("Machine %s:" % m)
			for op in schedule[m]:
				if op[0].machine != m: 
					print("Job %s is on the wrong machine." % op[0])
				if op[2] - op[1] != op[0].duration:
					print("Job %s takes a wrong amount of time, it takes %s" % (op[0], op[2]-op[1]))
				print('--- %s.%s start %s duration %s end %s' % (op[0].job, op[0].step, op[1], op[0].duration, op[2]))
				timetable[op[0].job][op[0].step] = (op[1], op[2])

	for t in timetable:
		for i in range(len(t)):
			if i <= len(t) - 2:
				if t[i][1] > t[i+1][0]:
					print("Steps from the same Job overlap: %s" % t)


# This function performs the tabu search on the given problem instance
# Tasks on the same machine after one another (i.e. neighbours) are swapped to possibly reach a better schedule
def search_schedule(plan):
	schedule = realize_plan(plan) 	# schedule is a tuple, 
									# first entry is list of lists of triples, the actual schedule, 
									# second entry is the time

	machines = plan['machines']

	# Start Tabu Search
	best_schedule = schedule
	no_improve = 0
	tabus = dict()
	frequencies = dict()
	iteration=0


	# Those two simply serve to see how many valid and invalid neighbours we check
	valid = 0
	invalid = 0

	while no_improve < NO_IMPROVE_MAX:					# Find best neighbour for current plan
		best_time = -1
		aspiration_check = []

		for m in range(machines):						# Try out all positions on all machines 
			for i in range(len(plan[m])-1):				# as swapping elements

	# Switch between swapping only neighbours and swapping any operations by disabling either the next two or the third line.
	######### 
				for k in range(1):
					j = i+1
	#########
#				for j in range(i+1,len(plan[m])):
	#########

					neighbour = generate_complex_neighbour(plan, m, i, j)
					if neighbour != False:									# for all permissible plans:
						sched = realize_plan(neighbour)						# construct the corresponding schedule
						if sched['time'] > 0:								# and compare it to the best schedule seen so far
							valid += 1

							penalty = 0
							if plan[m][j] in frequencies:
								penalty += len(frequencies[plan[m][j]])
							if plan[m][i] in frequencies:
								penalty += len(frequencies[plan[m][i]])
							penalty *= FREQUENCY_INFLUENCE

							if (best_time == -1) or (sched['time'] + penalty < best_time):
								if (plan[m][j],plan[m][i]) in tabus: 
									aspiration_check.append((copy.deepcopy(sched),penalty,m,i,j))
##									print("Swapping %s with %s is tabu!" % (plan[m][j],plan[m][i]))
								else:
									best_neighbour = sched
									best_time = sched['time'] + penalty
									swap = (m, i, j)
						else: 
							invalid += 1

		
		# Aspiration Search: If there is tabu neighbour with time better than current optimum 
		# 						and best found swap, choose tabu swap instead
		threshold = min(best_time, best_schedule['time']) if best_time > 0 else best_schedule['time']
		for (sched,penalty,m,i,j) in aspiration_check:
			if (sched['time'] + penalty < threshold):
				best_neighbour = sched
				best_time = sched['time'] + penalty
				threshold = best_time
				swap = (m, i, j)
##				print("Swapping %s with %s is tabu but great! Gives %s" % (plan[m][j],plan[m][i],best_neighbour['time']))


		if best_time == -1:
			print("No valid neighbour found.")
			break

		# Get Operations swapped
		op1 = plan[swap[0]][swap[1]]
		op2 = plan[swap[0]][swap[2]]
		
##		print("Swapped: %s with %s -- Current schedule's time: %s" % (op1,op2,best_neighbour['time']))

		# Update the best schedule and no-improvement-counter
		if best_neighbour['time'] >= best_schedule['time']:
			no_improve +=1
		else:
			best_schedule = best_neighbour
			no_improve = 0

		# Update tabus and add new tabu
		for tabu in list(tabus):
			if tabus[tabu] > 1:	
				tabus[tabu] -= 1 
			else:
				del tabus[tabu]
		tabus[(op1,op2)] = RECENCY_MEMORY

		# Update frequency memory
		for operation in list(frequencies):
			if frequencies[operation][0] == (iteration - FREQUENCY_MEMORY): 
				frequencies[operation].pop(0)
				if len(frequencies[operation]) == 0: del frequencies[operation]

		for op in (op1,op2):
			if op in frequencies:
				frequencies[op].append(iteration)
			else:
				frequencies[op] = [iteration]

		iteration += 1

		# Make the plan giving the best neighbour the starting point for the next iteration
		plan = generate_complex_neighbour(plan, swap[0], swap[1], swap[2])

	print("valid: %s, invalid: %s" % (valid,invalid))
	return best_schedule
	

def main():
	start_time = time.time()

	# Decide, on which instance to test our code
	if len(sys.argv) > 1:
		# you may run the script with a path to an instance as the argument
		instance = sys.argv[1]
		instance_path = 'instances/' + instance + '.txt'
		if not path.exists(instance_path):
			raise SystemExit("There is no instance at %s" % instance_path)
	else: 
		# default if no argument is passed
		instance = 'simple'
		instance_path = 'instances/' + instance + '.txt'

	# Make a plan from the chosen instance and turn it into the initial schedule
	### Note: Will always give a valid schedule, due to how we get the plan from the instance
	plan = parse_instance(instance_path) # plan is a dict

	set_dynamic_parameters(plan)

	# Run the tabu search
	optimum = -1
	for i in range(TRIES):
		if MODE == 'Active':
			plan = random_plan(plan)
		elif MODE == 'Experimental':
			plan = fixed_plan(plan, i, instance)
		else:
			raise SystemExit("The MODE variable is set to an undefined value!")

		best_schedule = search_schedule(plan)
		print("")
		print("Best Schedule in Run: %s" % best_schedule['time'])
		print("++++++++++++++++++++")
		print("")

		if (optimum < 0) or (best_schedule['time'] < optimum):
			optimum = best_schedule['time']
			optimum_schedule = best_schedule


	# Output
	execution_time = round(time.time() - start_time)
	print("Program takes %s minutes and %s seconds to run" \
		% (round(execution_time / 60), execution_time % 60) )
	print_schedule(optimum_schedule, plan)


def set_dynamic_parameters(plan):
	global RECENCY_MEMORY, FREQUENCY_MEMORY, FREQUENCY_INFLUENCE
	jobs = plan['jobs']
	steps = plan['steps']
	machines = plan['machines']
	weight = 0.25 * math.sqrt(jobs * steps)
	RECENCY_MEMORY = steps*machines/10			# How long are specific swaps tabu?
	FREQUENCY_MEMORY = steps*machines/2			# For how many steps do we remember our moves
	FREQUENCY_INFLUENCE = round(weight,2)		# Weight for the influence of the frequency
	print("Swaps are Tabu for %s steps" % FREQUENCY_MEMORY)
	print("Frequency Memory remembers the past %s steps" % FREQUENCY_MEMORY)
	print("Weight of frequency of moves is %s" % FREQUENCY_INFLUENCE)
	
# This function is used to perform tabu search on all benchmarked instances from the lecture
# It iterates over these instances and stores for all instances 
# 	the optimum time, 
# 	the optimum schedule 
# 	the resulting times from all other iterations of tabu search on this instance
def serial_experiments ():
	result = dict()
	for instance in INSTANCES:
		print("#########################")
		instance_path = 'instances/' + instance + '.txt'
		if not path.exists(instance_path):
			raise SystemExit("There is no instance at %s" % instance_path)
		else:
			print('Now running instance: '+ instance)
		print("#########################")
		
		plan = parse_instance(instance_path) 

		set_dynamic_parameters(plan)

		# Run the tabu search
		optimum = -1
		times = []
		for i in range(TRIES):
			plan = fixed_plan(plan, i, instance)

			schedule = search_schedule(plan)
			times.append(schedule['time'])
			if (optimum < 0) or (schedule['time'] < optimum):
				optimum = schedule['time']
				optimum_schedule = schedule

		result[instance] = (optimum, optimum_schedule, times)

	storage = open('results.txt', 'wb')			# for persistency, the results are stored 
	pickle.dump(result, storage)				# to a txt file
	storage.close()

def output_serial_results ():
	file = open('results.txt', 'rb')
	result = pickle.load(file)

	for instance in result:
		print("Instance %s has been performed in %s time units" % (instance, result[instance][0]))
	
	file.close()



if __name__ == "__main__": main()