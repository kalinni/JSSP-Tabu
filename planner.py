import operation
import pickle
import random
from os import path


def random_plan(plan):	#constructs a random schedule by repeatedly picking the next step to be sorted
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

def fixed_plan(plan, index, instance):
	file_path = "plans/" + instance + ".txt"
	plans = []
	if not path.exists(file_path):
		file = open(file_path, "wb")
		for i in range(15):
			new_plan = random_plan(plan)
			plans.append(new_plan)
		pickle.dump(plans, file)
		file.close()
	file = open(file_path, "rb")
	plans = pickle.load(file)
	file.close()
	return plans[index]