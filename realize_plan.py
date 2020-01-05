import sys
from operation import Operation
import instanceparser

#diese Funktion erhält eine Liste der Steps auf den Maschinen
#und erzeugt eine optimale Schedule für diese Reihenfolge
def realize_plan (plan):
	#Anzahl Jobs, Steps pro Job, Maschinen in Probleminstanz
	jobs, steps, machines = plan['jobs'], plan['steps'], plan['machines']

	#enabled tracked, ab welchem Zeitpunkt ein Step erlaubt ist
	enabled = [[0 if s == 0 else -1 for s in range(steps)] for j in range(jobs)]

	#schedule enthält für die Maschinen je eine Liste von 3-Tupeln (Step, Startzeit, Endzeit)
	schedule = [ [] for m in range(machines) ]

	#next zeigt für jede Maschine das nächste Element des Plans an
	next = [0 for m in range(machines)]

	#blocked zeigt an, ob es keine steps mehr gab, die einsortiert werden konnten 
	#(tritt auch ein, wenn alle steps einsortiert wurden)
	blocked = False
	while not blocked:
		blocked = True
		for m in range(machines):   #teste für alle Maschinen, ob der nächste step einsortiert werden kann
			if next[m] < len(plan[m]):
				j, s = plan[m][next[m]].job, plan[m][next[m]].step
				if enabled[j][s] != -1:
					blocked = False
					if schedule[m]:
						start = max(schedule[m][-1][2], enabled[j][s])
					else:
						start = enabled[j][s]
					finish = start + plan[m][next[m]].duration
					schedule[m].append( ( plan[m][next[m]], start, finish ) )
					next[m] += 1
					if s < steps -1:
						enabled[j][s+1] = finish #der nächste Step wird enabled zum Ende des vorherigen 
	#finished testet ob alle steps einsortiert wurden (dh ob die schedule zulässig ist)
	finished = True    
	for m in range(machines):
		finished = finished and (next[m] >= len(plan[m]))

	#time ermittelt die benötigte Zeit falls die schedule zulässig ist
	time =-1
	if finished:
		for m in range(machines):
			time = max(time, schedule[m][-1][2])

	#Ausgabe: schedule -> Liste von 3-Tupeln (Step, Startzeit, Endzeit) je Maschine
	#		  time   ->   benötigte Zeit der Schedule (-1 falls die Schedule ungütig ist)
	return [schedule, time]