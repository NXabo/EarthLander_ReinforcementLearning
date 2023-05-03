# EarthLander - Nicolas Xaborov - Modifié pour Reinforcement Learning
# 04/2023 #

# Take EL as EarthLander
# Take RL as Reinforcement Learning
# Take eps as epsilon, wich make the choice between exploration and exploitation

# Please be aware that your environment must have these packages :
###########
import random as r
import numpy as np
import matplotlib.pyplot as mp
import math
###########

############ EL parameters
altitude = 8100
speed = 268
throttle = 0
fuel = 1000
state = 0
alt_poss = [[0,800],[800,2000],[2000,3000],[3000,4000],[4000,5000],[5000,999999]]
speed_poss = [[-999999,0],[0,40],[40,70],[70,200],[200,999999]]
############

########### RL parameters
eps_train = 0
eps_test = 0
epi_train = 15000
epi_test = 800
###########

############# FeedBack parameters
pos_re = 1
neg_re = -200
dis_fa = 1
last_speed = []
#############

########### Fonction d'environement
def environment(nbr_episode,trans_matrix,epsilon,is_train):

    if is_train :
        print("Session d'entrainement...")
    else :
        print("Session de test...")
    

    ############# FeedBack parameters
    global pos_re
    global neg_re
    global dis_fa
    global last_speed
    landed = np.zeros(nbr_episode)
    #############

    ############ EL parameters
    global altitude
    global speed
    global throttle
    global fuel
    global state
    global alt_poss
    global speed_poss
    ############

    for episode in range(nbr_episode) :

        ############# Affiche de la progression 
        if episode%200 == 0: print("Progression : "+str(episode)+" épisodes passés.")
        #############

        ############# Variable d'état de partie
        game_state = 0 # Partie non-finie = 0, perdue = 1, gagnée = 2
        #############

        ############# Variable de log des actions prises en fonction de l'état
        log_state_action = np.empty((0,2))
        #############

        ############ EL parameters - Doivent être reset pour chaque épisode
        # Les randoms introduits permettent d'obtenir une matrice de transition plus robuste
        altitude = 8100 + r.randint(0,100) * 10
        speed = 268 + r.randint(-5,5) * 10
        throttle = 0
        fuel = 1000
        state = 0
        ############

        ############ Boucle pour une partie :
        while game_state == 0:
            
            ############ Gestion de l'état
            for i in range(len(alt_poss)):
                if alt_poss[i][0] <= altitude and alt_poss[i][1] > altitude:
                    state = i
                    break
            for i in range(len(speed_poss)):
                if speed_poss[i][0] <= speed and speed_poss[i][1] > speed:
                    state = state * len(speed_poss) + i
                    break
            ############

            ############ MaJ de l'action choisie par Agent_QL
            throttle = agent_QL(trans_matrix,epsilon)
            if fuel <= 0:
                fuel = 0
                throttle = 0
            ############

            ############ MaJ des paramètres EL
            a = 9.8-throttle
            altitude -= speed*0.1 - a*0.01/2
            speed += a*0.1
            fuel -= throttle*0.1
            ############

            ############ MaJ de la variable des log(s)
            log_state_action = np.concatenate((log_state_action, np.array([[state,throttle]])))
            ############

            ############ Conditions de fin de partie 
            if altitude <= 0:
                last_speed.append(speed)
                if speed <= 40:
                    altitude = 0
                    throttle = 0
                    speed = 0
                    game_state = 2
                else:
                    altitude = 0
                    throttle = 0
                    speed = 0
                    game_state = 1
            ############
        
        ############

        ############ End of the game, feedback
        if is_train:
            if game_state == 2:
                reward = pos_re
            else:
                reward = neg_re
            for i in range(log_state_action.shape[0]):
                a = log_state_action.shape[0]-1-i
                trans_matrix[int(log_state_action[a,0]),int(log_state_action[a,1])] += reward
                reward *= dis_fa
        landed[episode] = game_state
    return landed
    ############


############ Fonction d'agent de réenforcement
def agent_QL(trans_matrix,epsilon):
    a = r.random()
    if a < epsilon:
        action = r.randint(0,19)
    else: 
        indice_max_rewarded = np.argmax(trans_matrix,axis=1)
        action = indice_max_rewarded[state]
    return action
############

############ Pre-set :
trans_matrix = np.zeros((len(speed_poss)*len(alt_poss),20))
# premier paramètre : nombre d'état qui est le nombre d'intervalles d'altitude possible
# multiplé par le nombre d'intervalles de vitesse possible
# second paramètre : nombre de niveau de puissance moteur possible (20 par défaut dans EL)
############

############ Training session, set the trans_matrix
landed = environment(epi_train,trans_matrix,eps_train,True)
np.savetxt("trans_matrix.txt",trans_matrix,fmt="%d")
#mp.plot(landed)
#mp.show()
############

trans_matrix = np.loadtxt("trans_matrix.txt")

############ Testing session, test the trans_matrix
landed = environment(epi_test,trans_matrix,eps_test,False)
np.savetxt("trans_matrix.txt",trans_matrix,fmt="%d")
mp.plot(landed)
mp.show()
############