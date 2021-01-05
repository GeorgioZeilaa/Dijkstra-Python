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
        print("The Network:")
        for line in self.network:
            print(line, end = "")#debug
        #----------------------------------
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
        self.route = []
        self.route = txtfile.read()
        self.route = self.route.strip().split(">")
        self.startnode = ord(self.route[0]) - 65
        self.endnode = ord(self.route[1]) - 65
        self.currentnode = self.startnode
        self.route_populated = True
        txtfile.close()

    def populate_node_table(self):
        self.nodetable_populated = False
        for _ in self.network:
            self.nodetable.append(Node())
        self.nodetable[self.startnode].distfromsource = 0
        self.nodetable[self.startnode].visited = True
        self.nodetable_populated = True

    def return_near_neighbour(self):
        '''determine nearest neighbours of current node'''#parses the network data structure and returns a list of the unvisited nearest neighbours of the current node.
        returnnearneighbour = []
        for index,_ in enumerate(self.network):
            if (self.nodetable[index].visited == False and self.network[self.currentnode][index] > 0):#checks if the node has not been visited and if the currentnode has a neighbour
                returnnearneighbour.append(index)#add the index values which are the neighbours to the list returnnearneighbour
        if returnnearneighbour == []:#for console spam puposes if it is returning empty lists
            return returnnearneighbour
        print("\nCurrent Near Neighbours Found: ",returnnearneighbour)
        return returnnearneighbour

    def calculate_tentative(self):
        '''calculate tentative distances of nearest neighbours'''
        nearneighbour = self.return_near_neighbour()#to store the list of the near neighbours of the currentnode
        for index, _ in enumerate(nearneighbour):
            newdistance = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][nearneighbour[index]]#adds the neighbour and currentnode distances
            if(newdistance < self.nodetable[nearneighbour[index]].distfromsource):#checks if the currentnode and neighbour node distances is less than distance from source of the neighbour
                self.nodetable[nearneighbour[index]].distfromsource = newdistance#sets the new distance to the neighbour's distance
                self.nodetable[nearneighbour[index]].previous = self.currentnode#sets the currentnode to the previous node of the neighbour that was chosen
                print("\nIndex: " ,nearneighbour[index], " Distance From Source: ", self.nodetable[nearneighbour[index]].distfromsource,"\n")
        print("------------------------------------")

    def determine_next_node(self):
        '''determine next node to examine'''
        lowest = infinity
        lowest_index = invalid_node
        self.nodetable[self.currentnode].visited = True#sets the current node's visited to true so that we do not revisit that node
        for index, _ in enumerate(self.nodetable):#return the lowest value for that node
            value = self.nodetable[index].distfromsource
            if(value < lowest and self.nodetable[index].visited == False):#retrieves the lowest distance from source
                lowest = value
                lowest_index = index
        if lowest_index != -1:#if the lowest distance from source is not found
            self.currentnode = lowest_index#sets the correct index of the current node to be examined which is the lowest cost
            print("Next Node:", chr(self.currentnode+65), " Index:", self.currentnode, self.network[self.currentnode])#debug
        else:
            print("ERROR: No paths found!")
            return False

    def calculate_shortest_path(self):
        '''calculate shortest path across network'''
        while self.currentnode != self.endnode:#as long as the currentnode is not equal to endnode this means we did not find the path
            self.calculate_tentative()
            if self.determine_next_node() == False:
                return False

    def return_shortest_path(self):
        '''return shortest path as list (start->end), and total distance'''
        path = []#to temperaty store the path that was found
        while self.currentnode != self.startnode:#we reverse the path that was found by using .previous and when the currentnode goes back to startnode we end the loop
            path.insert(0, chr(self.currentnode+65))#adds to the path list the letter that we found
            self.currentnode = self.nodetable[self.currentnode].previous#retrieves the previous node and sets that to be the currentnode
        path.insert(0,chr(self.startnode+65))#to add the start node at the beginning of the path list
        print("\nTotal Distance: ", self.nodetable[self.endnode].distfromsource)
        return path

