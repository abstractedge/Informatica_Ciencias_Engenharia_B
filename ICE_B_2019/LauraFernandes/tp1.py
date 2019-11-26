TP2_3.py
A
A
F
J
Type
Text
Size
6 KB (6,171 bytes)
Storage used
6 KB (6,171 bytes)
Location
Rita Leite
Owner
me
Modified
May 29, 2019 by me
Opened
12:48 PM by me
Created
Jun 24, 2019
Add a description
Viewers can download

# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:11:09 2018

@author: Carolina Dias e Rita Leite
"""
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

             
def base_dados(argumento,conecao):
  
    if conecao!=None:
        conecao.close()
    print('*'+argumento+'*') 
    conn=sqlite3.connect(argumento)
   
    return conn
    
    

def reportar(objeto,fich):
    
    #especifica o nome do ficheiro de relatorio que ira ser preenchido
   
    if fich!=None:
        fich.close()
        
    ficheiro_open = open(objeto,'w')
    return ficheiro_open


def criar_tabelas(nomeBD):
    
    try:
        cursor=nomeBD.cursor()
        cursor.execute('CREATE TABLE Lotes ( Identificador_lote TEXT, Estirpe TEXT,'+\
                       'Codigo TEXT, Temperatura_incubação INT, PRIMARY KEY(Identificador_lote));')
        cursor.execute('CREATE TABLE Amostras (Identificador_amostra TEXT, Identificador_lote TEXT, Tempo INT, Concentracao REAL, PRIMARY KEY(Identificador_amostra));')
        nomeBD.commit()
    except:
        print('Erro a criar tabela!')
        
              
def carregar(ficheiro,nomeBD):
    
    #Ler um ficheiro com o nome indicado e carregar a informacao para as tabelas da base de
    #dados nomeBD
    
    linhas = open(ficheiro).readlines()
    cursor = nomeBD.cursor()    

    for linha in linhas:
        try:
             amostra = linha.strip()
             sql_lotes = 'INSERT INTO Lotes VALUES ( "{0}", "{1}", "{2}", {3});'
             sql_lotes = sql_lotes.format(amostra[0],amostra[1],amostra[2],amostra[3])
             cursor.execute(sql_lotes)
             nomeBD.commit()
        except:
             print('Erro na ',linha)
     
     
    for linha in linhas:
         try:
             amostra = linha.strip().split(';')
             sql_amostras = 'INSERT INTO Amostras VALUES ( "{0}", "{1}", {2}, {3});'
             for linha in linhas[4:]:
                 identificador_lote,identificador_amostra,tempo,concentracao=linha.split(';')
             sql_amostras = sql_amostras.format(identificador_lote,identificador_amostra,tempo,concentracao)
             cursor.execute(sql_amostras)
             nomeBD.commit()
         except:
             print('Erro na ',linha)
    


def query_db(conn,query):
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    result = []
    for record in records:
        dicionario={}
        for ix in range(len(record)):
            dicionario[cursor.description[ix][0]]=record[ix]
        result.append(dicionario)
    return result         

 
def estirpes(ficheiro,nomeBD,minT,maxT,meio): 
    
    #Escrever no ficheiro seleccionado para o relatorio os codigos das estirpes que tenham sido
    #cultivadas a temperaturas entre minT e maxT no meio especificado em meio.

    caracteristicas=[]
    if meio!='*':
        caracteristicas.append('Codigo is '+ '"{}"'.format(meio))
    if minT!='*':
        caracteristicas.append('Temperatura>'+str(minT))
    if maxT!='*':
        caracteristicas.append('Temperatura<'+str(maxT))
    sequencia='SELECT DISTINCT Estirpe FROM Lotes'
    if len(caracteristicas)>=1:
        sequencia=sequencia+' WHERE '+' AND '.join(caracteristicas)+';'
    else:
        sequencia=sequencia+';'
    doc=query_db(nomeBD,sequencia)
       
    #2.1
    dados= '{0} estirpes cultivadas com o meio {1} entre {2} ºC e {3}ºC \n {4}'
    dados=dados.format(len(doc),meio,minT,maxT)
    ficheiro.write(dados)
    
    for linha in doc:
        ficheiro.write(linha['Estirpe']+'\n')
    
def x(estirpe,nomeBD):
    query_x='SELECT Tempo FROM Amostras JOIN Lotes USING (Identificador_lote) WHERE Estirpe is "{0}";'
    sql=query_x.format(estirpe)
    tempo_x=[]
    valores=query_db(nomeBD,sql)
    for valor in valores:
        tempo_x.append((valor['Tempo'])/60)
    return tempo_x    
    

def y(estirpe,nomeBD):
    query_y='SELECT Concentracao FROM Amostras JOIN Lotes USING (Identificador_lote) WHERE Estirpe is "{0}";'
    sql=query_y.format(estirpe)
    concentracao_y=[]
    valores=query_db(nomeBD,sql)
    for valor in valores:
        concentracao_y.append(valor['Concentracao'])
    return concentracao_y   
    

def grafico(ficheiro,nomeBD,estirpe): 
    plt.plot(x(estirpe,nomeBD),y(estirpe,nomeBD),'k.')
    plt.title('Estirpe:{0}'.format(estirpe))
    plt.xlabel('Tempo/horas')
    plt.ylabel('[Insulina](g/L)')
    plt.savefig('ficheiro')
    plt.close()
  
         
def beta(eixo_x,eixo_y):
    #calcular a regressão linear
    somatorio_x=0
    somatorio_y=0
    somatorio_xy=0
    somatorio_xx=0
    
    for ix in range(len(eixo_x)):
        somatorio_x=somatorio_x+eixo_x[ix]
        somatorio_xx=somatorio_xx+eixo_x[ix]**2
    for ix in range(len(eixo_y)):
        somatorio_y=somatorio_y+eixo_y[ix]
        somatorio_xy=somatorio_xy+ eixo_x[ix]*eixo_y[ix]
    beta=(somatorio_xy-((1/len(eixo_x))*somatorio_x*somatorio_y))/(somatorio_xx-((1/len(eixo_x))*(somatorio_x)**2))
    return beta
    
def processar(ficheiro):
    
    teste=open(ficheiro).readlines()
    b_d=None
    rp=None
    for line in teste:
        
        if ' ' in line:
           comando,argumento=line.strip().split(' ')
        else: 
            comando=line.strip()
            
        if comando=='BASE_DADOS':
             print(argumento)
             b_d=base_dados(argumento,b_d)             
        elif comando=='REPORT':
             rp=reportar(argumento,rp)
        elif comando=='CRIAR_TABELAS':
             criar_tabelas(b_d)
        elif comando=='CARREGAR':
             carregar(argumento,b_d)
        elif comando=='ESTIRPES':
             minT,maxT,meio=argumento.strip().split(';')
             estirpes(rp,b_d,minT,maxT,meio)
        elif comando=='GRAFICO':
             ficheiro_nome,estirpe_nome=argumento.strip().split(';')  
             grafico(rp,b_d,estirpe_nome)
             
    b_d.close()
    rp.close() 
    
   """
