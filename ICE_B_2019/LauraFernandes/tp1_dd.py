"""
@author: LauraFernandes
"""
from tp1_data import teste, estrela
import numpy as np
import math

"""
Função distancia
Função que devolve a distância entre os pares de coordenadas p1 e p2 a partir do cálculo que se encontra no enunciado
"""
def distancia(altitudes, lado, p1, p2):
    return math.sqrt(math.pow(lado*(p1[0] - p2[0]), 2) + math.pow(lado*(p1[1] - p2[1]), 2) + math.pow((altitudes[p1[0]][p1[1]] - altitudes[p2[0]][p2[1]]), 2))


"""
Função distancia_percorrida
Função que devolve a distância total entre o conjunto de pares de coordenadas encontrados no vetor caminho
"""
def distancia_percorrida(altitudes, lado, caminho):
    distance = 0
    
    for ix in range(1,len(caminho)):
        distance += distancia(altitudes, lado, caminho[ix-1], caminho[ix])
    
    return distance


"""
Função subir_norte
Função que devolve o par de coordenadas que tenha o maior valor de altitude. São comparados o par dado e o par imediatamente a cima (a norte) do primeiro
"""
def subir_norte(altitudes, inicio):  
    if ((inicio[0] < len(altitudes)) & ((inicio[0] - 1) >= 0) & (altitudes[inicio[0]][inicio[1]] < altitudes[inicio[0]-1][inicio[1]])):
        return ((inicio[0]-1), inicio[1])


"""
Função vizinhas
Função que devolve o conjunto de pares de coordenadas vizinhos de um dado par 
"""
def vizinhas(alturas, celula):    
    vizinhos = []
    
    if ((celula[0] >= 0) & (celula[1] >= 0)):
      
        if (celula[0] == 0):
            iniciox = 0
            fimx    = 2
            
            #Canto Superior Esquerdo#
            if (celula[1] == 0):                                                            
                inicioy = 0
                fimy    = 2
        
            #Canto Superior Direito#    
            elif (celula[1] == (len(alturas[0]) - 1)):                                       
                inicioy = (len(alturas[0]) - 2)
                fimy    = len(alturas[0])
              
            #Limite Superior#      
            elif ((celula[1] != 0) | (celula[1] != (len(alturas[0]) - 1))):                  
                inicioy = (celula[1]-1)
                fimy    = (celula[1]+2)
                      
        elif (celula[0] == (len(alturas) - 1)):                                          
            iniciox = (len(alturas)-2)
            fimx    = len(alturas)
            
            #Canto Inferior Esquerdo#   
            if (celula[1] == 0):
                inicioy = 0
                fimy    = 2
            
            #Canto Inferior Direto#                        
            elif (celula[1] == (len(alturas[0]) - 1)):                      
                inicioy = (len(alturas[0])-2)
                fimy    = len(alturas[0])
        
            #Limite Inferior#
            elif ((celula[1] != 0) | (celula[1] != (len(alturas[0]) - 1))):
                inicioy = (celula[1]-1)
                fimy    = (celula[1]+2)
        
        
        elif ((celula[0] != 0) | (celula[0] != (len(alturas) - 1))):
            iniciox = (celula[0]-1)
            fimx    = (celula[0]+2)
              
            if (celula[1] == 0):                     
                inicioy = 0
                fimy    = 2
            
            #Limite Direito#
            elif (celula[1] == (len(alturas[0]) - 1)):
                inicioy = (len(alturas[0])-2)
                fimy    = len(alturas[0])
        
            #Interior#
            else:   
                iniciox = (celula[0]-1)
                fimx    = (celula[0]+2)
                inicioy = (celula[1]-1)
                fimy    = (celula[1]+2)
                
        for ix in range(iniciox, fimx):
                for iy in range(inicioy, fimy):
                    if ((ix == celula[0]) & (iy == celula[1])):
                        continue
                    else:
                        vizinhos.append((ix, iy))                        
                        #print (ix)
                        #print (iy)                                             
    return vizinhos


"""
Função vizinha_mais_alta
Função que devolve o de par de coordenadas vizinho com a maior altitude
"""
def vizinha_mais_alta(altitudes, celula): 
    flag = False
    
    Vizinhos = vizinhas(altitudes, celula)
    Altitude = 0
    for i in range (len(Vizinhos)):
        tuplo = Vizinhos[i]
        
        if ((altitudes[tuplo[0]][tuplo[1]] > altitudes[celula[0]][celula[1]])):
            flag = True
            if (altitudes[tuplo[0]][tuplo[1]] > Altitude):
                Altitude = altitudes[tuplo[0]][tuplo[1]]
              
    if (flag == True):  
        for i in range (len(Vizinhos)):
            tuplo = Vizinhos[i]
            
            #print (tuplo)
            #print(altitudes[tuplo[0]][tuplo[1]])
            
            if (altitudes[tuplo[0]][tuplo[1]] == Altitude):
                return tuplo
                break
    else:
        return celula


"""
Função subir_mais_alto
Função que devolve o conjunto de pares de coordenadas que têm a altitude mais alta em cada raio de vizinhos. Este acaba quando as células vizinhas não dispõem de altitude maior que a atual
"""
def subir_mais_alto(altitudes, celula):   
    Caminho = []
    Caminho.append(celula)
    
    while (1):
        Tuplo = vizinha_mais_alta(altitudes, Caminho[-1])
        #print (Tuplo)
        if (Caminho[-1] == Tuplo):
            break
        else:
            Caminho.append(Tuplo)
    
    return Caminho