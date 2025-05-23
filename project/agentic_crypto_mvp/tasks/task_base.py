class TaskBase:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def execute(self):
        raise NotImplementedError("You must implement the execute method in the subclass.")
    
    def __repr__(self):
        return f"<Task(name={self.name}, description={self.description})>"