@author: LauraFernandes
"""
from tp1_data import teste, estrela
import numpy as np
import math


def distancia(altitudes, lado, p1, p2):

    return math.sqrt(math.pow(lado*(p1[0] - p2[0]), 2) + math.pow(lado*(p1[1] - p2[1]), 2) + math.pow((altitudes[p1[0]][p1[1]] - altitudes[p2[0]][p2[1]]), 2))

def distancia_percorrida(altitudes, lado, caminho):
    distance = 0
    
    for ix in range(1,len(caminho)):
        distance += distancia(altitudes, lado, caminho[ix-1], caminho[ix])
    return distance

def subir_norte(altitudes, inicio):
    
    if ((inicio[0] < len(altitudes)) & ((inicio[0] - 1) >= 0) & (altitudes[inicio[0]][inicio[1]] < altitudes[inicio[0]-1][inicio[1]])):
        return ((inicio[0]-1), inicio[1])

def vizinhas(alturas, celula):    
    Coordenadas = []
    
    #print ((len(alturas) - 1)) 
    #print ((len(alturas[0]) - 1))
    #print (celula[0])
    #print (celula[1])
    
    if ((celula[0] >= 0) & (celula[1] >= 0)):
        #Canto Superior Esquerdo#
        if ((celula[0] == 0) & (celula[1] == 0)):                                                            
            ix_inicio = 0
            ix_fim    = 2
            iy_inicio = 0
            iy_fim    = 2
        
        #Canto Superior Direito#    
        elif ((celula[0] == 0) & (celula[1] == (len(alturas[0]) - 1))):                                       
            ix_inicio = 0
            ix_fim    = 2
            iy_inicio = (len(alturas[0]) - 2)
            iy_fim    = len(alturas[0])
              
        #Limite Superior#      
        elif ((celula[0] == 0) & ((celula[1] != 0) | (celula[1] != (len(alturas[0]) - 1)))):                  
            ix_inicio = 0
            ix_fim    = 2
            iy_inicio = (celula[1]-1)
            iy_fim    = (celula[1]+2)
            
        #Canto Inferior Esquerdo#                
        elif ((celula[0] == (len(alturas) - 1)) & (celula[1] == 0)):                                          
            ix_inicio = (len(alturas)-2)
            ix_fim    = len(alturas)
            iy_inicio = 0
            iy_fim    = 2
        
        #Limite Esquerdo#    
        elif (((celula[0] != 0) | (celula[0] != (len(alturas) - 1))) & (celula[1] == 0)):                     
            ix_inicio = (celula[0]-1)
            ix_fim    = (celula[0]+2)
            iy_inicio = 0
            iy_fim    = 2
        
        #Canto Inferior Direto#                        
        elif ((celula[0] == (len(alturas) - 1)) & (celula[1] == (len(alturas[0]) - 1))):                      
            ix_inicio = (len(alturas)-2)
            ix_fim    = len(alturas)
            iy_inicio = (len(alturas[0])-2)
            iy_fim    = len(alturas[0])
        
        #Limite Inferior#
        elif ((celula[0] == (len(alturas) - 1)) & ((celula[1] != 0) | (celula[1] != (len(alturas[0]) - 1)))):
            ix_inicio = (celula[0]-1)
            ix_fim    = (celula[0]+1)
            iy_inicio = (celula[1]-1)
            iy_fim    = (celula[1]+2)
        
        #Limite Direito#
        elif (((celula[0] != 0) | (celula[0] != (len(alturas) - 1))) & (celula[1] == (len(alturas[0]) - 1))):
            ix_inicio = (celula[0]-1)
            ix_fim    = (celula[0]+2)
            iy_inicio = (len(alturas[0])-2)
            iy_fim    = len(alturas[0])

        #Interior#
        else:   
            ix_inicio = (celula[0]-1)
            ix_fim    = (celula[0]+2)
            iy_inicio = (celula[1]-1)
            iy_fim    = (celula[1]+2)

        for ix in range(ix_inicio, ix_fim):
                for iy in range(iy_inicio, iy_fim):
                    if ((ix == celula[0]) & (iy == celula[1])):
                        continue
                    else:
                        Coordenadas.append((ix, iy))  
                        
                        #print (ix)
                        #print (iy)                                               
    return Coordenadas

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
