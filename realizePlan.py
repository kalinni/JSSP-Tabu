from operation import Operation
import functools
import operator

foldl = lambda func, acc, xs: functools.reduce(func, xs, acc) # akkumuliert eine Liste von links 

jobs, steps, machines = 4, 5, 4

 #diese Funktion erhält eine Liste der Steps auf den Maschinen
 #und erzeugt eine optimale Schedule für diese Reihenfolge
def realizePlan (plan):        

    #enabled tracked, ab welchem Zeitpunkt ein Step erlaubt ist
    enabled = [[if j == 0: 0 else sys.maxint for j in range(steps)] for i in range(jobs)]

    #schedule enthält für die Maschinen je eine Liste von 3-Tupeln (Step, Startzeit, Endzeit)
    schedule = [ [] for m in range(machines) ]

	#blocked zeigt an, ob es keine steps mehr gab, die einsortiert werden konnten 
    #(tritt auch ein, wenn alle steps einsortiert wurden)
	blocked = False

	while not blocked:
		blocked = True
		for m in range(machines):   #teste für alle Maschinen, ob der nächste step einsortiert werden kann
			machinePlan = plan[m]
			if machinePlan:
				op = machinePlan[0]]
                j, s = op.job, op.step
				if enabled[t][s] <= schedule[m][-1][2]:
                    blocked = False
					schedule[m].append( ( machinePlan.pop(), schedule[m][-1][2], schedule[m][-1][2]+op.duration ) )
					enabled[t][s+1] = schedule[m][-1][2] #dies ist die Endzeit des neu einsortierten op
    finished = foldl (and) True (map (not) plan)    #finished ist True, wenn alle steps einsortiert wurden
	return [finished, schedule, enabled]