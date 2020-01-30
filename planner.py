import operation
import pickle
import random
from os import path

#constructs a random plan by repeatedly picking the next step to be performed at random
def random_plan(plan):
	next_step = [0 for i in range(plan['jobs'])]
	new_plan = dict()

	new_plan['machines'], new_plan['jobs'], new_plan['steps'] = plan['machines'], plan['jobs'], plan['steps']

	for i in range(new_plan['machines']):
		new_plan[i] = []
	finished = True
	for n in next_step:											# the loop is performed while there are still steps not
		finished = finished and not (n < new_plan['steps'])		# sorted into the new plan (i.e. not finished)

	while not finished:
		options = [ i for i in range(new_plan['jobs']) 			# choose one job among the ones where
				if next_step[i] < new_plan['steps'] ]				# not all steps have been sorted in yet
		job = random.choice(options)

		insert = False
		for m in range(plan['machines']):						# find job and insert the next step into the new plan
			i = 0
			while i < len(plan[m]) and not insert:
				# find the next step of the chosen job in the old plan and copy it into the new plan
				# insert makes sure that only one job is added in every interation 
				if plan[m][i].job == job and plan[m][i].step == next_step[job] and not insert:
					new_plan[m].append(plan[m][i])
					next_step[job] += 1
					insert = True
				i += 1
		finished = True
		for n in next_step:
			finished = finished and not (n < new_plan['steps'])
	
	return new_plan


# fixed plan loads one of the precomputed plans for a given instance from a binary file
# this function also precomputes plans in case 
def fixed_plan(plan, index, instance):
	file_path = "plans/" + instance + ".txt"
	plans = []
	if not path.exists(file_path):		# if the plans have not been precomputed yet
		file = open(file_path, "wb")	# construct a new file and add 15 random plans
		for i in range(15):
			new_plan = random_plan(plan)
			plans.append(new_plan)
		pickle.dump(plans, file)		# store the computed plans persistently as a binary file
		file.close()
	file = open(file_path, "rb")
	plans = pickle.load(file)
	file.close()
	return plans[index]