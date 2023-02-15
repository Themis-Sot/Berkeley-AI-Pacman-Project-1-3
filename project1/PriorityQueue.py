import heapq

"""analutiki eksigisi tis leitourgias sto README!!"""

class PriorityQueue:

    heap = []
    count = 0
    

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))
        self.count += 1
        return None

    def pop(self):
        if self.count > 0:
            popped = heapq.heappop(self.heap)
            self.count -= 1
            return popped[1]
        

    def isEmpty(self):
        if self.count == 0:
            return True
        else:
            return False
        

    def update(self, item, priority):
        for x in self.heap:
            if x[1] == item:
                if x[0] <= priority:    
                    return None
                else:
                    x[0] = priority
                    return None
        
        self.push(item, priority)
                
        return


    def PQSort(self, nlist):
        for x in nlist:
            self.push(x, x)
        sortedList = []
        for y in range(len(nlist)):
            sortedList.append(self.pop())

        return sortedList



"""
q = PriorityQueue()

q.push("task1", 1)
q.push("task1", 2)
q.push("task0", 0)
t = q.pop()
print(t)
t = q.pop()
print(t)
t = q.pop()
print(t)



pq = PriorityQueue()
numlist = [5, 2, 6, 8, 14, 3, 21]
numlist2 = [5, 4, 15, 1, 48, 43, 68, 59, 72]
sortedL = q.PQSort(numlist)
sorted2 = pq.PQSort(numlist2)
print(sortedL)
print(sorted2)
"""

