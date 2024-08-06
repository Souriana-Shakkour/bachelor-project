import numpy 
import random
import winsound

def arrayToCSV (array, csv):
    numpy.savetxt(csv, array, delimiter=',', newline= '\n')
    
def generateLinearGraphCSV (csv, size):
    e = [[0 for i in range(size)]
         for j in range (size)]
    for i in range(size):
         for j in range (size):
             if i == j-1:
                 e[i][j] = random.randint(1, 10)
    arrayToCSV(e, csv)
      
def csvToMatrix (fileName):
    arr = numpy.loadtxt(fileName, delimiter=",", dtype=str)
    arrint = [[None for column in range(len(arr))]
                for row in range(len(arr))]
    rowIndex = 0
    for row in arr:
        columnIndex = 0
        for column in row:
            arrint[rowIndex][columnIndex] = float(arr[rowIndex][columnIndex])
            columnIndex += 1
        rowIndex += 1
    return arrint
    
def densifyCSV (oldCSV, newCSV ,numVertices, numNewEdges):
    if numNewEdges == 0:
        return
    e = csvToMatrix(oldCSV)
    numAddedEdges = 0
    for row in range (len(e)):
        for column in range (len(e[row])):
            if (e[row][column] == 0 ):
                e[row][column] = random.randint(1, 10)
                numAddedEdges += 1
                if numAddedEdges == numNewEdges:
                    arrayToCSV(e, newCSV)
                    return
    arrayToCSV(e, newCSV)

def createGraph (size, numGraphs, alaramOn):
    fileName = str(size) + ".1.csv"
    numEdgesToAdd = ((size * (size - 1) ) - (size - 1) )
    numNewEdgesPerGraph = numEdgesToAdd // (numGraphs - 1)
    generateLinearGraphCSV(fileName, size)
    for graphCount in range(1, numGraphs + 1):
        newFileName = str(size) + "." + str(graphCount+1) + ".csv"
        densifyCSV(fileName, newFileName, size, numNewEdgesPerGraph)
        fileName = newFileName
    if (numEdgesToAdd % numGraphs) != 0:
        densifyCSV(fileName, newFileName, size, numEdgesToAdd % numGraphs)
    if alaramOn == "Y" or alaramOn == "y":
        frequency = 2500
        duration = 1200
        winsound.Beep(frequency, duration)

createGraph(2500, 15, "y")
createGraph(5000, 20, "y")
createGraph(10000, 25, "y")

print ("Done")
