# Se presenta el proyecto "Watchtower" , realizado por Lukas Vasquez, Sebastian Oñate y Fabian Corvalan
# El proyecta busca crear un sistema de control en las calles de Duckietown, para lo cual, 
# mediante una camara de vigilancia logra contar cuantos autos pasan por un area determinada. 

import sys
import argparse
import gym
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv
import numpy as np
import cv2
import random
########## se leen los argumentos y se define el enviroment#############
cap=cv2.VideoCapture('circuito_duckie.mp4')
###################################################################################




##########################################################################

### se  declara MOG2  en una variable background substraction ######################
background_substractor=cv2.createBackgroundSubtractorMOG2()
    
    
# fijamos un contador de autos que sera utilizado mas adelante

contador_auto = 0 #cuenta autos
contar=True # se activa para contar autos
step=0 # se deja de contar autos hasta que llegue a 50

 
while True:

    ret,frame = cap.read()  

    # Captura la tecla que está siendo apretada y almacena su valor en key
    key = cv2.waitKey(30)
    # Si la tecla es Esc, se sale del loop y termina el programa
    if key == 27:
        break
        

        # especificamos area a analizar que corresponde a toda el area de la imagen, que corresponde a toda la area de la imagen
    area_pts = np.array([(235, 100), (0,500), (700,500), (400,100)])
    
        

       
    # creamos una imagen auxiliar, donde determinamos el area en la que actuará el detector
    imagen_aux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8) 
    imagen_aux = cv2.drawContours(imagen_aux, [area_pts], -1, (255), -1)
    imagen_area = cv2.bitwise_and(frame, frame, mask=imagen_aux)
    


   
    # aplicamos la sustraccion de fondo
    mask = background_substractor.apply(imagen_area)
 
    kernel1=np.ones((10,10),np.uint8)
    kernel2=np.ones((2,2),np.uint8)
    output=cv2.GaussianBlur(mask,(5,5),0) 
    output1=cv2.erode(output,kernel1,iterations=1)
    output2=cv2.dilate(output1,kernel2,iterations=1)
    output3=cv2.inRange(output2,50,255)

    

    # encontramos los contornos presentes de mask, para luego basándonos en su área poder determinar si existe movimiento (autos)
    cnts = cv2.findContours(output3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
  

    for cnt in cnts:#encerramos contornos en boundig boxes y agregamos texto 
        if cv2.contourArea(cnt) > 1100:
            x, y, w, h = cv2.boundingRect(cnt)
                # encasillamos el auto
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,250), 2)
            cv2.putText(frame, 'Duckiebot', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 255, 255), 1, cv2.LINE_AA)
               
        #generamos condicion que activa el contador, la idea es que el contador se active y luego se desactive por un tiempo
        #para que no se cuente un mismo auto dos veces

        if contar:
                #si contar es True el contador de autos esta activado y aumenta=+1  
            if 270 < y+h < 282:
                contador_auto += 1
                cv2.line(frame, (165, 280), (500, 280), (255,0,0),3)
                contar=False #una vez aumenta,deja de  contar=False
               
        else:# si contar no es True no se activa el contador de autos hasta que step=50
            step+=1
            if step ==50:
                contar=True
                step=0

                
        # visualizamos los contenidos

        # muestra la linea del filtro
    cv2.line(frame, (165, 280), (500, 280), (0,255,0), 2)
        # muestra un recuadro para el contador
    cv2.rectangle(frame, (510,255), (585,315), (255,0,255), 2)
        # texto de contador
    cv2.putText(frame,"Total:", (510,250),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        #muestra titulo
    cv2.putText(frame,"Watchtower Tracking", (10,25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
        #texto
    cv2.putText(frame,"Counting..", (500 , 400),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,195,50), 2)
        # muestra el contador
    cv2.putText(frame, str(contador_auto), (520,295),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
        # muestra la ventana emergente con el sistema implementado
    cv2.imshow('Proyecto Watchtower Duckietown',frame)


       



