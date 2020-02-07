#this function calculates an optimal schedule from the given plan (i.e. order of steps on every machine)
def realize_plan (plan):
	#store the number of jobs, steps and machines for easier access
	jobs, steps, machines = plan['jobs'], plan['steps'], plan['machines']

	#enabled tracks at which point in time a step is 'enabled' (i.e. its predecessor step has finished)
	enabled = [[0 if s == 0 else -1 for s in range(steps)] for j in range(jobs)]

	schedule = { m:[] for m in range(machines) }
	following = {m:0 for m in range(machines)}			# following tracks the next step for every machine

	# for every machine, check whether the next planned step is already enabled 
	# if so: insert that step into the schedule
	# if no step can be inserted: plan is blocking and thus impermissible (deadlock occurred)
	blocked = False
	while not blocked:
		blocked = True
		for m in range(machines):
			if following[m] < len(plan[m]):
				j, s = plan[m][following[m]].job, plan[m][following[m]].step
				if enabled[j][s] != -1:
					blocked = False
					if schedule[m]:
						start = max(schedule[m][-1][2], enabled[j][s])
					else:
						start = enabled[j][s]
					finish = start + plan[m][following[m]].duration
					schedule[m].append( ( plan[m][following[m]], start, finish ) )
					following[m] += 1
					if s < steps -1:
						enabled[j][s+1] = finish 	# after inserting step s, the successor step s+1 is enabled

	#finished checks whether schedule is complete (i.e. no deadlock)
	finished = True    
	for m in range(machines):
		finished = finished and (following[m] >= len(plan[m]))

	#time records the number of machine cycles needed for the schedule (in case the plan is permissible), otherwise: -1
	time =-1
	if finished:
		for m in range(machines):
			time = max(time, schedule[m][-1][2])
	schedule['time']=time

	#output: dictionary with the following keys and values
	# machinenumber 	-> List of 3-tuples (Step, starting time, finish time) for the respective machine
	#		   time    	-> number of machine cycles needed for the plan
	return schedule