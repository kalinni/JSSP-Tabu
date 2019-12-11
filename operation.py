class Operation():
    """Operations form the various steps of a job for the JSSP"""
    def __init__(self, job, step, duration, machine):
        self.job=job
        self.step=step
        self.duration=duration
        self.machine=machine
    def __eq__(self, other):
        return self.job == other.job and self.step == other.step