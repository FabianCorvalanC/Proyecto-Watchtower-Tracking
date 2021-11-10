###Este es el programa para la sustraccion de fondo mediante el método de contrastar una imagen del fondo vacio y una con autos en ella


import sys
import argparse
import gym
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv
import numpy as np
import cv2


####definicion de argumentos y enviroment#########################################################
if __name__ == '__main__':

    # Se leen los argumentos de entrada
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-name', default="Duckietown-udem1-v1")
    parser.add_argument('--map-name', default='tracking_map.yaml')
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
    ##############################################################################################################



    #A continuacion  se  lee una imagen del fondo del simulador (sin autos) mediante .imread y es almacenada en la variable background,
    # la imagen puede ser tomada mediante el programa  backgroundimage.py  ##

    background=cv2.imread('background.jpg')

    while True:

        # Captura la tecla que está siendo apretada y almacena su valor en key
        key = cv2.waitKey(30)
        # Si la tecla es Esc, se sale del loop y termina el programa
        if key == 27:
            break

        action = np.array([0.0, 0.0])
        # Se ejecuta la acción definida anteriormente y se retorna la observación (obs),
        # la evaluación (reward), etc
        obs, reward, done, info = env.step(action)
        # obs consiste en un imagen RGB de 640 x 480 x 3

        ## a continuacion se contrastan las imagen del fondo (background) con el simulador  con duckiebots (obs)
        substraction=cv2.absdiff(background,obs)

        ##se realizan operaciones para limpiar la imagen ###############################################
        _,substractionbinary=cv2.threshold(cv2.cvtColor(substraction,cv2.COLOR_RGB2GRAY),10,255,cv2.THRESH_BINARY)
        kernel1=np.ones((10,10),np.uint8)
        kernel2=np.ones((2,2),np.uint8)
        output=cv2.GaussianBlur(substractionbinary,(5,5),0)
        
        output1=cv2.erode(output,kernel1,iterations=1)
        output2=cv2.dilate(output1,kernel2,iterations=1)
        output3=cv2.inRange(output2,50,255)

        # done significa que el Duckiebot chocó con un objeto o se salió del camino
        if done:
            print('done!')
            # En ese caso se reinicia el simulador
            env.reset()


        ## se muestran los resultados  (obs=original,subsrtaction= final) ### 
        cv2.imshow('obs',cv2.cvtColor(obs,cv2.COLOR_RGB2BGR))
        cv2.imshow('substraction',output3)
        
    #Se cierra el environment y termina el programa
env.close()
