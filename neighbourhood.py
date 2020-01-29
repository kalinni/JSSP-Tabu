import copy

#generates one neighbour (plan) by swapping steps at index a and index b on indicated machine
#returns False if swap fails
def generate_neighbour(plan, machine, index_a, index_b):
	if plan[machine][index_a].job == plan[machine][index_b].job:		# Swapping generates an impermissible schedule 
		return False													# when two steps of the same job are swapped
		
	for index in range(index_a + 1, index_b):							# Swapping also generates an impermissible schedule
		if (plan[machine][index].job == plan[machine][index_a].job		# when any step in-between belongs to either of
			or plan[machine][index].job == plan[machine][index_b].job):	#  the swapped steps
			return False
	
	#copy original plan and swap elements
	neighbour = copy.deepcopy(plan)	#shallow copy would cause change in the original plan
	swapElement = neighbour[machine][index_a]
	neighbour[machine][index_a] = neighbour[machine][index_b]
	neighbour[machine][index_b] = swapElement

	return neighbour