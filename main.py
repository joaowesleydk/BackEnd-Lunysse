from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import os
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import get_db
 
load_dotenv()
app = FastAPI(
    title=os.getenv("APP_NAME"),
    version=os.getenv("APP_VERSION"),
)
@app.get("/")
def read_root():
    return{"message": "Bem-Vindo a API LYRA"}
 
@app.get("/test-db")
def test_database_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("Select 1 "))
        return {"Status": "sucess", "message": "conexao com banco de dados ok"}
    except Exception as error:
        return{"Status": "error", "message": f"Falha na conexao: {error}"}
   
 