# send Email using API


async def send_email(email_from,email_to:str,message,subject):
    return {"message":f"message sent {email_from}","status":1}