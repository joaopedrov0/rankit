class NodeGraph:
    def __init__(self, data):
        self.data = data
        self.connections = []
        
    def __str__(self):
        temp = ''
        for connection in self.connections:
            currentTuple = list(connection.items())[0]
            temp += "Nó: {} | Peso: {}\n".format(currentTuple[0].data, currentTuple[1])
        if len(self.connections) == 0:
            temp = "Sem conexões"
        return '''
    Informações do nó
    
    # Dado
    {}
    
    # Conexões
    {}
    '''.format(self.data, temp)
    
    
    def getConnectionNodes(self):
        temp = []
        for connection in self.connections:
            currentTuple = list(connection.items())[0]
            temp.append(currentTuple[0])
        return temp
    
    def getConnectionNodesDict(self):
        temp = []
        for connection in self.connections:
            currentTuple = list(connection.items())[0]
            temp.append({"node":currentTuple[0], "data":currentTuple[0].data})
        return temp
    
    def isConnectedTo(self, node):
        res = False
        for connection in self.connections:
            if list(connection.keys())[0] == node:
                res = True
        return res