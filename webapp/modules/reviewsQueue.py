class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class ReviewsQueue:
    def __init__(self, maxsize=None):
        self.head = None
        self.tail = None
        self.size = 0
        self.maxsize = maxsize
    
    def isEmpty(self): # Verifica se está vazia
        if self.head == None:
            return True
        return False

    def push(self, new_data): # Insere uma avaliação no começo da lista
        new_node = Node(new_data)

        self.size += 1

        if self.isEmpty():
            self.head = new_node
            self.tail = new_node

        else:
            new_node.next = self.head
            self.head = new_node
            
        if self.maxsize and self.size > self.maxsize:
            self.pop()

    def pushArray(self, array): # Insere várias avaliações no começo da lista
        for review in array:
            self.push(review)
    
    def print(self): # Imprime a lista de avaliações
        if self.isEmpty():
            print('Lista vazia!')
        
        else:
            temp = self.head

            while temp:
                print(temp.data, ' ', end='')
                temp = temp.next
            print()

    def returnArray(self): # Retorna uma lista das avaliações
        if self.isEmpty():
            print('Lista vazia!')

        else:
            temp = self.head
            array = []
            while temp:
                array.append(temp.data)
                temp = temp.next

            return array
    
    def pop(self): # Remove última avaliação da lista
        if self.isEmpty():
            print('Lista vazia!')
        
        else:
            self.size -= 1
            penult = self.head
            last = self.head

            while last.next:
                penult = last
                last = last.next
            
            penult.next = None
            self.tail = penult

    def deleteReview(self, key): # Remove a avaliação especificada no parâmetro "key"
        if self.isEmpty():
            print('Empty list')
        else:
            temp = self.head

            if temp is not None:
                if temp.data == key:
                    self.head = temp.next
                    temp = None
                    return
            
            while temp is not None:
                if temp.data == key:
                    break
                prev = temp
                temp = temp.next
            
            if temp == None:
                return

            prev.next = temp.next
            temp = None
    
    def clear(self): # Limpa a lista de avaliações
        if self.isEmpty():
            print('Lista vazia!')
        
        else:
            self.head = None