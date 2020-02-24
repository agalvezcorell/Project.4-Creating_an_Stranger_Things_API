from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import src.recomendaciones as rec   
from flask import Flask, request
import src.mongoadd as mgadd
import src.mongoget as mgget
import json


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20000 per day", "5000 per hour"]
)
#Métodos POST para añadir info a la bd.

@app.route('/new/user',methods=['POST'])
def insertUser():
    nombre = request.form.getlist('name')
    mgadd.addUser(nombre)
    return "User insertado correctamente en la base de datos"


@app.route('/new/chat', methods=['POST'])
def insertChat():
    name = request.form.get('chat_name')
    participants = request.form.getlist('participants')
    mgadd.addChat(name,participants)
    return "Chat insertado correctamente en la base de datos"

@app.route('/new/message',methods=['POST'])
def insertMessage():
    user = request.form.get('name')
    chat = request.form.get('chat_name')
    message = request.form.get('message')
    mgadd.addMessage(user,chat,message)
    return "Mensaje insertado correctamente en la base de datos"

#Métodos GET para obtener info de la API.
#get usuario
@app.route('/users')
def getUsers():
    info = mgget.users()
    return json.dumps(info)

#get chats en los que está un user
@app.route('/user/chat/<name>')
def getChatsUser(name):
    info = mgget.chatUser(name)
    return json.dumps(info)

#get todos los grupos creados
@app.route('/chats')
def getChats(): 
    info = mgget.chats()
    return json.dumps(info)

#get usuarios de un grupo
@app.route('/chat/<name>')
def getUsersChat(name):
    info = mgget.usersChat(name)
    return json.dumps(info)


#get todos los mensajes de un user
@app.route('/user/message/<name>')
def getMessageUser(name):
    info = mgget.messagesUser(name)
    return json.dumps(info)

#get todos los mensajes de un chat
@app.route('/chat/message/<name>')
def getMessagesChat(name):
    info = mgget.messagesChat(name)
    return json.dumps(info)

# Get sentimientos de un chat
@app.route('/chat/sentiments/<name>')
def sentimentsChat(name):
    info = mgget.sentimientosChat(name)
    return json.dumps(info)


#get sentimientos de chat(separado por users)
@app.route('/chat/sentiments/users/<name>')
def sentimientosChatUsers(name):
    info = mgget.sentimientosChatUser(name)
    return json.dumps(info)


#get sentimientos de un usuario
@app.route('/user/sentiments/<name>')
def sentimentsUser(name):
    ran = "N"
    info = mgget.sentimientosUser(name,ran)
    return json.dumps(info)

#get sentimientos de un mensaje random de un usuario
@app.route('/user/random/sentiments/<name>')
def sentimentsRandom(name):
    ran = "Y"
    info = mgget.sentimientosUser(name,ran)
    return json.dumps(info)

# Get recomendaciones
@app.route('/recommend/<name>')
def recomendamosUser(name):
    info = rec.recomiendaUser(name)
    return json.dumps(info)

app.run("0.0.0.0", 5000, debug=True)
