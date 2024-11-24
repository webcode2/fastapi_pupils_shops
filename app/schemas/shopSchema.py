from pydantic import BaseModel, Field



class PupSchema(BaseModel):
    text:str=Field()    
    breed_id:int=Field()


    
class ShopSchema(BaseModel):
    name: str 
    location: str
    state: str
    street_name:str
    house_number:str
    Business_reg_no: str
   
