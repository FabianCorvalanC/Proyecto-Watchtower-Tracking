# Proyecto-Watchtower-Tracking
### Se presenta el proyecto "Watchtower" , realizado por Lukas Vasquez, Sebastian Oñate y Fabian Corvalan
### El proyecta busca crear un sistema de control en las calles de Duckietown, para lo cual, 
### mediante una camara de vigilancia logra contar cuantos autos pasan por un area determinada. 

### Se llevaron a cabo 2 soluciones para la extracción de fondo en la carpeta BS se puede hayar la primera solución, la cual fue realizada de manera "bruta" ocupando una imagen de fondo  sin autos y la resta  mediante cv2.absdiff.
### La segunda solución se realiz+o con los algoritmos de sustracción ya implementados en open cv, en este caso se utiliza MOG2.Para los avances posteriores se trabaja sobre esta solución debido a su simplicidad.