class MaxFlow(Dijkstra):
 #'''inherits from Dijkstra class. Expose and override Dijkstra methods and add new ones where required, but must use original Dijkstra’s algorithm as part of the calculation'''
    def __init__(self):
        Dijkstra.__init__(self)
        self.max_flow = 0#total bottlenecks
        self.pathsavailable = []#paths for maxflow
        self.paths = []#paths found in return shortest path
        self.bottleneck = []

    def return_shortest_path(self):
        '''return shortest path as list (start->end), and total distance'''
        self.paths = []#to store the paths found
        if self.calculate_shortest_path() == False:
            return
        while self.currentnode != self.startnode:#we inverse the way back to start to find the path that was taken
            self.paths.insert(0, chr(self.currentnode+65))#insert the currentnode into paths array by converting it to a letter
            self.currentnode = self.nodetable[self.currentnode].previous#going to the previous node whichever it was using the nodetable
        self.paths.insert(0,chr(self.startnode+65))#to include the start node in the paths array
        return self.paths

    def reset(self):#we copy some parts of the nodetable to reset the values
        for index, _ in enumerate(self.nodetable):#loops through the nodetable and resets all nodes back to start to be able to run dijkstra again
            self.nodetable[index].visited = False
            self.nodetable[index].distfromsource = infinity
            self.nodetable[index].previous = invalid_node
        self.nodetable[self.startnode].visited = True
        self.currentnode = self.startnode
        self.nodetable[self.currentnode].distfromsource = 0
        self.paths.clear()#makes sure that previous path that was found is cleared so the new one can be added

    def return_bottleneck(self):
        lowest = infinity#used to calculate the minimum value in the path
        bottleneck = [0,0]#stores bottleneck values
        self.pathsavailable.append(self.paths)
        #self.paths = self.paths[:-1]
        for index, _ in enumerate(self.paths):#loop the paths that return shortest path has found
            if index == len(self.paths)-1:#makes sure that no error occurs when trying to access out of range value
                return bottleneck
            edges = self.network[ord(self.paths[index])-65][ord(self.paths[index+1])-65]#to recieve the cost of the current node to the next one
            #print("MINIMUM: ",min(lowest, edges)) CHANGE
            if edges >= 0 and edges < lowest:#check if the nodes have the capacity and finds the minimum capacity of each path
                lowest = edges#sets the lowest value so the next comparison in the if statement can be compared with the lowest value found previously
                bottleneck[0] = ord(self.paths[index])-65
                bottleneck[1] = ord(self.paths[index+1])-65
        return bottleneck#returns the index value of the bottleneck which is the min in the path

    def bottleneck_remove(self):
        remove = self.network[self.return_bottleneck()[0]][self.return_bottleneck()[1]]
        for index, _ in enumerate(self.paths):
            if index == len(self.paths)-1:#so no out of range error occurs
                break
            self.network[ord(self.paths[index])-65][ord(self.paths[index+1])-65] -= remove#this removes the bottleneck cost from the original capacity
        self.bottleneck.append(remove)#makes a record of the bottleneck
        self.max_flow += remove#adds the bottleneck to a the max_flow variable
    def return_maxflow(self):
        return self.max_flow

    def calculate_paths(self):
        for index, _ in enumerate(self.nodetable):
            self.reset()#resets so dijkstra can run again
            self.return_shortest_path()#recieve the next path
            self.bottleneck_remove()#loops through the path that was found previously and finds the minimum cost in that path and subtracts it from the available capacities
            self.pathsavailable[index] = self.paths.copy()#to keep a record of every path that was found because we need to clear paths to find the next available one
        pathsavailablewithoutempty= [x for x in self.pathsavailable if x != []]#to remove the empty spaces that dijkstra tried to add
        bottleneckswithoutempty = [x for x in self.bottleneck if x != 0]
        print("\nBottleNecks:", bottleneckswithoutempty)
        print("Paths MaxFlow:", pathsavailablewithoutempty)

if __name__ == '__main__':
    print("-------Dijkstra-------")
    djkstra = Dijkstra()
    djkstra.populate_network("network.txt")
    djkstra.parse_route("route.txt")
    djkstra.populate_node_table()
    djkstra.calculate_shortest_path()
    print(djkstra.return_shortest_path())
    
    print("-------MaxFlow-------")
    maxflow = MaxFlow()
    maxflow.populate_network("network.txt")
    maxflow.parse_route("route.txt")
    maxflow.populate_node_table()
    maxflow.calculate_paths()
    print("MaxFlow: ",maxflow.return_maxflow())
