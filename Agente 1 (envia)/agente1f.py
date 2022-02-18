import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import psutil
import os
from os import walk
from requests import get
from contenidomensaje import Contenido

ip = get('https://api.ipify.org').text
separador = "---END---"



#Se debe crear en el agente que envia, una carpeta que se llame compartir.
#Dentro de ella se ubican los archivos que se podran mostrar

#Se obtiene la ruta raiz mas el sufijo de la carpeta compartir
directory = os.getcwd() + "/compartir"
#Creamos una variable files para guardar los nombres de los archivos dentro.
files = ""
#Obtenemos los nombres de los archivos usando la libreria walk
filenames = next(walk(directory), (None, None, []))[2]
#Convertimos el array de nombres en un string para poder compartirlo.
for element in filenames:
	files = files + element +","

#Creamos una variable cpu_us, que obtiene el uso del cpu
#haciendo uso de la libreria psutil.
cpu_us = psutil.cpu_percent(interval=1)
if cpu_us <= 40.0:
	conten = Contenido()
else:
	conten = ""

#Definimos la clase para el agente que envía los datos.
class SenderAgent(Agent):
	class InformBehav(OneShotBehaviour):
		async def run(self):
			

			#Message contain:


			print("InformBehav en proceso")
			msg = Message(to="mccagente2@trashserver.net")     # Se crea el mensaje hacia el destinatario
			msg.set_metadata("performative", "inform")  
			msg.set_metadata("ontology", "myOntology")  # Se selecciona la ontologia usada
			msg.set_metadata("language", "OWL-S")       # Se selecciona el lenguaje usado
			msg.body = "1RUTA: "+directory+", 2ARCHIVOS: "+files+" 3IP: "+ip+", 4CPU: "+str(cpu_us)+", 5STATUS: "+conten+separador # Creamos el cuerpo del mensaje
			await self.send(msg)
			print("Mensaje enviado!")
			# Configuramos el mensaje de finalizacion
			self.exit_code = "Proceso finalizado!"
			# Terminamos el agente
			await self.agent.stop()
	async def setup(self):
		print("Agente inicializado")
		#print(f'IP publica: {ip}')
		self.b = self.InformBehav()
		self.add_behaviour(self.b)
agent = SenderAgent("mccagente1@trashserver.net", "12345678")
future = agent.start()
future.result()
while agent.is_alive():
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print("Se presiono una tecla")
		agent.stop()
		break
print("El agente finalizo con el siguiente codigo: {}".format(agent.b.exit_code))
