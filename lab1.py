from webapp.models import UsersCollection, MediaCollection, ReviewsCollection

from webapp.modules.Graph import Graph, Traveler, NodeGraph

allUsers = list(UsersCollection.find())

def main():
    menu = '''
    [1] - Exibir informações do viajante
    [2] - Exibir mapa
    [3] - Viajar para <posição no mapa>
    [4] - Voltar
    [5] - Fast travel
    [0] - Sair
    '''
    Nayahath = Traveler()
    Arcana = Graph()
    for user in allUsers:
        # Arcana.registerNode(user"username")
        for username in user["followers"]:
            # print(user["followers"])
            # print(user["username"], " followed by ",username)
            Arcana.connectByData(username, user["username"], force=True)
        for username in user["following"]:
            # print(user["following"])
            # print(user["username"], " following ",username)
            Arcana.connectByData(user["username"], username, force=True)
    # Graph.autofill(Arcana)
    print(Arcana)
    Nayahath.setPosition(Arcana.registeredNodes[0])
    
    
    while True:
        print(menu)
        userInput = input("Digite o código da ação: ")
        if userInput == '1':
            print(Nayahath)
        elif userInput == '2':
            Nayahath.showMap()
        elif userInput == '3':
            while True:
                try:
                    pos = int(input("Digite a posição do destino no mapa: "))
                    break
                except:
                    print("Posição deve ser um número inteiro")
            Nayahath.travelTo(pos)
        elif userInput == '4':
            print("Viajante rebobinando...")
            Nayahath.back()
        elif userInput == '5':
            newPosition = input("Digite a nova posição do viajante: ")
            newPosition = Arcana.getNodeByValue(newPosition)
            if newPosition:
                Nayahath.setPosition(newPosition)
            else:
                print("Destino não encontrado.")
                
        elif userInput == '0':
            break
        else:
            print("Opção inválida")
    
main()