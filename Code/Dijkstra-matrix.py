#The following code reads the graphs generated previously and stored in csv files, converts them to matrices, runs Dijkstra's algorithm on them and saves the running time in a txt file.
#The lines 14-38 come from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
#The code is created to run on Google Colab, it would require some adjustments to run locally.

!pip install numpy
!pip install time
!pip install tqdm

from google.colab import drive
drive.mount('/content/drive/')

import numpy as np
import time
import concurrent.futures
import os
import tqdm

class Graph():
  def __init__(self, vertices):
    self.V = vertices
    self.graph = [[0 for column in range(vertices)]
                     for row in range(vertices)]
        
  def minDistance(self, dist, sptSet):
    min = float('inf')
    for v in range(self.V):
      if dist[v] < min and sptSet[v] == False:
        min = dist[v]
        minIndex = v
    return minIndex
    
  def dijkstra(self, src):
      dist = [float('inf')] * self.V
      dist[src] = 0
      sptSet = [False] * self.V
      for cout in range(self.V):
        u = self.minDistance(dist, sptSet)
        sptSet[u] = True
        for v in range(self.V):
          if (self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]):
            dist[v] = dist[u] + self.graph[u][v]

def readChunk(filename, start, end):
  with open("/content/drive/Shareddrives/dijkstra_bp/final/"+filename, 'r') as f:
    if start > 0:
      f.seek(start)
      f.readline()
    lines = []
    currentPos = f.tell()
    while end is None or currentPos < end:
      line = f.readline()
      if not line:
        break
      lines.append(line)
      currentPos = f.tell()
  return ''.join(lines)

def convertChunk(data):
  from io import StringIO
  return np.genfromtxt(StringIO(data), delimiter=",", dtype=float)

def loadAndConvert(fileName):
  fileSize = os.path.getsize("/content/drive/Shareddrives/dijkstra_bp/final/"+fileName)
  numThreads = 4
  chunkSize = fileSize // numThreads-1
  with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
    readFutures = []
    for i in range(numThreads):
      start = i * chunkSize
      end = (i + 1) * chunkSize if i < numThreads - 1 else None
      readFutures.append((i, executor.submit(readChunk, fileName, start, end)))
    chunks = [None] * numThreads
    for i, future in tqdm.tqdm(readFutures, total=numThreads, desc="Reading Chunks"):
      chunks[i] = future.result()
    processFutures = [executor.submit(convertChunk, chunk) for chunk in chunks]
    arrays = [None] * numThreads
    for i, future in enumerate(processFutures):
      arrays[i] = future.result()
  combinedArray = np.vstack(arrays)
  return combinedArray.tolist()

def saveRunningTime (csv):
  g = Graph(0)
  g.graph = loadAndConvert(csv)
  g.V = len(g.graph)
  t0 = time.perf_counter()
  g.dijkstra(0)
  t1 = time.perf_counter()
  total = t1-t0
  file = open("/content/drive/Shareddrives/dijkstra_bp/final/mx_time.txt","a")
  file.write(str(csv) + " time for matrix is: " + str(total) + '\n')
  file.close()

def runForGraphs (numGraphs, numVertices):
  for i in range (1, numGraphs + 1):
    saveRunningTime(str(numVertices) + "." + str(i) + ".csv")

runForGraphs (16, 2500)
runForGraphs (21, 5000)
runForGraphs (26, 10000)

print ("Done")
