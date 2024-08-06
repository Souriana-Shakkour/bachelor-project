!pip install numpy
!pip install time
!pip install tqdm

from google.colab import drive
drive.mount('/content/drive/')

import numpy as np
from tqdm.notebook import tqdm
import time

class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        
    def insertAtEnd(self, data):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
            return
        currentNode = self.head
        while(currentNode.next):
            currentNode = currentNode.next
        currentNode.next = newNode

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [LinkedList() for column in range(vertices)]

    def minDistance(self, dist, sptSet):
        print(self.V)
        min = float('inf')
        print(self.V)
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                minIndex = v
        return minIndex

    def dijkstra(self, src):
        dist = [float('inf')] * self.V
        if len(dist) != 0:
            dist[src] = 0
        sptSet = [False] * self.V
        for count in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True
            v = self.graph[u].head
            while v != None:
                dis = v.data[1]
                neighbour = v.data[0]
                if (sptSet[neighbour] == False and       # not visited
				dist[neighbour] > dist[u] + int(dis)):   #shorter path found
                    dist[neighbour] = dist[u] + int(dis)
                v = v.next

def csvToLinkedList (fileName):
    arr = np.loadtxt("/content/drive/Shareddrives/dijkstra_bp/final/"+fileName, delimiter=",", dtype=str)
    arrint = [LinkedList() for column in range(len(arr))]
    rowIndex = 0
    for rowIn in tqdm(range(0,len(arr)), leave = True, desc="creating graph", ascii=True, ncols=75, dynamic_ncols=True):
        columnIndex = 0
        row = arr[rowIn]
        for column in row:
            if (float(arr[rowIndex][columnIndex]) != 0):
                arrint[rowIndex].insertAtEnd((columnIndex, float(arr[rowIndex][columnIndex])))
            columnIndex += 1
        rowIndex += 1
        columnIndex = 0
    return arrint

def saveRunningTime (csv):
    g = Graph(0)
    g.graph = csvToLinkedList(csv)
    g.V = len(g.graph)
    t0 = time.perf_counter()
    g.dijkstra(0)
    t1 = time.perf_counter()
    total = t1-t0
    file = open("/content/drive/Shareddrives/dijkstra_bp/final/time.txt","a")
    file.write(str(csv) + " time for linked list is: " + str(total) + '\n')
    file.close()

def runForGraphs (numGraphs, numVertices):
    for i in tqdm (range (1, numGraphs+ 1),
                  desc="Loading…",
                  ascii=False):
      saveRunningTime(str(numVertices) + "." + str(i) + ".csv")
      
runForGraphs (16, 2500)
runForGraphs (21, 5000)
runForGraphs (26, 10000)

print ("Done")
