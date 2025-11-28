from nltk.tree import Tree

class Patron:
    def __clasificacion_interna(self, elem):# A partir de un árbol retorna una lista de sinónimos (si están disponibles) o en su defecto el ngrama de cada uno de los símbolos terminales
        if isinstance(elem, Tree):
           if len(elem) == 1 and isinstance(elem[0], Tree):
                return self.__clasificacion_interna(elem[0])
           elif len(elem) == 2 and str(elem.label()) == 'NO_ACCION' and isinstance(elem[1], Tree):
                return self.__clasificacion_interna(elem[1])
        categoria = str(elem.label())
        if categoria[0] == '_':# Es sinónimo
            return categoria
        componente = ' '.join([str(i[0]) for i in elem.pos()])# Concatenar ngrama
        return componente


    def __set_componentes_clas(self):# Asigna los componentes ente, enfermedad, influir, accion (en caso de haberlos) para poder realizar la comparación con otro patrón
        componentes = {}
        for i in self.arbol_:
            t = str(i.label())
            if t == 'ENFERMEDAD':
                componentes['enfermedad'] = i
            elif t == 'OBJETO' or t == 'MEDICAMENTO':
                componentes['ente'] = i
            elif t == 'ACCION' or t == 'NO_ACCION':
                t2 = str((i[0] if t == 'ACCION' else i[1][0]).label())
                if t2 == 'COMBATIR' or t2 == 'PROPICIAR':
                    componentes['influir'] = i
                else:
                    componentes['accion'] = i
        for k in ['enfermedad', 'ente', 'accion', 'influir']:
            if k not in componentes:
                componentes[k] = None
        self.componentes_clas = componentes
    

    def __preparar_comparacion(self):
        self.caso_cmp = -1
        id = self.id()
        cmp = self.componentes_clas
        if id < 9 and 'influir' in cmp:# SOLO SE PUEDEN OBTENER PATRONES EQUIVALENTES SI EL ID DEL PATRÓN ES MENOR A 9 Y EL COMPONENTE 'influir' ESTÁ PRESENTE
            es_objeto = str(cmp['ente'].label()) == 'OBJETO'
            # SE OBTIENEN 4 EQUIVALENCIAS SI LA ACCION SE REFIERE EXPLICITAMENTE A UN SINONIMO DE "_USAR" O SI LA ACCION "_USAR" VIENE IMPLICITA MEDIANTE LOS PATRONES 3, 4
            # SE OBTIENEN 2 EQUIVALENCIAS SI LA ACCION PERTENECE A LA CATEGORIA "OTRA_ACCION"
            if es_objeto:
                if cmp['accion'] != None:
                    t_accion = str((cmp['accion'][0] if str(cmp['accion'].label()) == 'ACCION' else cmp['accion'][1][0]).label())
                    if t_accion == 'OTRA_ACCION':
                        self.caso_cmp = 1
                    elif self.__clasificacion_interna(cmp['accion']) == '_USAR':
                        self.caso_cmp = 2
                else:
                    if id in [3, 4]:
                        cmp['accion'] = '_USAR'
                        self.caso_cmp = 2
            else:# SE OBTIENEN HASTA 4 EQUIVALENCIAS SI LA ACCION HACE REFERENCIA A "[_TOMAR, _COMER, _USAR] = _ADMINISTRAR" UN MEDICAMENTO
                administrar = ['_USAR', '_TOMAR', '_COMER']
                if cmp['accion'] == None:
                    cmp['accion'] = '_USAR'
                    self.caso_cmp = 3
                else:
                    if self.__clasificacion_interna(cmp['accion']) in administrar:
                        self.caso_cmp = 3
                    else:
                        self.caso_cmp = 4
            for k in cmp:
                if isinstance(cmp[k], Tree):
                    cmp[k] = self.__clasificacion_interna(cmp[k])
            self.componentes_clas = cmp
        
        if self.caso_cmp == -1:
            self.componentes_cmp_ = [self.__clasificacion_interna(i) for i in self.arbol_]


    def comparar(self, otro, modo_estricto=True):
        print('--------------------------------------------------------------------------------------------------------------')
        print('COMPARAR:')
        self.imprimir()
        print('\n')
        otro.imprimir()
        
        # Realiza una comparación exacta como si fueran 2 strings
        if self.caso_cmp == -1 and otro.caso_cmp == -1:
            if len(self.componentes_cmp_) == len(otro.componentes_cmp):
                for i in range(len(self.componentes_cmp_)):
                    if self.componentes_cmp_[i] != otro.componentes_cmp[i]:
                        return False
                return True
            return False
        # Compara 2 patrones que son del mismo id de comparación
        # También prosigue si ambos patrones tienen definido el diccionario self.componentes_clas y el modo estricto está desactivado
        elif otro.caso_cmp == self.caso_cmp or (not modo_estricto and self.componentes_clas['influir'] is not None):
            for k in self.componentes_clas:
                if not modo_estricto and k == 'accion':
                    continue
                if self.componentes_clas[k] != otro.componentes_clas[k]:
                    return False
            return True
        return False
    

    def __init__(self, arbol, index_inicio, index_fin):        
        self.arbol_  = arbol
        self.index_inicio_ = index_inicio
        self.index_fin_ = index_fin
        self.index_inicio_parrafo_ = None
        self.index_fin_parrafo_ = None
        self.componentes_cmp_ = None
        self.es_contradiccion_ = None
        self.__set_componentes_clas()
        self.__preparar_comparacion()
   

    def __str__(self):
        return str(self.arbol_)


    def imprimir(self):
        Tree.fromstring(str(self.arbol_)).pretty_print()


    def titulo(self):
        return self.arbol_.label()
   

    def id(self):
        return int(self.arbol_.label()[6:7])
    
    
    def es_contradiccion(self):
        return self.arbol_.label().find('NEGADO') != -1


    def arbol(self):
        return self.arbol_


    def terminales(self):
        return self.arbol_.pos()


    def set_index_inicio(self, index):
        self.index_inicio_ = index


    def set_index_fin(self, index):
        self.index_fin_ = index


    def index_inicio(self):
        return self.index_inicio_


    def index_fin(self):
        return self.index_fin_
    
    def set_index_inicio_parrafo(self, index):
        self.index_inicio_parrafo_ = index


    def set_index_fin_parrafo(self, index):
        self.index_fin_parrafo_ = index


    def index_inicio_parrafo(self):
        return self.index_inicio_parrafo_


    def index_fin_parrafo(self):
        return self.index_fin_parrafo_