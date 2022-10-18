#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        if use_heap:
            self.heap(srcIndex)
        else:
            self.list(srcIndex)

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)


        t2 = time.time()
        return (t2-t1)

    def heap(self, srcIndex):
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

        return

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

