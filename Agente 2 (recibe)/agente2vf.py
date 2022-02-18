import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime
import os


t_out = 10
msg_contain =""
class ReceiverAgent(Agent):
	class RecvBehav(OneShotBehaviour):
		async def run(self):
			global msg_contain
			print("Agente receptor en funcionamiento")

			msg = await self.receive(timeout=t_out) # wait for a message for 10 seconds
			if msg:
				#print("Mensaje recibido: {}".format(msg.body))
				msg_contain = msg.body
			
			else:
				print("No se recibio mensajes en ", t_out, " segundos")

			# stop agent from behaviour
			await self.agent.stop()

	async def setup(self):
		print("Agente receptor Iniciado")
		b = self.RecvBehav()
		template = Template()
		template.set_metadata("performative", "inform")
		self.add_behaviour(b, template)

if __name__ == "__main__":
	receiveragent = ReceiverAgent("mccagente2@trashserver.net", "12345678")
	future = receiveragent.start()
	future.result() # wait for receiver agent to be prepared.

	while receiveragent.is_alive():
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			receiveragent.stop()
			break

	index_ruta = msg_contain.find("1RUTA:")
	index_files = msg_contain.find("2ARCHIVOS:")
	index_ip = msg_contain.find("3IP:")
	index_cpu = msg_contain.find("4CPU:")
	index_stat = msg_contain.find("5STATUS:")
	index_end = msg_contain.find("---END---")


	ruta = msg_contain[index_ruta+7:index_files-2]
	all_files = msg_contain[index_files+11:index_ip-2]
	ip = msg_contain[index_ip+5:index_cpu-2]
	resultado = msg_contain[index_stat+9:index_end]
	
	try:
		cpu_used = float(msg_contain[index_cpu+6:index_stat-2])
	except:
		print("Agente indisponible, vuelva a intentar")
		quit()
		cpu_used = "Null"
	files = all_files.split(",")
	files_col = ""
	for elemento in files:
		files_col = files_col + elemento + "\n"
		
	print("\n---Directorio:--- \n",ruta, sep="")
	print("\n---Archivos:--- \n",files_col, sep="")
	print("---IP PUBLICA:--- \n",ip, sep="")
	print("\n---%CPU USADO:--- \n",cpu_used, sep="")
	print("\n---RESULTADO:--- \n",resultado, sep="")
	
	print("\n\nAgente finalizado")
	

 
	if cpu_used != "Null" and cpu_used < 40:
		print("El agente puede ejecutar codigo")
		
		#print(datetime.today())
		
		try:
			directorio = 'Directorio_generado_agente2'
			os.mkdir(directorio)
		except:
			pass
	else:
		print("CPU del agente por encima del 40%, intentar en otro momento")
		quit()

	path = os.getcwd()+"/"+directorio
	#def Segunda_funcion():
 	#	print(resultado, "\nFecha ",datetime.today(), sep="", file=file)
	texto = "---Fecha de ejecucion: " + str(datetime.today()) + "---\n\n" + resultado
	file_path = path+"/"+"generado.txt"
	file = open(file_path,"w")
	file.write(texto)
	#print("Un texto se escribirá", file=file)
	file.close()
	print("\nSe procede a ejecutar el codigo y guardarlo en el siguiente directorio: ",path)
