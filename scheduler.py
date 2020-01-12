import sys
from os import path
from instanceparser import parse_instance
from realize_plan import realize_plan
from neighbourhood import generate_neighbour

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

	# Get a plan from the chosen instance and turn it into a schedule
	### Note: Will always give a valid schedule, due to how we get the plan from the instance
	plan = parse_instance(instance) # plan is a dict
	schedule = realize_plan(plan) # schedule is a tuple, first entry is list of lists of triples, the actual schedule, second entry is the time

	machines = plan['machines']
	jobs = plan['jobs']

	# Check neighbourhood
	best_schedule = schedule
	for m in range(machines):
		for i in range(len(plan[m])):
			neighbour = generate_neighbour(plan, m, i)
			if neighbour != False:
				sched = realize_plan(neighbour)
				if sched[1] > 0:
					if (sched[1] < best_schedule[1]):
						best_schedule = sched
						swap = (m, i)
	# Output
	print_schedule(best_schedule)



if __name__ == "__main__": main()