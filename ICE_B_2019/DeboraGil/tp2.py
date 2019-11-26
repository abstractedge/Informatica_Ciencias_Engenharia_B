tp2.py
A
A
F
J
Type
Text
Size
6 KB (6,311 bytes)
Storage used
6 KB (6,311 bytes)
Location
Débora Gil
Owner
me
Modified
Jun 4, 2019 by me
Opened
Sep 1, 2019 by me
Created
Jun 24, 2019
Add a description
Viewers can download

# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:11:09 2019

@author: Beatriz  e Débora Gil
"""
import sqlite3
import numpy as np
import matplotlib.pyplot as plt


"""
Funcao base_dados
A função retorna uma ligação "conn", passada pelo parâmetro de entrada "database". Caso haja alguma existente, esta é fechada. 
"""
def base_dados(basedados,ligacao_ativa):

    
    if ligacao_ativa!=None:
        ligacao_ativa.close()
    print('*'+basedados+'*') 
    conexao = sqlite3.connect(basedados)
    return conexao


"""
Funcao criar_tabelas
A funcao está responsável por criar duas tabelas na base de dados nomeBD, a tabela compostos e a tabela atributos.
"""
def criar_tabelas(nomeBD):
 
    
    try:
        cursor=nomeBD.cursor()
        cursor.execute('CREATE TABLE Compostos (Identificador_compostos INT, nome_composto TEXT,'+\
                       'formula_quimica_composto TEXT, ponto_ebulicao REAL, PRIMARY KEY(Identificador_compostos));')
        cursor.execute('CREATE TABLE Atributos (Identificador_atributo INT, Identificador_composto INT, atributo TEXT, PRIMARY KEY(Identificador_atributo));')
        nomeBD.commit()
    except:
        print('Erro a criar tabela!')
        
        
"""
Funcao carregar
Esta funcao le um ficheiro com o nome indicado e carrega a informacao para as tabelas da base de dados nomeBD
"""        
def carregar(ficheiro,nomeBD):

    
    linhas = open(ficheiro).readlines()
    cursor = nomeBD.cursor()

    try:
        sql_compostos = 'INSERT INTO Compostos VALUES ({0}, "{1}", {2}, {3});'
        sql_compostos = sql_compostos.format(linhas[0].strip(),linhas[1].strip(),linhas[2].strip(),linhas[3].strip())
        cursor.execute(sql_compostos)
        nomeBD.commit()
    except:
        print('Erro na ',linhas)
     
     
    for linha in linhas[4:]:
         try:
             atributo = linha.strip().split(';')
             sql_atributos = 'INSERT INTO Atributos VALUES ( "{0}", "{1}", {2}, {3});'
             """sql_atributos = sql_atributos.format(amostra[0].strip(),linhas[0].strip(),amostra[1].strip(),amostra[2].strip()) VERIFICAR ESTA LINHA DE CODIGO"""
             cursor.execute(sql_atributos)
             nomeBD.commit()
         except:
             print('Erro na ',linha)
 
            
"""
Funcao reportar
Esta funcao cria um ficheiro texto "relatorio". Caso exista algum aberto, este é fechado.  
"""             
def reportar(objeto,relatorio):

    
    if relatorio!=None:
        relatorio.close()
        
    ficheiro_open = open(objeto,'w')
    return ficheiro_open


def lista():


"""
Funcao query_baseDados
Funcao que devolve uma lista de dicionarios
"""
def query_baseDados(nomeBD, query):

    cursor = nomeBD.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print(len(records))
    result = []
    for record in records:
        dicionario={}

        for ix in range(len(record)):
            dicionario[cursor.description[ix][0]]=record[ix]
        result.append(dicionario)
    return result  


"""
Funcao grafico
Funcao que recebe os valores de x e de y, colocando-os no grafico. 
Calculo da regressao linear.
"""
def grafico(nome_ficheiro, nomeBD, nome_atributo):

    eixo_x = x(nome_atributo, nomeBD)
    eixo_y = y(nome_atrituto, nomeBD)
    plt.plot(eixo_x, eixo_y,'k.')
    plt.title('Atributo:{0}'.format(nome_atributo))
    plt.xlabel('Logaritmo do número de átomos de Carbono')
    plt.ylabel('Ponto de ebulição, ºC')
    eixo_x = np.array(eixo_x)
    Beta = beta(eixo_x, eixo_y)
    plt.plot(eixo_x, (alpha(eixo_x, eixo_y, Beta) + (Beta*eixo_x)))
    plt.savefig('ficheiro.png') 
    plt.close()
  

def beta(eixo_x,eixo_y):
    """
    Calculo do parametro beta, atraves da formula fornecida no enunciado.
    """
    xAvg = 0
    yAvg = 0
    somatorio_x_xAvg = 0
    somatorio_y_yAvg = 0
    somatorio_x_xAvg_squared = 0
    
    for ix in range(len(eixo_x)):
        xAvg += eixo_x[ix]   
    xAvg = xAvg/len(eixo_x)
    
    for iy in range(len(eixo_y)):
        yAvg += eixo_y[iy]    
    yAvg = yAvg/len(eixo_y)
    
    for ix in range(len(eixo_x)):
        somatorio_x_xAvg += (eixo_x[ix] - xAvg)
        somatorio_x_xAvg_squared += (eixo_x[ix] - xAvg)**2
        
    for iy in range(len(eixo_y)):
        somatorio_y_yAvg += (eixo_y[iy] - yAvg) 
        
    beta = ((somatorio_x_xAvg*somatorio_y_yAvg)/somatorio_x_xAvg_squared)
    return beta

def alpha(eixo_x,eixo_y, beta):
    """
    Calculo do parametro beta, atraves da formula fornecida no enunciado.
    """
    xTotal = 0
    yTotal = 0
    N = 0
    
    for ix in range(len(eixo_x)):
        xTotal += eixo_x[ix]   
    
    for iy in range(len(eixo_y)):
        yTotal += eixo_y[iy]    
        
    alpha = ((yTotal/N) - beta*(xTotal/N))
    return alpha



"""
Funcao processar
Funcao que recebe o nome do ficheiro de texto com as instrucoes de processamento, fornecidas pelos investigadores. 
A funcao le e executa os comandos descritos nesse ficheiro.
"""
def processar(ficheiro):

    teste=open(ficheiro).readlines()
    baseDados=None
    relatorio=None
    for line in teste:
        
        if ' ' in line:
           comando,argumento=line.strip().split(' ')
        else: 
            comando=line.strip()
            
        if comando   == 'BASE_DADOS':
             print(argumento)
             baseDados = base_dados(argumento, baseDados)  
             
        elif comando == 'CRIAR_TABELAS':
             criar_tabelas(base_dados)  
             
        elif comando == 'CARREGAR':
             carregar(argumento, baseDados)
             
        elif comando == 'REPORT':
             relatorio = reportar(argumento, relatorio)
             
        elif comando == 'LISTA':
             formula_empirica,atributo = argumento.strip().split(';')
             lista(relatorio, basedados, formula_empirica, atributo)
             
        elif comando == 'GRAFICO':
             nome_ficheiro, nome_atributo = argumento.strip().split(';')  
             grafico(relatorio, baseDados, nome_atributo)
             
    baseDados.close()
    relatorio.close() 
