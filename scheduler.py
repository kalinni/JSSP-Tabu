import sys
from os import path
from instanceparser import parse_instance
from realize_plan import realize_plan
from neighbourhood import generate_neighbour

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

	# Run the code we have so far
	plan = parse_instance(instance)
	schedule = realize_plan(plan)

	machines = plan['machines']
	jobs = plan['jobs']

	# Output to check our results
	if schedule[1] < 0: 
		print("Couldn't schedule all jobs with this plan")
	else:
		for m in range(machines):
			print("Machine %s:" % m)
			for op in schedule[0][m]:
				if op[0].machine != m: 
					print("Job %s is on the wrong machine." % op[0])
				if op[2] - op[1] != op[0].duration:
					print("Job %s takes a wrong amount of time, it takes %s" % (op[0], op[2]-op[1]))
				print('--- %s.%s start %s duration %s' % (op[0].job, op[0].step, op[1], op[0].duration))

	#Check neighbourhood
	best_value = -1
	for m in range(machines):
		for i in range(len(plan[m])):
			neighbour = generate_neighbour(plan, m, i)
			sched = realize_plan(neighbour)
			if sched[1] > 0:
				if (best_value < 0) or (sched[1] < best_value):
					best_value = sched[1]
					new_schedule = sched[0]
					swap = (m, i)
	print(swap)



if __name__ == "__main__": main()