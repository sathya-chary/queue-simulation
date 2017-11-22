#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:54:41 2017

Simulation of an M/D/1 queue.
Customers arrive stochastically (exponential distribution).
Customers are served at a constant rate.
There is only one server.
The average (over several trials) number of customers waiting to be served at 
each time step is simulated and plotted.

@author: chary
"""
import numpy as np
import random
import matplotlib.pyplot as plt

class Queue(object): #Creating a queue object that has enqueue and dequeue methods
    
    def __init__(self, max_length = 1000):
        self.items = []
        self.length = len(self.items)
        self.max_length = max_length
        
    def getLength(self):
        self.length = len(self.items)
        return self.length
    
    def enqueue(self, x):
        current_length = self.getLength()
        if current_length >= self.max_length:
            print ("Queue is full") #Optional warning
            #pass
        else:
            self.items.append(x)
        
    def dequeue(self):
        if self.items == []:
            print("Queue Empty") #Optional warning
            #pass
        else:
            return self.items.pop(0)
            
    def __str__(self):
        return 'Current Queue: ' + str(self.items)
            

numTrials = 100 #Number of trials to average over
maxTime = 100 #Maximum time steps to run the simulation
lambd = 1.5 #Incoming customers modeled as exponential distribution with lambda value
rate_of_service = 1.5 #Rate of service assumed to be deterministic and constant
time_steps = [x for x in range(maxTime)] #Measure queue length at every integer time unit
numInQueueTotNP = np.zeros(maxTime)                        
for trial in range(numTrials): #Conduct several trials of the simulation and use the average
    test_queue = Queue() #Initialize queue for this trial
    numInQueue = []
    time = 0 #Set initial time for this trial
    next_arrival = 0 #Start the simulation with an arrival
    next_outgoing = 1/rate_of_service #Set the intial value of a departure to the time to service the first customer
    next_time_step = 0 #Time steps at which queue length measurements are taken
    while time < maxTime:
        if time == next_arrival:
            test_queue.enqueue(1)
            incoming = random.expovariate(lambd) #Exponential distribution for arrivals
            next_arrival = time + incoming #Calculate next arrival time
            #print(next_arrival)
        if time == next_outgoing:
            queueLength = test_queue.getLength()
            if queueLength > 0: #Check if anyone remaining in queue before dequeuing
                test_queue.dequeue()
            outgoing = 1/rate_of_service #Uniform rate of service (and hence, departures)
            next_outgoing = time + outgoing #Calculate time of next departure
            #print(next_outgoing)
        if time == next_time_step: #Measure queue length at specific times to study growth
            numInQueue.append(test_queue.getLength())
            next_time_step += 1
            #print(next_time_step)
        time = min(next_arrival, next_outgoing, next_time_step) #Set time to next nearest event    
    numInQueueNP = np.array(numInQueue)
    numInQueueTotNP += numInQueueNP #Add results for every trial
AvgNumInQueue = np.array([])
AvgNumInQueue = numInQueueTotNP/numTrials #Find average of all trials at every step
plt.plot(time_steps, AvgNumInQueue, 'bo', label = 'Average No. of Customers Waiting in Line')
plt.legend()
plt.xlabel('Time Step #')
plt.ylabel('Average No. of Customers Waiting')
plt.show()