# from webapp.models import Database

# print(Database.getFollowSuggestions("rainankaneka", "mastergamerjp"))



from webapp.modules import ReviewsQueue

q = ReviewsQueue()

q.push('abacate')
q.push('maçã')
q.push('pera')
q.push('melancia')
q.push('morango')
q.push('melão')

q.print()

q.pop()

q.print()