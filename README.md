# JSSP-Tabu

This is an implementation of the tabu search algorithm for solving the Job Shop Scheduling Problem. It was done as a solution to the practical task for the Problem Solving and Search in AI lecture at TU Dresden.

## Our Vocabulary for the JSSP

A JSSP has several jobs consisting of several steps each. We call one such step an _operation_. Each operation can be performed by only one machine. 

Given are _instances_ for the JSSP, where operations are sorted by their jobs. We parse those instances into _plans_. A plan has all operations sorted by machine and already gives the order in which they are executed.

However, a plan does not contain start and end times for the operations. To get those, a plan is turned into a _schedule_.

Not every plan generated during a run of our tabu search can be turned into a complete schedule - some contain deadlocks caused by dependencies between machines. Our code only checks for a reasonable order of operations located on the same machine before trying to schedule a plan.

[//]: # Include Tries, Iterations and the other parameters here or, better, in an extra section

## Running our Code

Type the following into your command line
```

python searcher.py la26

```
This will run a tabu search for the la26 instance. You can also leave the parameter, the code will then take a very simple and tiny test instance as default.

## Checking our results

__evaluator.py__ has a method called ```output\_serial\_results()``` which will so far simply print our best results for some of the benchmark instances to the command line.


## Structure and Content of the Repository

Folders:
- __instances/__
  - contains all instances from http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt separeted into separate files
- plans/
  - Contains binaries of lists of plans for those instances
  - These plans are the starting points for tabu search iterations in experimental mode
- results/
  - The results of our test with the benchmark instances
  - results.txt is a binary used by the methods in evaluator.py
  - The excel file contains some of our notes from playing around with parameters.
- other/
  - The original jobshop1.txt file and our slides for the status talk.

Python files:
- __searcher.py__
  - This is the main file, it contains the methods and structure for the search, for recency and frequency memories, a print\_schedule function and a main method. 
- neighbourhood.py
  - Contains the function that returns a neighbour for a given plan. The function takes two indices and is capable of doing long distant swaps on a machine and checking them for reasonability if asked to.
- operation.py
  - Contains only a class for operations. Each operation contains its job, machine, step (which step of the job it is) and duration.
- jssp\_parser.py
  - Function to turn a given instance into a plan (and the script that separeted jobshop1.txt).
- planner.py
  - Functions to create either a random starting point for the tabu search (i.e. a random plan) from another plan or give pregenerated plans to enable us to compare runtime and result for a fixed set of starting points.
- scheduler.py
  - The method to turn a plan into a schedule. This resamples the evaluation function of our tabu search.
- __evalutor.py__
  - Methods to evaluate how our search algorithm is performing on the given benchmark instances.

