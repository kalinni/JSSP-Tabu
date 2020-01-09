from operation import Operation
import copy
import instanceparser

#generates one neighbour by swapping indicated step in plan one position forward
#returns False if swap fails
def generate_neighbour(plan, machine, index):
	if index == 0:
		return False
	if plan[machine][index].job == plan[machine][index - 1].job:
		return False
	
	#copy original plan and swap elements
	neighbour = copy.deepcopy(plan)	#shallow copy would cause change in the original plan
	swapElement = neighbour[machine].pop(index)
	neighbour[machine].insert(index-1, swapElement)

	return neighbour