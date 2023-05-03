# EarthLander - Nicolas Xaborov - Modifié pour Reinforcement Learning - README
# 04/2023 #


#### DOSSIER ####
Vérifiez que dans votre dossier se trouve les éléments suivants :
- EarthLanderQL, fichier par lequel vous allez générer la matrice de prise de décision
  pour votre agent de réenforcement.
- EarthLanderManual, fichier dans lequel vous pourrez lancer le jeu au format graphique
  et tester votre matrice de prise de décision.
- trans_matrix.txt, fichier texte dans lequel sera sauvé la matrice de prise de décision
  et qui sera chargé dans EarthLanderManual lors de votre test graphique.


#### MAKE IT WORK ####
Ligne par ligne vous sera décrit quoi changer/introduire.

## MatrixGenerator.py :
ligne 17 et 18, introduire vos paramètres de départ (altitude et vitesse)
ligne 22 et 23, introduire les vecteurs d'altitudes et vitesses possibles
                EXEMPLE :
                alt_poss = [[0,1000],[1000,2000],[2000,3000],
                           [3000,4000],[4000,5000],[5000,99999999999]]
                speed_poss = [[-999,0],[0,40],[40,999999]]
                VEILLEZ à ce que les intervalles se suivent directement, que la 
                valeur de droite soit la valeur de gauche dans l'intervalle qui suit.
ligne 27 à 30, introduire vos paramètres epsilon (eps_...) et episodes (epi_...)
ligne 34 à 36, introduire vos paramètres de feedback (reward positif et négatif et le
               disrupt factor)
ligne 37, pour un gain de temps de traitement, vous pouvez mettre en commentaire last_speed
          mais devez alors également commenter la ligne 53 et la ligne 123
ligne 63 et 64, ré-introduire les vecteurs d'altitudes et vitesses possibles
ligne 70, réglez la fréquence de mise à jour de la progression en modifiant la valeur
          après le modulo (%). Plus la valeur est grande, moins souvent la progression
          est rapportée
ligne 82 et 83, ré-introduisez vos paramètres de départ

## EarthLanderManual.py :
ligne 12, 13, 20 et 21, ré-introduisez les paramètres en respectant ce que vous avez fait dans 
                        EarthLanderQL.


#### trans_matrix ####

N'oubliez pas de vider le fichier entre chaque entrainement, car sinon votre matrice
précédente influencera vos résultats.
Clic droit sur le fichier -> ouvrir avec -> bloc-note -> supprimez tous pour en faire 
un fichier texte vide. 


BONNE CHANCE, 

            Nicolas Xaborov.
