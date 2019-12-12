import sys
from operation import Operation

jobs, steps, machines = 5, 4, 5 #Anzahl Jobs, Steps pro Job, Maschinen in Probleminstanz

#diese Funktion erhält eine Liste der Steps auf den Maschinen
#und erzeugt eine optimale Schedule für diese Reihenfolge
def realizePlan (plan):
	#enabled tracked, ab welchem Zeitpunkt ein Step erlaubt ist
	enabled = [[0 if j == 0 else sys.maxsize for j in range(steps)] for i in range(jobs)]

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
				op = machinePlan[0]
				j, s = op.job, op.step
				if enabled[j][s] <= schedule[m][-1][2]:
					blocked = False
					schedule[m].append( ( machinePlan.pop(), schedule[m][-1][2], schedule[m][-1][2]+op.duration ) )
					enabled[j][s+1] = schedule[m][-1][2] #dies ist die Endzeit des neu einsortierten op
	finished = True    #finished ist True wenn alle steps einsortiert wurden
	for m in plan:
		finished = finished and (not m)
	return [finished, schedule, enabled]