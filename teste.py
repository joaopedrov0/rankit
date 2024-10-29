from webapp.models import UsersCollection
import bcrypt

# simulando login 

temp = UsersCollection.find_one({"username": "seila"}) # pegando usuario do banco
print(temp)

res = bcrypt.checkpw('abacate'.encode('utf-8'), temp["password"]) # senha certa

print(res)

res = bcrypt.checkpw('mamão'.encode('utf-8'), temp["password"]) # senha errada

print(res)