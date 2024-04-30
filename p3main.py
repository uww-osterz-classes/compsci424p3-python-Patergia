"""
COMPSCI 424 Program 3
Name: 
"""

import os
import sys
import threading  # standard Python threading library

# (Comments are just suggestions. Feel free to modify or delete them.)

# When you start a thread with a call to "threading.Thread", you will
# need to pass in the name of the function whose code should run in
# that thread.

# If you want your variables and data structures for the banker's
# algorithm to have global scope, declare them here. This may make
# the rest of your program easier to write. 
available = []
max = []
allocation = []
request = []
# Most software engineers say global variables are a Bad Idea (and 
# they're usually correct!), but systems programmers do it all the
# time, so I'm allowing it here.


# Let's write a main method at the top
def main():
    # Code to test command-line argument processing.
    # You can keep, modify, or remove this. It's not required.
    if len(sys.argv) < 3:
        sys.stderr.write("Not enough command-line arguments provided, exiting.")
        sys.exit(1)

    print("Selected mode:", sys.argv[1])
    print("Setup file location:", sys.argv[2])

    # 1. Open the setup file using the path in argv[2]
    num_resources = 0
    num_processes = 0
    with open(sys.argv[2], 'r') as setup_file:
        # 2. Get the number of resources and processes from the setup
        # file, and use this info to create the Banker's Algorithm
        # data structures
        num_resources = int(setup_file.readline().split()[0])
        print(num_resources, "resources")
        num_processes = int(setup_file.readline().split()[0])
        print(num_processes, "processes")

        # 3. Use the rest of the setup file to initialize the data structures
        setup_file.readline() #skip past "availible"

        available = setup_file.readline().split()
        available = list(map(int, available)) #convert characters to int
        print("available resources:\n", available)

        setup_file.readline() #skip past "max"

        for i in range(num_processes): #initialize max
            max.append(setup_file.readline().split())
            max[i] = list(map(int, max[i]))

        print("maximum resources:\n", max)

        setup_file.readline() #skip past "allocation"

        for i in range(num_processes): #initialize allocation
            allocation.append(setup_file.readline().split())
            allocation[i] = list(map(int, allocation[i]))

        print("resource allocation:\n", allocation)


        request = [[0 for i in range(num_resources)] for j in range(num_processes)]
        print("current requests:\n", request)



    
    # 4. Check initial conditions to ensure that the system is
    # beginning in a safe state: see "Check initial conditions"
    # in the Program 3 instructions
    banker = BankersAlgorithm(available, max, allocation, request)
    if banker.is_safe_state():
        print("is safe state")
    else:
        print("unsafe")
    # 5. Go into either manual or automatic mode, depending on
    # the value of args[0]; you could implement these two modes
    # as separate methods within this class, as separate classes
    # with their own main methods, or as additional code within
    # this main method.

# fill in other methods here as desired
#def manual_mode(banker):
#    go = True
#    print("manual mode has begun. Please enter release, request, or end commands.")
#    while go:
#        input = input()
#        if

class BankersAlgorithm:
    def __init__(self, available, max, allocation, request) -> None:
        self.available = available
        self.max = max
        self.allocation = allocation
        self.request = request
        self.num_resources = len(available)
        self.num_processes = len(max)
        self.need = [[0 for i in range(self.num_resources)] for j in range(self.num_processes)]
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.need[i][j] = max[i][j] - allocation[i][j]

    def is_safe_state(self):
        work = list(self.available)
        finish = [False] * self.num_processes
        while True:
            found = False
            for i in range(self.num_processes):
                if not finish[i] and all(need <= work[j] for j, need in enumerate(self.need[i])):
                    work = [work[j] + self.allocation[i][j] for j in range(self.num_resources)]
                    finish[i] = True
                    found = True
            if not found:
                break
        return all(finish)
    
    def request(self, pID, request):
        for i in range(self.num_resources):
            if request[i] > self.need[pID][i] or request[i] > self.available[i]:
                return False
        
        for i in range(self.num_resources):
            self.allocation[pID][i] += request[i]
            self.need[pID][i] -= request[i]
            self.available[i] -= request[i]
        
        if self.is_safe_state():
            return True
        else:
            for i in range(self.num_resources):
                self.allocation[pID][i] -= request[i]
                self.need[pID][i] += request[i]
                self.available[i] += request[i]
            return False
        
    def release(self, pID, release):
        valid = True
        for i in range(self.num_resources):
            if release[i] < 0 or allocation[pID][i] - release[i] < 0:
                print("ERROR: invalid release")
                return
            
            available[i] += request[i]
            self.allocation[pID][i] -= request[i]
            self.max[pID][i] -= request[i]
            self.need[pID][i] -= request[i]

    

main() # call the main function