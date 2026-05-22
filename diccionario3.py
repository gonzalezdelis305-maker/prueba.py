from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google import genai
import os
import json

app = FastAPI()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


preguntas = {
    "pregunta1": "hola",
    "pregunta2": "que dia es hoy",
    "pregunta3": "que es python"
}


@app.get("/")
def inicio():

    return {
        "mensaje": "API funcionando correctamente"
    }


@app.get("/preguntar")
def preguntar():

    try:

        resultado = {}

        
        for clave, valor in preguntas.items():

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=valor
            )

            resultado[clave] = {
                "pregunta": valor,
                "respuesta": response.text
            }

        
        return JSONResponse(
            content=json.loads(
                json.dumps(resultado, ensure_ascii=False)
            )
        )

    except Exception as e:

        return {
            "error": str(e)
        }
