import json
import socketio
from typing  import List
from ..core.security import get_current_user
from socketio.exceptions import ConnectionRefusedError
sio = socketio.AsyncServer(async_mode='asgi',cors_allowed_origin=[])
socket_app=socketio.ASGIApp(socketio_server=sio,)

online:List[dict[str,str|int]]=[]
group_chat=[]


def add_new_user(data,service:list[dict|str]=online):
    service.append(data)
    


@sio.on("connect")
async def connect(sid, env,auth):  
    if  env.get("HTTP_AUTH") is None:
        raise ConnectionRefusedError('authentication failed')     
    user =await get_current_user(env.get("HTTP_AUTH"),socket=True)    
    add_new_user({user["email"]:sid})
    print(len(online))

@sio.on("group")
async def group_message(sid,env):
    pass; 
    
    
@sio.on("DM")
async def direct_message(sid,data):
    await sio.emit('DM', data,skip_sid=sid)
    return "ok"

   
@sio.on("disconnect")
async def disconnect(sid):
    for user in online:
        if user.values():
            online.remove(user)
    print(online)            
    print("Client Disconnected: "+" "+str(sid))