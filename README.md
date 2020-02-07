# JSSP-Tabu

This is an implementation of the tabu search algorithm for solving the Job Shop Scheduling Problem (JSSP). It was done as a solution to the practical task for the Problem Solving and Search in AI lecture at TU Dresden.

## Our Vocabulary for the JSSP

A JSSP has several jobs consisting of several steps each. We call one such step an _operation_. Each operation can be performed by only one machine. 

Given are _instances_ for the JSSP, where operations are sorted by their jobs. We parse those instances into _plans_. A plan has all operations sorted by machine and already gives the order in which they are executed.

However, a plan does not contain start and end times for the operations. To get those, a plan is turned into its corresponding _schedule_. 

Notice: Not every plan generated during a run of our tabu search can be turned into a complete schedule - some plans contain deadlocks caused by dependencies between machines. As our code only checks for a reasonable order of operations located on the same machine before trying to schedule a plan, those deadlocks will only be found during scheduling.

## Our Tabu Search Implementation

### Neighbourhood
Our tabu search algorithm constructs the neighbourhood of a plan by considering all plans obtained through swapping two ''adjacent'' operations on one machine. We decided on resticting swaps to neighbouring operations to keep the runtime from blowing up. To avoid getting stuck in a local optimum too easily, the algorithm is allowed to swap any two steps of the same machine when no improvement has been found in a number of iterations. This way we get a good tradeoff between runtime of the algorithm and runtime of the resulting best schedule.

### Evaluation
The evalutation of the neighbouring plans is done by creating the corresponding schedules and getting their respective runtimes. A runtime of -1 is returned for plans that contain deadlocks.

### Recency Memory/Tabu List
We tried several versions of the tabu list for our algorithm:
1. tabu on both operations of the performed swap (i.e. both can not take part in any swaps for a while)
2. tabu only on the swap undoing the performed swap
3. tabu on the machine on which the swap took place

Performance increased when we decided to move to tabus on machine level, probably because the number of operations or potential swaps in total was too big compared to the total number of iterations we would usually see before termination of the algorithm.

The current implementation therefore has a recency memory storing the machines the performed swaps occured on.

### Aspiration criterion
To improve the results further, we have implemented a simple aspiration criterion to allow for good swaps to still happen, even if the respective machine is currently on the tabu list. Moving to machine based tabus caused the aspiration criterion to actually be relevant. With operation based tabus we almost never saw any use of the criterion.

### Frequency Memory
The same happened with the frequency memory. Here, too, we started by remembering how often operations where part of swaps and moved on to remembering only the machine numbers instead. The frequencies are used to compute a penalty which is added to the time returned for the neighbour during evaluation. The penalties influence increases when no improvement occures for several iterations.

### Termination
The tabu search terminates when no better swap has been found for a number of iterations.


## Parameters of the algorithm

While the algorithm has been able to perform reasonably well, there are still a number of values that we have not been able to find optimal values for. The general mechanisms of the algorithm work as outlined above, but concrete runs of the algorithm are usually influenced by the parameters described below. 
It is possible to set concrete parameters as input values for the tabu search. Default values (for which we obtained good results among the different test instances) are hard-coded. All of these values depend on the concrete problem instance, and coefficients can be set to influence their values.
* RECENCY_MEMORY : After a swap has been performed, the machine will be tabu for this many following swaps
* FREQUENCY_MEMORY : A move will be remembered for the frequency-based penalty for this number of steps
* FREQUENCY_INFLUENCE : This weight will be used to control the influence of the frequency-based penalty

These values influence the algorithm, but we have decided to hardcode their values in the source code.
* NO_IMPROVEMENT_MAX : This value sets the number of plans the algorithm will explore before terminating the run
* NO_IMPROVEMENT_SWITCH : After this many steps without improvement will the algorithm allow arbitrary swaps 
* TRIES : To improve the result, the algorithm performs more this number of iterations with different starting plans
* MODE : In order to optimize parameter (and eliminate the influence of the starting plan), it is possible to fall back on precomputed starting plans. This is only utilized in mode 'Experimental' 

## Running our Code

Type the following into your command line
```

python searcher.py la26

```
This will run a tabu search for the la26 instance. You can also leave the parameter, the code will then take a very simple and tiny test instance as default.

## Checking our results

__evaluator.py__ has a method called ```output\_serial\_results()``` which will simply print our best results for some of the benchmark instances to the command line. In addition there are several methods we used to test varous parameter configurations and a method performance() which calculates means and standard deviations of results, compares them to the known optimums for the benchmark instances and generates a chart containing those information. Those charts can also be found in the results folder.

## Some Notes on the Content and Structure of the Repository

Folders:
- instances/
  - contains all instances from http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt separeted into separate files
- plans/
  - Contains binaries of lists of plans for those instances
  - These plans are the starting points for tabu search iterations in experimental mode
- results/
  - Results of various tests with the benchmark instances
  - .txt files are binaries used by the methods in evaluator.py to store results
  - .png contain charts generated from those results
  - Files in the sub folder contain results from runs with operation-level recency and frequency memories
- other/
  - The original jobshop1.txt file and our slides for the status talk.

Python files:
- searcher.py
  - This is the __main file__, it contains the methods and structure for the search, for recency and frequency memories, a print\_schedule function and a main method. 
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
- evalutor.py
  - Methods to evaluate how our search algorithm is performing on the given __benchmark instances__.

