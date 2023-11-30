from typing import Optional
from pydantic import BaseModel
from enum import Enum

class eventTypeEnum(Enum):
    email_open = 'email_open'
    email_click = 'email_click'
    email_unsubscribe = 'email_unsubscribe'
    purchase = 'purchase'


class EventInput(BaseModel):
    customer_id: int 
    event_type: eventTypeEnum 
    timestamp: str  
    email_id: int
    clicked_link: Optional[str]= None
    product_id: Optional[int] = None
    amount: Optional[float] = None
    
    class Config:  
        use_enum_values = True 
    