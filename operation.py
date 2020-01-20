class Operation:
    """Operations form the various steps of a job for the JSSP"""

    def __init__(self, job, step, duration, machine):
        self.job=job
        self.step=step
        self.duration=duration
        self.machine=machine

    def __eq__(self, other):
        return (isinstance(other, type(self))
            and self.job == other.job 
            and self.step == other.step)
    def __hash__(self):
        return hash((self.job,self.step))

    def __str__(self):
        return "Job %s.%s" % (self.job,self.step)
        
    def __repr__(self):
    	return "<Operation job:%s step:%s, duration:%s, machine:%s>" % (self.job,self.step,self.duration,self.machine)