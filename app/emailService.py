from typing import List
from pydantic import EmailStr
from.core.config import Settings
import  resend
import os
from .schemas.schemas import EmailMessage

        
        
        
class EmailService():
    def __init__(self,api_key:str=Settings.RESEND_API_KEY,fail_silently=False):
        self.client=resend
        self.client_api=api_key       
        self.fail_silently=fail_silently    
       
    
    async def send_messages(self,email_messages:List[EmailMessage]):
        num_sent=0
        for message in email_messages:
            # Create Resend email data
            email_data = {
                "from": message.from_email,
                "to": message.to,
                "subject":message.subject,
                "text": message.body,
                "html": message.html_body,
                # Add any other Resend-specific options here
            }
            try:              
                # Send the email using Resend
                response = await self.client.Emails.send(email_data)

                print(response)
                num_sent += 1
              
                    
            except Exception as e:
                if self.fail_silently:
                    pass
                else:
                    raise e

        return num_sent
            
    async def send_message(self,message:EmailMessage):
        
        # Create Resend email data
        email_data = {
            "from": message.from_email,"to": message.to,"subject":message.subject,"text": message.body,"html": message.html_body
            # Add any other Resend-specific options here
        }
        try:              
            # Send the email using Resend
            response =  self.client.Emails.send(email_data)
        except Exception as e:
            if self.fail_silently:
                pass
            else:
                raise e

        return 
        
            
            
            
