from contextlib import asynccontextmanager
from typing import Annotated, List

import numpy as np
from app.schemas import EventInput
from fastapi import FastAPI, Query, Response, Body
from datetime import date
import pandas as pd

file = './persist_data.csv'
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create csv file for persist data
    with open(file,'w') as f:
        f.write('customer_id,event_type,timestamp,email_id,clicked_link,product_id,amount \n')
    yield

app = FastAPI(lifespan= lifespan)

@app.get('/', response_model=str)
def get_home():
    return "Hello World"



@app.post("/event-subscription/hook", response_model=str)
async def new_event( data:  Annotated[EventInput, Body(embed=True)]):
    new_line = ','.join(str(val) for val in data.model_dump().values())
    with open(file, 'a+') as f:
        f.write(new_line + '\n')
    return  Response(content= 'Data persist successfully')

@app.get('/all_events/{customer_id}', response_model= List[EventInput])
async def get_all_event_by_customer(
    customer_id: int,
    start_date: date = Query(None),
    end_data: date = Query(None)
):
    data_csv = pd.read_csv(file)
    data_csv.replace(np.nan,None,  inplace=True)

    data_customer = data_csv.loc[data_csv['customer_id']== customer_id ]
    response_data = [EventInput(**record) for record in data_customer.to_dict(orient='records')]
    return response_data