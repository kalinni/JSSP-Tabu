from operation import Operation

def separate_instances(file,directory):
	'''
	This function simply separates the instances found in jobshop1.txt into extra files 
	on which the parse_instance function can then be called.

	'''
	with open(file,encoding="utf8") as file:
		first_instance_found = False
		file_created = False
		for line in file:
			if first_instance_found:
				content = line.split()
				if len(content) > 0 and content[0] == 'instance':
					try:
						if file_created: instance.close()
						instance = open(directory + content[1] + ".txt", "x")
						print(directory + content[1] + ".txt was created")
						file_created = True
					except:
						print("File %s.txt already exists." % (content[1]))
						file_created = False
				if file_created: instance.write(line)
			else:
				if line.find(' +++'): first_instance_found = True



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
					plan['machines'] = int(content[1])
					job = -1
				if len(content) > 2:
					if 'steps' not in plan: plan['steps'] = int(len(content)/2)
					job += 1
					for i in range(0,len(content),2):
						if int(content[i]) not in plan: plan[int(content[i])]=[]
						plan[int(content[i])].append(Operation(job, int(i/2), int(content[i+1]), int(content[i])))
			except:
				pass
	return plan