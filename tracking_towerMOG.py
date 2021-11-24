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
if __name__ == '__main__':

    # Se leen los argumentos de entrada
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default="Duckietown-udem1-v1")
    parser.add_argument('--map-name', default='tracking_map.yaml')##mapa a utilizar
    parser.add_argument('--distortion', default=False, action='store_true')
    parser.add_argument('--draw-curve', action='store_true', help='draw the lane following curve')
    parser.add_argument('--draw-bbox', action='store_true', help='draw collision detection bounding boxes')
    parser.add_argument('--domain-rand', action='store_true', help='enable domain randomization')
    parser.add_argument('--frame-skip', default=1, type=int, help='number of frames to skip')
    parser.add_argument('--seed', default=1, type=int, help='seed')
    args = parser.parse_args()

    # Definición del environment
    if args.env_name and args.env_name.find('Duckietown') != -1:
        env = DuckietownEnv(
            seed = args.seed,
            map_name = args.map_name,
            draw_curve = args.draw_curve,
            draw_bbox = args.draw_bbox,
            domain_rand = args.domain_rand,
            frame_skip = args.frame_skip,
            distortion = args.distortion,
        )
    else:
        env = gym.make(args.env_name)

    # Se reinicia el environment
    env.reset()
##########################################################################

### se  declara MOG2  en una variable background substraction ######################
    background_substractor=cv2.createBackgroundSubtractorMOG2()
    
    
    # fijamos un contador de autos que sera utilizado mas adelante
    contador_auto = 0
 


    while True:

        # Captura la tecla que está siendo apretada y almacena su valor en key
        key = cv2.waitKey(30)
        # Si la tecla es Esc, se sale del loop y termina el programa
        if key == 27:
            break
        
        action =np.array([0.0, 0.0]) # no hay movimiento
        
        obs, reward, done, info = env.step(action)
        # obs consiste en un imagen RGB de 640 x 480 x 3
        

        # done significa que el Duckiebot chocó con un objeto o se salió del camino
        if done:
            print('done!')
            # En ese caso se reinicia el simulador
            env.reset()

        # especificamos area a analizar que corresponde a toda el area de la imagen, que corresponde a toda la area de la imagen
        area_pts = np.array([(235, 135), (0,500), (700,500), (400,135)])
       
        

       
        # creamos una imagen auxiliar, donde determinamos el area en la que actuará el detector
        imagen_aux = np.zeros(shape=(obs.shape[:2]), dtype=np.uint8) 
        imagen_aux = cv2.drawContours(imagen_aux, [area_pts], -1, (255), -1)
        imagen_area = cv2.bitwise_and(obs, obs, mask=imagen_aux)
   
        # aplicamos la sustraccion de fondo
        mask = background_substractor.apply(imagen_area)

        # encontramos los contornos presentes de mask, para luego basándonos en su área poder determinar si existe movimiento (autos)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for cnt in cnts:
            if cv2.contourArea(cnt) > 1500:
                x, y, w, h = cv2.boundingRect(cnt)
                # encasillamos el auto
                cv2.rectangle(obs, (x,y), (x+w,y+h), (0,0,250), 2)
                cv2.putText(obs, 'Duckiebot', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (255, 255, 255), 1, cv2.LINE_AA)
               

                # aumentamos el contador
                if 278 < y+h < 282:
                    contador_auto += 1
                    cv2.line(obs, (165, 280), (500, 280), (255,0,0),3)
                

        # visualizamos los contenidos

        # muestra la linea del filtro
        cv2.line(obs, (165, 280), (500, 280), (0,255,0), 2)
        # muestra un recuadro para el contador
        cv2.rectangle(obs, (510,255), (585,315), (255,0,255), 2)
        #
        cv2.putText(obs,"Total:", (510,250),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.putText(obs,"Watchtower Tracking", (10,25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
        
        cv2.putText(obs,"Counting..", (500 , 400),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,195,50), 2)
        
        # muestra el contador
        cv2.putText(obs, str(contador_auto), (520,295),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
        # muestra la ventana emergente con el sistema implementado
        cv2.imshow('Proyecto Watchtower Duckietown',cv2.cvtColor(obs,cv2.COLOR_RGB2BGR))

       
    #Se cierra el environment y termina el programa
env.close()
