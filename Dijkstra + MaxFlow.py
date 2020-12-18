infinity = 1000000
invalid_node = -1

class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False

class Dijkstra:
    def __init__(self):
        self.fileloaded = False
        self.startnode = 0
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []
        self.route_populated = False
        self.currentnode = 0

    def populate_network(self, filename):
        self.fileloaded = False
        try:
            txtfile = open(filename, "r")#default is read mode
        except IOError:
            print("txt file does not exist!")
            return
        for line in txtfile:
            self.network.append(list(map(int, line.strip().split(',')))) #it maps every element on the list, strip takes out non integer values
        
        self.fileloaded = True
        #just for printing purposes -------
        if not self.fileloaded:#temp
            print("Error: No file Has been loaded!")
            return
        for line in self.network:
            print(line, end = "")#debug
        #-------------
        self.network_populated = True
        txtfile.close()

    def parse_route(self, filename):
        '''load in route file'''
        self.route_populated = False
        try:
            txtfile = open(filename, "r")#default is read mode
        except IOError:
            print("txt file does not exist!")
            return
        self.route = txtfile.read()
        self.route = self.route.strip().split(">")
        self.startnode = ord(self.route[0]) - 65
        self.endnode = ord(self.route[1]) - 65
        self.currentnode = self.startnode
        self.route_populated = True
        txtfile.close()

    def populate_node_table(self):
        self.nodetable_populated = False
        for line in self.network:
            self.nodetable.append(Node())
        self.nodetable[self.startnode].distfromsource = 0
        self.nodetable[self.startnode].visited = True
        self.nodetable_populated = True

    def return_near_neighbour(self):
        '''determine nearest neighbours of current node'''#parses the network data structure and returns a list of the unvisited nearest neighbours of the current node.
        returnnearneighbour = []
        for index,line in enumerate(self.network):
            if (self.nodetable[index].visited == False and self.network[self.currentnode][index] > 0):
                returnnearneighbour.append(index)
        print("Return near neighbour: ",returnnearneighbour)#debug
        return returnnearneighbour

    def calculate_tentative(self):
        '''calculate tentative distances of nearest neighbours'''
        nearneighbour = self.return_near_neighbour()
        #we need to reset all the distfromsource to 0 not just startnode
        for index, line in enumerate(nearneighbour):
            print()#debug
            newdistance = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][nearneighbour[index]]
            if(newdistance < self.nodetable[nearneighbour[index]].distfromsource):
                self.nodetable[nearneighbour[index]].distfromsource = newdistance
                self.nodetable[nearneighbour[index]].previous = self.currentnode
                #debug
                print("Index: " ,nearneighbour[index], "Distance From Source: ", self.nodetable[nearneighbour[index]].distfromsource)

    def determine_next_node(self):
        '''determine next node to examine'''
        lowest = infinity
        lowest_index = invalid_node
        self.nodetable[self.currentnode].visited = True
        for index, line in enumerate(self.nodetable):#return the lowest value for that node
            value = self.nodetable[index].distfromsource
            if(value < lowest and self.nodetable[index].visited == False):
                lowest = value
                lowest_index = index
        self.currentnode = lowest_index
        print("Next Node: ", self.network[self.currentnode],chr(self.currentnode+65))#debug
      
    def calculate_shortest_path(self):
        '''calculate shortest path across network'''
        while self.currentnode != self.endnode:
            self.calculate_tentative()
            self.determine_next_node()

    def return_shortest_path(self):
        '''return shortest path as list (start->end), and total distance'''
        path = []
        while self.currentnode != self.startnode:
            path.insert(0, chr(self.currentnode+65))
            self.currentnode = self.nodetable[self.currentnode].previous
        path.insert(0,chr(self.startnode+65))
        print("Total Distance: ", self.nodetable[self.endnode].distfromsource)#debug
        return path

class MaxFlow(Dijkstra): 
 '''inherits from Dijkstra class. 
Expose and override Dijkstra methods and add new ones where required, but must use original Dijkstra’s algorithm as part of the calculation'''


if __name__ == '__main__':
    test = Dijkstra()
    test.populate_network("network.txt")
    test.parse_route("route.txt")
    test.populate_node_table()
    test.calculate_shortest_path()
    print(test.return_shortest_path())