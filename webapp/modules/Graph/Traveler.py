from .NodeGraph import NodeGraph

class Traveler:
    def __init__(self, currentNode=None):
        self.currentPosition = currentNode if currentNode else None
        self.path = []
        self.map = []
        self.travelTotalCost = 0
        self.travelCosts = []
        
    def __str__(self):
        
        path = ''
        for p in self.path:
            path += "{} - ".format(p.data)
        path = path if path else "Empty"
        
        return '''
    Traveler Description
    
    # Current position
    {}
    
    # Path
    {}
    
    # Costs
    - List of costs: {}
    - Total cost: {}
    '''.format(self.currentPosition.data if self.currentPosition else "Undefined", path, self.travelCosts, self.travelTotalCost)
    
    def setPosition(self, node):
        if not isinstance(node, NodeGraph):
            print("Node must be a NodeGraph instance.")
            return
        self.currentPosition = node
        self.path = [node]
        self.map = [*node.connections]
        self.travelTotalCost = 0
        self.travelCosts = []
        
    def showMap(self):
        temp = ''
        for connection in self.map:
            currentTuple = list(connection.items())[0]
            temp += "Posição: {} | Nó: {} | Peso: {}\n".format(self.map.index(connection), currentTuple[0].data, currentTuple[1])
        if len(self.map) == 0:
            temp = "Sem conexões"
        print(temp)
        return
    
    def getMapNodeOnly(self):
        temp = []
        for connection in self.map:
            currentTuple = list(connection.items())[0]
            temp.append(currentTuple[0])
        return temp
    
    def travelTo(self, direction):
        if direction >= 0 and direction < len(self.map):
            travel = list(self.map[direction].items())[0]
            target = travel[0]
            cost = travel[1]
            
            self.currentPosition = target
            self.path.append(target)
            self.travelTotalCost += cost
            self.travelCosts.append(cost)
            self.map = [*target.connections]
            
    def back(self):
        if len(self.path) == 1:
            return True # Fim da jornada
        self.path.pop()
        self.currentPosition = self.path[len(self.path) - 1]
        self.travelCosts.pop()
        self.travelTotalCost = sum(self.travelCosts)
        self.map = [*self.currentPosition.connections]
        return False # Não acabou
        
    def getPosition(self):
        return self.currentPosition
    
    def getPathValueList(self):
        temp = []
        for path in self.path:
            temp.append(path.data)
        return temp