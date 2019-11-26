"""
Created on Fri Apr 20 22:11:33 2018

@author: RitaLeite and CarolinaDias
"""

from tp1_data import cities, distances  

days = [[0 for x in range(len(distances[0]))] for y in range(len(distances[0]))]; #Global matrix needed to save travel_days function's result 

# 2.0 - distances on a path calcule

def partial_distances(distances, indexes):
    """
    Cálculo das distâncias parciais entre os pontos de visita. 
    Esta função devolve as distâncias parciais entre a a primeira e a segunda cidade,
    entre a segunda e a terceira, e assim sucessivamente.
    """
    
    partial_distance = []                                                       
    for ix in range(1,len(indexes)):
        distances[indexes[ix-1]][indexes[ix]]
        partial_distance.append(distances[indexes[ix-1]][indexes[ix]])
    
    return partial_distance
  
# 2.1 - travel days calcule 

def travel_days(distances, short, max_drive):
    """
    Cálculo do tempo necessário para percorrer as distâncias entre as cidades.
    Caso a distância entre as cidades seja menor que 200km não será necessário perder um dia de viagem;
    caso a distância esteja entre os 200 e os 800km´s necessitarão de um dia inteiro para viagem;
    caso a distância seja superior a 800km´s necessitarão de 2 dias para viagem.
    
    """
    
    distances_row = 0;                                                          #Variable needed to travel through distances' matrix rows
    distances_column = 0;                                                       #Variable needed to travel through distances' matrix columns
    decision_array = [[0 for x in range(len(distances[0]))] for y in range(len(distances[0]))];
    
    while distances_row < len(distances[0]):                                    #Cycle needed to go through distances' matrix rows
        
        while distances_column < len(distances[0]):                             #Cycle needed to go through distances' matrix columns
            
            if (distances[distances_row][distances_column] < short):            #Check if a given distance is below 'short' variable
                decision_array[distances_row][distances_column] = 0;
            else:
                if ((distances[distances_row][distances_column] > short) & (distances[distances_row][distances_column] < max_drive)): #Check if a given distance is between 'short' and 'max_drive' variables
                    decision_array[distances_row][distances_column] = 1;    
                else:
                    if(distances[distances_row][distances_column] > max_drive): #Check if a given distance is above 'max_drive' variable
                        decision_array[distances_row][distances_column] = 2; 
                        
            distances_column = distances_column + 1;                            #Increment distances_column to next column of 'distances'
            
        distances_row = distances_row + 1;                                      #Increment distances_row to next row of 'distances'
        distances_column = 0;                                                   #When the cycle finishes a line, reset distances_column
    
                                                
    return decision_array
    
# 2.2 - total cost calcule

def total_cost(distances, days, indexes): 
    """
    Função que devolve o custo total do itinerário, tanto em quilómetros
    como em dias de viagem entre cidades.
    """
    
    dis = sum(partial_distances(distances, indexes));
    t_days = 0
    
    for elements in range(1,len(indexes)):                                      
        a = indexes[elements-1]
        b = indexes[elements]
        t_days = t_days + days[a][b]

    return (dis,t_days)

# 2.3 - total cost through the cities names calcule

def city_indexes(reference, names):
    """
    Função que devolve o indice das cidades indicadas.
    """
    x = 0; 
    index_array = [0]*len(names);                                               
    
    while x < len(names):
        reference.index(names[x]);
        index_array[x] = reference.index(names[x]);
        x = x + 1 
 
    return index_array;
    
def journey_cost(city_names, distances, days, visit):
    """
    Função que devolve o custo total da viagem usando o nome das cidades.
    """
    y = city_indexes(city_names, visit);
    w = total_cost(distances, days, y);
    journey_cost = w;
    
    return journey_cost
