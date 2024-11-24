
from pydantic import EmailStr
import os

# from typing import 
class EmailMessage:
    def __init__(self,subject,to,from_email ,body,html_body):
        self.subject=subject
        self.to:EmailStr=to
        self.from_email:EmailStr=from_email
        self.body:str=body
        self.html_body:str=html_body
   