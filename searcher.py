import sys
from os import path
import math
import time
import copy

from jssp_parser import parse_instance
from scheduler import realize_plan
from neighbourhood import generate_neighbour
from planner import random_plan, fixed_plan

NO_IMPROVE_MAX = 12		# How many iterations without improvement before we stop?
NO_IMPROVE_SWITCH = 6	# How many iterations without improvement before we switch to a more complex neighbourhood?
TRIES = 5				# From how many different starting schedules do we run the tabu search?

MODE = 'Active'	# MODE variable shows whether the program is supposed to measure performance 
						# on a preset list of plans ('Experimental') or supposed to run for arbitrary plans ('Active')

# This function prints the schedule to the command line
# It also identifies inconsistency in the schedule (though our tabu search should not cause any)
def print_schedule(schedule):
	timetable = [ [ 0 for s in range(schedule['steps']) ] for j in range(schedule['jobs']) ]
	if schedule['time'] < 0: 
		print("Couldn't schedule all jobs with this plan")
	else:
		print("Schedule takes %s time intervals" % schedule['time'])
		for m in range(schedule['machines']):
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


# This function performs the tabu search on the given problem instance represented as plan
def search_schedule(plan):
	
	# Initialization
	schedule = realize_plan(plan) 	# schedule is a dict with its overall time as value to the key 'time' 
									# and ordered lists of (operation, start, end)-triples for each machine
	machines = plan['machines']
	best_schedule = schedule
	no_improve = 0
	tabus = dict()
	frequencies = dict()
	iteration=0

	# Those two simply serve to see how many valid and invalid neighbours we check
	valid = 0
	invalid = 0
	aspiration = 0

	# Start of the Tabu Search
	### While last improvement is less than a fixed number of steps away, find best neighbour for current plan
	while no_improve < NO_IMPROVE_MAX:					
		best_time = -1
		aspiration_check = []

		# Try out all positions on all machines for swapping
		for m in range(machines):
			for i in range(len(plan[m])-1):
				# If we had no improvement recently switch from fast but simple swapping of only neighbours to more complex swapping of any operations on the same machine
				if no_improve < NO_IMPROVE_SWITCH: 
					neighbourrange = [i+1]
				else:
					neighbourrange = range(i+1,len(plan[m]))
				for j in neighbourrange:
					neighbour = generate_neighbour(plan, m, i, j)
					if neighbour != False:									# for all permissible plans:
						sched = realize_plan(neighbour)						# construct the corresponding schedule
						if sched['time'] > 0:								# and compare it to the best schedule seen so far
							valid += 1

							penalty = 0
							if m in frequencies:
								penalty += len(frequencies[m])
							penalty *= FREQUENCY_INFLUENCE + no_improve

							if (best_time == -1) or (sched['time'] + penalty < best_time):
								if m in tabus: 
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
				aspiration += 1
##				print("Swapping %s with %s is tabu but great! Gives %s" % (plan[m][j],plan[m][i],best_neighbour['time']))


		if best_time == -1:
			print("No valid neighbour found.")
			break

		# Get swapped operations
		op1 = plan[swap[0]][swap[1]]
		op2 = plan[swap[0]][swap[2]]
		
		print("Swapped: %s with %s -- Current schedule's time: %s" % (op1,op2,best_neighbour['time']))

		# Update the best schedule and no-improvement-counter
		if best_neighbour['time'] >= best_schedule['time']:
			no_improve +=1
		else:
			best_schedule = best_neighbour
			no_improve = 0

		# Update tabus and add new tabu
		for machine in list(tabus):
			if tabus[machine] > 1:	
				tabus[machine] -= 1 
			else:
				del tabus[machine]
		tabus[swap[0]] = RECENCY_MEMORY

		# Update frequency memory
		for machine in list(frequencies):
			if frequencies[machine][0] == (iteration - FREQUENCY_MEMORY): 
				frequencies[machine].pop(0)
				if len(frequencies[machine]) == 0: del frequencies[machine]

		if swap[0] in frequencies:
			frequencies[swap[0]].append(iteration)
		else:
			frequencies[swap[0]] = [iteration]

		iteration += 1

		# Make the plan giving the best neighbour the starting point for the next iteration
		plan = generate_neighbour(plan, swap[0], swap[1], swap[2])

	print("valid: %s, invalid: %s, aspiration %s, iterations %s" % (valid,invalid,aspiration, iteration))
	return best_schedule

def set_dynamic_parameters(plan, weights=(0.5, 2, 0.3)):
	global RECENCY_MEMORY, FREQUENCY_MEMORY, FREQUENCY_INFLUENCE
	jobs = plan['jobs']
	steps = plan['steps']
	machines = plan['machines']
	(recency_weight, frequency_weight, influence_weight) = weights
	RECENCY_MEMORY = machines*recency_weight									# How long are specific swaps tabu?
	FREQUENCY_MEMORY = machines*frequency_weight								# For how many steps do we remember our moves
	FREQUENCY_INFLUENCE = round((influence_weight * math.sqrt(jobs * steps)),2)		# Weight for the influence of the frequency
	print("Swaps are Tabu for %s steps" % RECENCY_MEMORY)
	print("Frequency Memory remembers the past %s steps" % FREQUENCY_MEMORY)
	print("Weight of frequency of moves is %s" % FREQUENCY_INFLUENCE)
	print("")

def tabu_search(instance, mode = MODE, weights=(0.5, 2, 0.3)):
	instance_path = 'instances/' + instance + '.txt'
	if not path.exists(instance_path):
		raise SystemExit("There is no instance at %s" % instance_path)

	# Get plan for the chosen instance
	### Note: Will always give a valid schedule, due to how we get the plan from the instance
	plan = parse_instance(instance_path) # plan is a dict, also contains machine, step and job numbers

	set_dynamic_parameters(plan, weights)

	# Run the tabu search for fixed number of starting points
	best_time = -1
	times = []
	for i in range(TRIES):
		if mode == 'Active':
			plan = random_plan(plan)
		elif mode == 'Experimental':
			plan = fixed_plan(plan, i, instance)
		else:
			raise SystemExit("The MODE variable is set to an undefined value!")

		schedule = search_schedule(plan)
		times.append(schedule['time'])

		print("Best Schedule in %s. Run: %s" % (i+1,schedule['time']))
		print("++++++++++++++++++++")
		print("")

		if (best_time < 0) or (schedule['time'] < best_time):
			best_time = schedule['time']
			best_schedule = schedule

	best_schedule['steps'] = plan['steps']
	best_schedule['jobs'] = plan['jobs']
	best_schedule['machines'] = plan['machines']

	return (best_time, best_schedule, times)

def main():
	start_time = time.time()

	# Decide, on which instance to test our code
	if len(sys.argv) > 1:
		# you may run the script with a name of an instance as the argument
		instance = sys.argv[1]
	else: 
		# default if no argument is passed
		instance = 'simple'

	# Run the search
	(optimum, optimum_schedule, times) = tabu_search(instance)

	# Output
	execution_time = round(time.time() - start_time)
	print("Program takes %s minutes and %s seconds to run" \
		% (round(execution_time / 60), execution_time % 60) )
	print_schedule(optimum_schedule)

if __name__ == "__main__": main()