#!/usr/bin/python3


from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.dest]
        while node.node_id != self.source:
            prevNode = self.network.nodes[self.prev[node.node_id]]
            edge = self.findEdge(prevNode, node)
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = prevNode
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        if use_heap:
            self.heap(srcIndex)
        else:
            self.list(srcIndex)

        t2 = time.time()
        return (t2-t1)

    def heap(self, srcIndex):
        dist = []
        prev = []
        myDictionary = {}
        H = self.heapQueue()
        for node in self.network.nodes:
            dist.append(float('inf'))
            prev.append(None)
            myDictionary.update({node.node_id:float('inf')})
        dist[srcIndex] = 0
        myDictionary.update({srcIndex:0})

        # this is the "makeQueue in the pseudocode"
        H.makeheap(myDictionary)

        while not H.isEmpty():
            u = H.deletemin(myDictionary)
            uNode = self.network.nodes[u]

            for neighbor in uNode.neighbors:
                if (dist[neighbor.dest.node_id] > dist[neighbor.src.node_id] + neighbor.length):
                    dist[neighbor.dest.node_id] = dist[neighbor.src.node_id] + neighbor.length
                    prev[neighbor.dest.node_id] = neighbor.src.node_id
                    myDictionary.update({neighbor.dest.node_id:(dist[neighbor.src.node_id] + neighbor.length)})
                    H.decreaseKey(neighbor.dest.node_id, myDictionary)
        # dijkstras algorothim now complete
        self.prev = prev

        return

    def list(self, srcIndex):
        dist = []
        prev = []
        H = self.PriorityQueue()
        for node in self.network.nodes:
            dist.append(float('inf'))
            prev.append(None)
        dist[srcIndex] = 0

        # this is the "makeQueue in the pseudocode"
        for i in range(len(dist)):
            H.insert([i, dist[i]])

        while not H.isEmpty():
            u = H.delete()
            uIndex = u[0]
            uNode = self.network.nodes[uIndex]

            for neighbor in uNode.neighbors:
                if (dist[neighbor.dest.node_id] > dist[neighbor.src.node_id] + neighbor.length):
                    oldData = [neighbor.dest.node_id, dist[neighbor.dest.node_id]]
                    dist[neighbor.dest.node_id] = dist[neighbor.src.node_id] + neighbor.length
                    prev[neighbor.dest.node_id] = neighbor.src.node_id;
                    H.decreaseKey(oldData, [neighbor.dest.node_id, dist[neighbor.dest.node_id]])
        # dijkstras algorothim now complete
        self.prev = prev

        return


    # Given two nodes, this will return the edge between the two nodes
    def findEdge(self, node1, node2):
        for neighbor in node1.neighbors:
            if neighbor.dest.node_id == node2.node_id:
                return neighbor

    # Got the skeleton for this priority queue from online, I refitted it for my purposes
    # data is [index, distance] array tuple
    class PriorityQueue(object):
        def __init__(self):
            self.queue = []

        def __str__(self):
            return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty
        def isEmpty(self):
            return len(self.queue) == 0

        # for inserting an element in the queue
        def insert(self, data):
            self.queue.append(data)

        def decreaseKey(self, oldData, newData):
            index = self.queue.index(oldData)
            self.queue[index] = newData

        # for popping an element based on Priority
        def delete(self):
            try:
                max_val = 0
                for i in range(len(self.queue)):
                    if self.queue[i][1] < self.queue[max_val][1]:
                        max_val = i
                item = self.queue[max_val]
                del self.queue[max_val]
                return item
            except IndexError:
                print()
                exit()

    class heapQueue(object):
        def __init__(self):
            self.h = []

        def isEmpty(self):
            if len(self.h) == 0:
                return True
            else:
                return False

        def insert(self, node_id, dictionary):
            self.bubbleup(node_id, (len(self.h) + 1), dictionary)
            return
        def decreaseKey(self, node_id, dictionary):
            self.bubbleup(node_id, self.h.index(node_id), dictionary)
            return

        def deletemin(self, dictionary):
            if len(self.h) == 1:
                return None
            else:
                x = self.h[0]
                self.siftdown(self.h[len(self.h) - 1], 0, dictionary)
                return x

        def makeheap(self, dictionary):
            for node_id in dictionary:
                self.h.append(node_id)
            i = len(dictionary.keys()) - 1
            while i != 0:
                self.siftdown(self.h[i], i, dictionary)
                i = i - 1

            return
        def bubbleup(self, node_id, i, dictionary):
            p = math.ceil(i / 2)
            while (i != 1) and (dictionary[self.h[p]] > dictionary[node_id]):
                self.h[i] = self.h[p]
                i = p
                p = math.ceil(i / 2)
            self.h[i] = node_id
            return

        def siftdown(self, node_id, i, dictionary):
            c = self.minchild(i, dictionary)
            while (c != 0) and dictionary[self.h[c]] < dictionary[node_id]:
                self.h[i] = self.h[c]
                i = c
                c = self.minchild(i, dictionary)
            self.h[i] = node_id
            return

        def minchild(self, i, dictionary):
            if ((2 * i) + 1) > len(self.h):
                return 0
            elif (2 * i) == len(self.h) - 1:
                return self.h[(2 * i)]
            else:
                if (dictionary[self.h[(2 * i)]] > dictionary[self.h[((2 * i) + 1)]]):
                    return self.h[((2 * i) + 1)]
                else:
                    return self.h[(2 * i)]