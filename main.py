from fastapi import FastAPI

app = FastAPI()


@app.get('/', response_model=str)
def get_home():
    return "Hello World"