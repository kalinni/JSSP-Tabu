import sys
from os import path
from instanceparser import parse_instance
from realize_plan import realize_plan
from neighbourhood import generate_neighbour
import random

RECENCY_MEMORY = 5
NO_IMPROVE_MAX = 20
ITERATIONS = 5


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
			if i<=len(t) - 1:
				if t[i][1] > t[i+1][0]:
					print("Steps from the same Job overlap: %s" % t)




def random_instance(plan):	#constructs a random schedule by repeatedly picking the next step to be sorted
	next_step = [0 for i in range(plan['jobs'])]
	new_plan = dict()

	new_plan['machines'], new_plan['jobs'], new_plan['steps'] = plan['machines'], plan['jobs'], plan['steps']
	for i in range(new_plan['machines']):
		new_plan[i] = []

	finished = True
	for n in next_step:
		finished = finished and not (n < new_plan['steps'])
	while not finished:
		step = False
		options = [ i for i in range(new_plan['jobs']) if next_step[i] < new_plan['steps'] ]	#Diese Konstruktion nimmt an, dass alle Jobs gleich viele Steps haben
		job = random.choice(options)
		for m in range(plan['machines']):
			i = 0
			while i < len(plan[m]) and not step:
				if plan[m][i].job == job and plan[m][i].step == next_step[job] and not step:
					step = plan[m][i]
					new_plan[m].append(step)
					next_step[job] += 1
					step = True
				i += 1
		finished = True
		for n in next_step:
			finished = finished and not (n < new_plan['steps'])
	
	return new_plan



def search_schedule(plan):
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
		
		# Aspiration Search: If there is tabu neighbour with time better than current optimum 
		# 						and best found swap, choose tabu swap instead
		threshold = min(best_time, best_schedule[1])
		for (m, i) in tabus:
			neighbour = generate_neighbour(plan, m, i)
			if neighbour != False:
				sched = realize_plan(neighbour)
				if sched[1] > 0:
					if (sched[1] < threshold):
						best_neighbour = sched
						best_time = sched[1]
						threshold = best_time
						swap = (m, i)
		
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

	# Make a plan from the chosen instance and turn it into the initial schedule
	### Note: Will always give a valid schedule, due to how we get the plan from the instance
	plan = parse_instance(instance) # plan is a dict

	# Run the tabu search
	optimum = -1
	for i in range(ITERATIONS):
		best_schedule = search_schedule(plan)
		print("++++++++++++++++++++")
		print("Best Schedule in Run: %s" % best_schedule[1])
		if optimum < 0:
			optimum = best_schedule[1]
			optimum_schedule = best_schedule
		else :
			if best_schedule[1] < optimum:
				optimum = best_schedule[1]
				optimum_schedule = best_schedule
		plan = random_instance(plan)

	# Output
	print_schedule(optimum_schedule, plan)

if __name__ == "__main__": main()