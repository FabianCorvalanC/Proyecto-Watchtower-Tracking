# Proyecto-Watchtower-Tracking
## Presentacion

### Se presenta el proyecto "Watchtower" , realizado por Lukas Vasquez, Sebastian Oñate y Fabian Corvalan
### El proyecto busca crear un sistema de control en las calles de Duckietown, para lo cual, 
### mediante una camara de vigilancia logra contar cuantos autos pasan por un area determinada. 

## Soluciones 
### Se llevaron a cabo 2 soluciones para la extracción de fondo en la carpeta "sustraccion_inicial" se puede hayar la primera solución, la cual fue realizada de manera "bruta" ocupando una imagen de fondo  sin autos y la resta  mediante cv2.absdiff.
### La segunda solución se puede encontrar en la carpeta "solucion_simulador" y se realizo con los algoritmos de sustracción ya implementados en open cv, en este caso se utiliza MOG2.Para los avances posteriores se trabaja sobre esta solución debido a su simplicidad.
### Para poder correr estas dos soluciones es necesario realizar las siguientes modificaciones en el simulador:
-posicion inicial:
	archivo: gym_duckietown/simulator.py
	linea: 475
	propose_pos = np.array([0.85, 0.2, 0.85])

	linea: 478
	propose_angle = 0

-velocidad del duckiebot
	archivo: gym_duckietown/objects.py
	linea: 117
	self.velocity = 0.3
-ademas se utiliza el mapa "tracking_map.yaml".
### por ultimo se realiza una implementacion a partir de un video real de duckietown, puede encontrarse en la carpeta "solucion_real" junto al video de prueba.