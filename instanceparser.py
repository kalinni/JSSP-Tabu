from operation import Operation

def parse_instance(file):
	''' 
	This function reads in given instances of the JSSP

	It takes the location of a file containing a single instance of the JSSP as input.
	Example: plan = parse_instance('instances/abz5.txt')
	The output is a dictionary containing:
	    - the number of jobs as the value for the key "jobs"
	    - the number of machines as the value for the key "machines"
	    - the number of steps per job as the value for the key "steps"
	    - all machine numbers as keys with all operations on that specific machine in a list as their values
	'''
	plan = dict()
	with open(file,encoding="utf8") as instance:
		for line in instance:
			try:
				if line.find('instance') > -1: continue
				if line.find('+') > -1: continue
				content = line.split()
				if len(content) == 2:
					plan['jobs'] = int(content[0])
					plan['steps'] = int(content[1])
					job = -1
				if len(content) > 2:
					job += 1
					for i in range(0,len(content),2):
						if int(content[i]) not in plan: plan[int(content[i])]=[]
						plan[int(content[i])].append(Operation(job, int(i/2), int(content[i+1]), int(content[i])))
			except:
				pass
	plan['machines'] = len(plan)-2
	return plan