def ContenidoSi():
	resultado = ""

	# Calcularemos el seno de x:
		
	PI = 3.1459
	x = PI/6
	def factorial(a):
		if a == 0:
			return 1
		else:
			return a*factorial(a-1)
	#Inicializamos Seno en 0
	sen = 0
	#Calculamos el seno de "x" segun la serie de taylor:
	for n in range(20):
		sen += (((-1)**(n))/factorial(2*n+1))*(x**(2*n+1))
	#Se crea el contenido
	resultado = "El seno de " + str(x) + " es: " + str(sen)

	return resultado


def ContenidoNo():
	#Se crea el contenido
	mensaje = "El agente esta usando mas del 40% del CPU"
	return mensaje
