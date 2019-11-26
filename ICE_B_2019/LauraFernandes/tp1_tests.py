#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de testes unitários para o TP1
Instruções:
    Pôr este ficheiro na pasta do trabalho prático.
    O módulo principal do trabalho prático tem de ser um ficheiro de nome tp1.py
    Na pasta tem de ter também o ficheiro tp1_data.py
    Premir F5 no Spyder (ou Run) para executar os testes
"""
from importlib import import_module
import numpy as np
from tp1_data import teste, estrela

def test_function(function, tests):
    """
    run all tests on a function
    """    
    results = []
    ix = 1
    for args, target in tests:
        test = function.__name__+', test '+str(ix)
        ix+=1
        try:
            res = function(*args)            
            if np.array_equal(res,target):
                results.append(test+' OK')
            else:
                results.append(test+' Incorrect result')
                print(res)
        except Exception as exception:
            results.append(test+' Exception raised: '+repr(exception))
    print('\n'.join(results))


def test_all(module_name,tests):
    try:
        module = import_module(module_name)       
        for fn,test in tests:
            try:
                function = getattr(module,fn)
                test_function(function,test)
            except:
                print(fn+' not found')
    except:
        print(module_name+'.py not found. Aborting all tests.')

tests = [
        ('distancia',
        [( (teste, 20, (2, 0), (3, 1)), 28.442925306655784),
         ( (teste, 20, (2, 1), (6, 4)), 100.04498987955368),
         ( (teste, 20, (2, 3), (2, 4)), 21.540659228538015),
         ]),    
       ('distancia_percorrida',
        [( (teste, 20, [ (2,0),(3,1),(3,2),(4,3) ]), 76.79781906417143),
         ( (teste, 20, [ (2,2),(3,3),(3,2),(4,2) ]), 69.88764155095805),
         (  (teste, 20, [ ]), 0),
         (  (teste, 20, [ (2,2)]), 0),
          ]),   
       ('subir_norte',
        [( (teste, (3,0) ), (2,0)),
         ( (teste, (1,0) ), (0, 0)),
        ]),
      ('vizinhas',
        [( (teste, (3,3) ),[(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]),
         ( (teste, (5,4) ),[(4, 3), (4, 4), (5, 3), (6, 3), (6, 4)]),
         ( (teste, (0,0) ),[(0, 1), (1, 0), (1, 1)]),
         ( (teste, (-5,-5) ),[]),         
          ]),   
      ('vizinha_mais_alta',
        [( (teste, (5,3) ),(5,4)),
         ( (teste, (1,1) ),(0, 0)),
         ( (teste, (1,2) ),(1, 2)),         
          ]),   
      ('subir_mais_alto',
        [( (teste, (5,3) ),[(5, 3), (5, 4)]),
         ( (teste, (6,1) ),[(6, 1), (5, 2), (4, 3), (3, 3)]),
         ( (teste, (1,0) ),[(1, 0), (0, 0)]),         
          ]),   
        ]
        
print('***** Tests *****')
test_all('tp1',tests)
