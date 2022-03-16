from multiprocessing import Condition, Lock, Value

class Table():
    def __init__(self,NPHIL, manager):
        self.current_phil = None
        self.forks = manager.list([True for i in range(NPHIL)])
        self.nphil = NPHIL
        self.mutex = Lock()
        self.free_fork = Condition(self.mutex)  #only one becasue only one can enter one at a time

    def set_current_phil(self, phil): #set which philosopher for future events
        self.current_phil = phil

    def get_current_phil(self): #get which philospher that wants to eat
        return self.current_phil

    def fork_available(self):   #check if yours and the person to the right have free forks
        phil = self.get_current_phil()
        return self.forks[phil] and self.forks[(phil+1)%self.nphil] #returns true if both are true

    def wants_eat(self, phil):  #look if two forks are availble and if so eating
        self.mutex.acquire()
        self.free_fork.wait_for(self.fork_available)    #eating, forks occupied
        self.forks[phil] = False
        self.forks[(phil + 1) % self.nphil] = False
        self.mutex.release()

    def wants_think(self,phil): #has been eating and starts thinking againg
        self.mutex.acquire()
        self.forks[phil] = True     #need to free the forks so they are available to others
        self.forks[(phil + 1) % self.nphil] = True
        self.free_fork.notify_all() #let all now that the fork[phil] is free
        self.mutex.release()


class CheatMonitor(): #destroy for the one who wants to eat
    def __init__(self):
        self.mutex = Lock()
        self.other_is_eating = Condition(self.mutex)
        self.eating = Value('i', 0)
        self.thinking = Value('i', 0)

    def wants_think(self,num):
        self.mutex.acquire()
        self.other_is_eating.wait_for(lambda : self.eating.value==2)
        self.eating.value -= 1
        self.mutex.release()

    def is_eating(self,num):
        self.mutex.acquire()
        self.eating.value += 1
        self.other_is_eating.notify()
        self.mutex.release()






