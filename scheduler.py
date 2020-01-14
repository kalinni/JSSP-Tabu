import sys
from os import path
from instanceparser import parse_instance
from realize_plan import realize_plan
from neighbourhood import generate_neighbour

RECENCY_MEMORY = 5
NO_IMPROVE_MAX = 20

def print_schedule(schedule):
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
				print('--- %s.%s start %s duration %s' % (op[0].job, op[0].step, op[1], op[0].duration))

def search_schedule(instance):

	# Get a plan from the chosen instance and turn it into the initial schedule
	### Note: Will always give a valid schedule, due to how we get the plan from the instance
	plan = parse_instance(instance) # plan is a dict
	schedule = realize_plan(plan) # schedule is a tuple, first entry is list of lists of triples, the actual schedule, second entry is the time

	machines = plan['machines']

	# Start Tabu Search
	best_schedule = schedule
	no_improve = 0
	tabus = dict()

	while no_improve < NO_IMPROVE_MAX:
		# Find best neighbour for current plan
		best_time = -1
		for m in range(machines):
			for i in range(len(plan[m])):
				if (m,i) in tabus: continue
				neighbour = generate_neighbour(plan, m, i)
				if neighbour != False:
					sched = realize_plan(neighbour)
					if sched[1] > 0:
						if (best_time == -1) or (sched[1] < best_time):
							best_neighbour = sched
							best_time = sched[1]
							swap = (m, i)
		if best_time == -1:
			print("No valid neighbour found.")
			break
		print("Swapped: %s -- Current schedule's time: %s" % (swap,best_time))

		# Update the best schedule and no-improvement-counter
		if best_time >= best_schedule[1]:
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
		tabus[swap] = RECENCY_MEMORY

		# Make the plan giving the best neighbour the starting point for the next iteration
		plan = generate_neighbour(plan, swap[0], swap[1])

	return best_schedule
	

def main():
	# Decide, on which instance to test our code
	if len(sys.argv) > 1:
		# you may run the script with a path to an instance as the argument
		if path.exists(sys.argv[1]):
			instance = sys.argv[1]
		else: 
			raise SystemExit("There is no instance at %s" % sys.argv[1])
	else: 
		# default if no argument is passed
		instance = 'instances/simple.txt'

	# Run the tabu search
	best_schedule = search_schedule(instance)

	# Output
	print_schedule(best_schedule)

if __name__ == "__main__": main()