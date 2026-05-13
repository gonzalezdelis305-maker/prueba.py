from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from icmplib import ping
from typing import List

app = FastAPI()

# =========================
# 📥 INPUT
# =========================
@strawberry.input
class HostInput:
    host: str


@strawberry.input
class MultiHostInput:
    hosts: List[str]


# =========================
# 📤 OUTPUT
# =========================
@strawberry.type
class ResultadoRed:
    comando: str
    salida: str


# =========================
# ⚠ CONTROL GENERAL DE ERRORES
# =========================
def manejar_error(error):

    mensaje = str(error)

    if "not known" in mensaje:

        return "Error: dirección o dominio no encontrado"

    elif "unreachable" in mensaje:

        return "Error: host no alcanzable"

    else:

        return f"Error inesperado: {mensaje}"


# =========================
# 🌐 QUERY
# =========================
@strawberry.type
class Query:

    # -------------------------
    # 📡 PING
    # -------------------------
    @strawberry.field
    def ping(self, datos: HostInput) -> ResultadoRed:

        try:

            resultado = ping(datos.host, count=4)

            salida = (
                f"Host: {datos.host}\n"
                f"IP: {resultado.address}\n"
                f"Paquetes enviados: {resultado.packets_sent}\n"
                f"Paquetes recibidos: {resultado.packets_received}\n"
                f"Pérdida: {resultado.packet_loss * 100}%\n"
                f"Tiempo promedio: {resultado.avg_rtt} ms"
            )

            return ResultadoRed(
                comando=f"ping {datos.host}",
                salida=salida
            )

        except Exception as e:

            return ResultadoRed(
                comando=f"ping {datos.host}",
                salida=manejar_error(e)
            )

    # -------------------------
    # 📡 MULTIPING
    # -------------------------
    @strawberry.field
    def multiping(self, datos: MultiHostInput) -> ResultadoRed:

        try:

            salida_total = ""

            for direccion in datos.hosts:

                resultado = ping(direccion, count=2)

                salida_total += (
                    f"\n===== {direccion} =====\n"
                    f"IP: {resultado.address}\n"
                    f"Paquetes enviados: {resultado.packets_sent}\n"
                    f"Paquetes recibidos: {resultado.packets_received}\n"
                    f"Pérdida: {resultado.packet_loss * 100}%\n"
                    f"Tiempo promedio: {resultado.avg_rtt} ms\n"
                )

            return ResultadoRed(
                comando="multiping",
                salida=salida_total
            )

        except Exception as e:

            return ResultadoRed(
                comando="multiping",
                salida=manejar_error(e)
            )

    # -------------------------
    # 🛰 TRACEROUTE SIMULADO
    # -------------------------
    @strawberry.field
    def traceroute(self, datos: HostInput) -> ResultadoRed:

        try:

            resultado = ping(datos.host, count=4)

            salida = (
                f"Ruta simulada hacia: {datos.host}\n"
                f"IP destino: {resultado.address}\n"
                f"Paquetes enviados: {resultado.packets_sent}\n"
                f"Paquetes recibidos: {resultado.packets_received}\n"
                f"Pérdida: {resultado.packet_loss * 100}%\n"
                f"Tiempo promedio: {resultado.avg_rtt} ms"
            )

            return ResultadoRed(
                comando=f"traceroute {datos.host}",
                salida=salida
            )

        except Exception as e:

            return ResultadoRed(
                comando=f"traceroute {datos.host}",
                salida=manejar_error(e)
            )


# =========================
# 🚀 GRAPHQL
# =========================
schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
