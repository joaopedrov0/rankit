
# Tutorial:
# quick = QuickSort(<lista>, <1 pra crescente e -1 pra descrescente>, <chave do dicionario se for um array de dicionarios>)

class QuickSort:
    def __init__(self, arr, method=1, key=None):
        """
        method 1 = crescente
        method -1 = descrescente
        """
        self.swapcount = 0
        self.unsorted = arr
        self.method = method
        self.sorted = self.sort(arr, True, 0, key)

    def __str__(self):
        return '''
        Unsorted: {}
        Method: {}
        Sorted: {}
        '''.format(self.unsorted, self.method, self.sorted)

    def sort(self, arr, first=True, counter=0, key=None):
        counter += 1
        pivot = arr[self.getPivotIndex(arr)]
        aux = self.sortByPivot(arr, pivot, key)
        before = aux[0]
        if len(before) > 1:
            before = self.sort(before, False, counter, key)
        after = aux[2]
        if len(after) > 1:
            after = self.sort(after, False, counter, key)
        res = [*before, pivot, *after]

        if first:
            print("QuickSort | SwapCount: {}".format(self.swapcount))

        return res


    def getPivotIndex(self, arr):
        """Encontra o índice do pivô de uma lista qualquer"""
        
        if len(arr) == 1: return 0
        
        res = (len(arr)-1) // 2

        return res

    def sortByPivot(self, arr, pivot, key):
        """Devolve duas listas que separam o que é maior e menor que o pivô"""
        before = []
        after = []
        passedPivot = False
        for elem in arr:
            if not passedPivot and elem == pivot: 
                passedPivot = True
                continue 
            if self.checkBefore(elem, pivot, key):
                self.swapcount += 1
                before.append(elem)
            else:
                self.swapcount += 1
                after.append(elem)

        return [before, pivot, after]

    def checkBefore(self, elem1, elem2, key):
        """Verifica se o elemento 1 vem antes do elemento 2"""
        if key == None:
            if elem1 == elem2: return True

            if elem1 < elem2 and self.method == 1: return True

            if elem1 > elem2 and self.method == -1: return True

            return False
        else:
            if elem1[key] == elem2[key]: return True

            if elem1[key] < elem2[key] and self.method == 1: return True

            if elem1[key] > elem2[key] and self.method == -1: return True

            return False





# pega a lista

# acha o pivo

# divide em duas listas

# verifica se o tamanho de uma lista é maior que um e repete o processo se for