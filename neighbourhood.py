from operation import Operation
import instanceparser

#generates one neighbour by swapping indicated step in plan one position forward
#returns False if swap fails
def generate_neighbour(plan, machine, index):
	if index == 0:
		return False
	if plan[machine][index].job == plan[machine][index - 1].job:
		return False

##########################################	->code performs swap in-place (original plan gets changed)!
#	swapElement = plan[machine].pop(index)
#	plan[machine].insert(index - 1, swapElement)
##########################################

	neighbour = dict()
	neighbour['machines'], neighbour['jobs'], neighbour['steps'] = plan['machines'], plan['jobs'], plan['steps']
	for m in range(neighbour['machines']):
		row = [plan[m][i] for i in range(len(plan[m]))]
		if m == machine:
			swapElement = row.pop(index)
			row.insert(index-1, swapElement)
		neighbour[m] = row

	return neighbour