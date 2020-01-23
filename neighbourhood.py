from operation import Operation
import copy

#generates one neighbour by swapping indicated step in plan one position forward
#returns False if swap fails
def generate_simple_neighbour(plan, machine, index):
	if index == 0:
		return False
	if plan[machine][index].job == plan[machine][index - 1].job:
		return False
	
	#copy original plan and swap elements
	neighbour = copy.deepcopy(plan)	#shallow copy would cause change in the original plan
	swapElement = neighbour[machine].pop(index)
	neighbour[machine].insert(index-1, swapElement)

	return neighbour

def generate_complex_neighbour(plan, machine, index_a, index_b):
	if plan[machine][index_a].job == plan[machine][index_b].job:
		return False
	for index in range(index_a + 1, index_b):
		if (plan[machine][index].job == plan[machine][index_a].job
			or plan[machine][index].job == plan[machine][index_b].job):
			return False
	
	#copy original plan and swap elements
	neighbour = copy.deepcopy(plan)	#shallow copy would cause change in the original plan
	swapElement = neighbour[machine][index_a]
	neighbour[machine][index_a] = neighbour[machine][index_b]
	neighbour[machine][index_b] = swapElement

	return neighbour