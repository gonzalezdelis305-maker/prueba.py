from fastapi import FastAPI
from google import genai
import os

app = FastAPI()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}

@app.get("/preguntar")
def preguntar(texto: str):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=texto
        )

        return {
            "pregunta": texto,
            "respuesta": response.text
        }

    except Exception as e:
        return {
            "pregunta": texto,
            "respuesta": "el servicio está ocupado en este momento, intenta nuevamente en unos segundos.",
            "detalle": str(e)  
        }
