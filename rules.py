# -*- encoding: utf-8 -*-

class Rules:
    """ Aplica las reglas del juego"""

    def __init__(self, raizMain, table, checker):
        self.raizMain = raizMain
        self.table = table
        self.checker = checker


    def manejador(self):
        """Controlador de las acciones a realizar, se encarga de
        ejecutar los pasos necesarios, reglas """

        raizPlain = self._arma_raiz(self.raizMain)
        if raizPlain:
            print "Lista Raiz COMEN: ", raizPlain
            wayJump = self._arma_camino(raizPlain)
            #print "Camino COMPLETO: ", wayJump
            
        else:
            print "NO COME NINGUNA"
        
    def _arma_raiz(self, listaMain):
        """Arma una lista  con los diccionarios de las fichas 
        que pueden comer, cada raiz en una lista"""
        listaPlain =[]
        for lista in listaMain:
            for dic in lista:
                listaPlain.append(dic)
         
        return listaPlain

    def _arma_camino(self, raiz):
        """Arma el camino para cada ficha que puede comer """
        way = []
        original_position = self.checker.position
        print "---------------------------------"
        for dic in raiz:
            #voy armando la lista con el camino por cada raiz
            destino = dic['destination'] 
            tempWay = []
            tempWay.append(dic)
            print "--- armando camino para Ficha:", dic['checker']
            lista = self._search_jump(destino)
            
            if len(lista) == 2:
                #TODO Pensar como implementar
                print "DEVOLVIO 2"
            elif len(lista) == 1:
                print "devolvio 1"
                tempWay.append(lista[0])
            else:
                print "devolvio -> ", len(lista)

            
            for square_jump in lista: 
                print "ENTROOOOOOOOO!!!!!!!!!"
                print square_jump

            #Siempre agrego la lista, que tiene al menos un diccionario    
            way.append(tempWay)

        print "CAMINO FINAL: ", way
        print "---------------------------------"
        #self.checker.position = original_position
        self.checker.move(original_position)
        return way
    

    def _search_jump(self, position):
        """Verifica si come una ficha, y devuelve los casilleros """
        print "--- verificando jump desde square ", position
        self.checker.move(position)
        tempDic = self.table.forced_jump_one_checker(self.checker)
        print "--- posibles:", tempDic
        print "-- check: ", self.checker
        return tempDic


    def _elige_camino_cc(self, raiz):
        """Elige el camino segun las reglas
        de calidad y cantidad  """
        pass
