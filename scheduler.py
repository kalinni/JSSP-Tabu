import sys
from os import path
import math
import time

from instanceparser import parse_instance
from realize_plan import realize_plan
from neighbourhood import generate_neighbour
from planner import random_plan, fixed_plan
import parameters

MODE = 'Experimental'	# MODE variable shows whether the program is supposed to measure performance 
						# on a preset list of plans ('Experimental') or supposed to run for arbitrary plans ('Active')

def print_schedule(schedule, plan):
	timetable = [ [ 0 for s in range(plan['steps']) ] for j in range(plan['jobs']) ]
	if schedule[1] < 0: 
		print("Couldn't schedule all jobs with this plan")
	else:
		print("Schedule takes %s time intervals" % schedule[1])
		for m in schedule[0]:
			print("Machine %s:" % schedule[0].index(m))
			for op in m:
				if op[0].machine != schedule[0].index(m): 
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







def search_schedule(plan):
	schedule = realize_plan(plan) # schedule is a tuple, first entry is list of lists of triples, the actual schedule, second entry is the time

	machines = plan['machines']

	# Start Tabu Search
	best_schedule = schedule
	no_improve = 0
	tabus = dict()
	frequencies = dict()
	iteration=0

	while no_improve < globals()['no_improvement']:
		# Find best neighbour for current plan
		best_time = -1
		aspiration_check = []
		for m in range(machines):
			for i in range(len(plan[m])):
				if (plan[m][i-1],plan[m][i]) in tabus: 
					print("Swapping %s with %s is tabu!" % (plan[m][i-1],plan[m][i]))
					aspiration_check.append((m,i))
					continue
				neighbour = generate_neighbour(plan, m, i)
				if neighbour != False:
					sched = realize_plan(neighbour)
					if sched[1] > 0:
						penalty = 0
						if plan[m][i-1] in frequencies:
							penalty += len(frequencies[plan[m][i-1]])
						if plan[m][i] in frequencies:
							penalty += len(frequencies[plan[m][i]])
						penalty *= globals()['frequency_influence']
						if (best_time == -1) or (sched[1] + penalty < best_time):
							best_neighbour = sched
							best_time = sched[1] + penalty
							swap = (m, i)
		
		# Aspiration Search: If there is tabu neighbour with time better than current optimum 
		# 						and best found swap, choose tabu swap instead
		threshold = min(best_time, best_schedule[1]) if best_time > 0 else best_schedule[1]
		for (m,i) in aspiration_check:
			neighbour = generate_neighbour(plan, m, i)
			if neighbour != False:
				sched = realize_plan(neighbour)
				if sched[1] > 0:
					penalty = 0
					if plan[m][i-1] in frequencies:
						penalty += len(frequencies[plan[m][i-1]])
					if plan[m][i] in frequencies:
						penalty += len(frequencies[plan[m][i]])
					penalty *= globals()['frequency_influence']
					if (sched[1] + penalty < threshold):
						best_neighbour = sched
						best_time = sched[1] + penalty
						threshold = best_time
						swap = (m, i)
						print("Swapping %s with %s is tabu but great! Gives %s" % (plan[m][i-1],plan[m][i],best_neighbour[1]))


		if best_time == -1:
			print("No valid neighbour found.")
			break

		# Get Operations swapped
		op1 = plan[swap[0]][swap[1]]
		op2 = plan[swap[0]][swap[1] - 1]
		
		print("Swapped: %s with %s -- Current schedule's time: %s" % (op1,op2,best_neighbour[1]))

		# Update the best schedule and no-improvement-counter
		if best_neighbour[1] >= best_schedule[1]:
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
		tabus[(op1,op2)] = globals()['recency_memory']

		# Update frequency memory
		for operation in list(frequencies):
			if frequencies[operation][0] == (iteration - globals()['frequency_memory']): 
				frequencies[operation].pop(0)
				if len(frequencies[operation]) == 0: del frequencies[operation]

		if op1 in frequencies:
			frequencies[op1].append(iteration)
		else:
			frequencies[op1] = [iteration]

		if op2 in frequencies:
			frequencies[op2].append(iteration) 
		else:
			frequencies[op2] = [iteration]

		iteration += 1

		# Make the plan giving the best neighbour the starting point for the next iteration
		plan = generate_neighbour(plan, swap[0], swap[1])

	return best_schedule
	

def main():
	start_time = time.time()
	#set global values
	globals()['recency_memory'] = parameters.RECENCY_MEMORY
	globals()['frequency_memory'] = parameters.FREQUENCY_MEMORY
	globals()['no_improvement'] = parameters.NO_IMPROVE_MAX
	globals()['tries'] = parameters.TRIES

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
	for i in range(globals()['tries']):
		if MODE == 'Active':
			plan = random_plan(plan)
		if MODE == 'Experimental':
			plan = fixed_plan(plan, i, instance)
		if not MODE == 'Active' and not MODE == 'Experimental':
			raise SystemExit("The MODE variable is set to an undefined value!")
		best_schedule = search_schedule(plan)
		print("")
		print("Best Schedule in Run: %s" % best_schedule[1])
		print("++++++++++++++++++++")
		print("")
		if optimum < 0:
			optimum = best_schedule[1]
			optimum_schedule = best_schedule
		else :
			if best_schedule[1] < optimum:
				optimum = best_schedule[1]
				optimum_schedule = best_schedule

	# Output
	execution_time = round(time.time() - start_time)
	print("Program takes %s minutes and %s seconds to run" \
		% (round(execution_time / 60), execution_time % 60) )
	print_schedule(optimum_schedule, plan)


def set_dynamic_parameters(plan):
	jobs = plan['jobs']
	steps = plan['steps']
	weight = 0.25 * math.sqrt(jobs * steps)
	globals()['frequency_influence'] = weight
	print("Weight of frequent move is %s" % round(weight))
	

if __name__ == "__main__": main()