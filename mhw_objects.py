import pickle
import os
import requests
import sys
from copy import deepcopy
import json


class database:  # root do banco de dados principal, separado pelos 3 ranks de armadura
    def __init__(self):
        self.master = slots()
        self.high = slots()
        self.low = slots()


class slots:  # cada parametro do root recebe um desses objetos, com os 5 slots equipaveis de armadura
    def __init__(self):
        self.head = linkedlist()
        self.chest = linkedlist()
        self.gloves = linkedlist()
        self.waist = linkedlist()
        self.legs = linkedlist()


class skill_obj:  # objeto que armazena os dados de uma skill, como o nome, id e nivel maximo
    def insert(self, skill):
        self.id = skill.get('id')
        self.name = skill.get('name')
        self.max_lvl = len(skill.get('ranks'))

    def __init__(self):
        self.id = None
        self.name = None
        self.max_lvl = None


class rank_node:  # nodo para a lista de ranks de uma skill, armazenando os dados especificos de cada nivel da skill,
    # e uma lista com as armaduras que contém esse rank

    def insertarmor(self, armor):
        self.armorlist.insert_sorted(armor)

    def insertskill(self, rank):  # função que recebe os dados da api e insere nos elementos apropriados da classe
        self.rankdata = skill_rank()
        self.rankdata.level = rank.get('level')
        self.rankdata.name = rank.get('skillName')
        self.rankdata.skill_id = rank.get('skill')
        if rank.get('modifiers') is not False:
            self.rankdata.modifiers = rank.get('modifiers')
        self.rankdata.desc = rank.get('description')

    def __init__(self):
        self.armorlist = linkedlist()
        self.rankdata = None


class skill_rank:  # objeto que armazena os dados de um rank de uma skill, utilizado na classe acima

    def __init__(self):
        self.name = None
        self.skill_id = None
        self.level = None
        self.desc = None
        self.modifiers = None


class armor_obj:  # objeto que armazena os dados de uma peça de armadura; os elementos de 'skills' são ponteiros para
    # o banco de dados de skills, onde estão os dados de cada skill da armadura

    def insert(self, armor, skill_db):  # função que recebe os dados da api e insere nos elementos apropriados da classe
        self.name = armor.get('name')
        self.id = armor.get('id')
        self.rank = armor.get('rank')
        self.slot = armor.get('type')
        self.defense = armor.get('defense').get('augmented')
        if armor.get('assets') is not None:  # algumas armaduras não tem imagem, essa linha verifica se a armadura
            # atual tem
            if armor.get('assets').get('imageMale') is not None:
                url = armor.get('assets').get('imageMale')  # a resposta da api é uma url https, essa pequena seção
                # separa o link do nome do arquivo, e insere a estrutura de pasta onde a imagem será salva
                url = url[31:]
                img = "assets/img" + url
                self.image = img
        self.fire_res = armor.get('resistances').get('fire')
        self.water_res = armor.get('resistances').get('water')
        self.thunder_res = armor.get('resistances').get('thunder')
        self.ice_res = armor.get('resistances').get('ice')
        self.dragon_res = armor.get('resistances').get('dragon')

        skill_list = armor.get('skills')
        temp_list = []

        for i in range(0, len(skill_list)):  # loop que monta uma lista com ponteiros para cada skill da armadura
            skill_lvl = skill_list[i].get('level') - 1
            skill_data = skill_db.search(skill_list[i].get('skill')).ranks[skill_lvl].rankdata
            temp_list.append(skill_data)
        self.skills = temp_list

    def __init__(self):
        self.name = None
        self.id = None
        self.rank = None
        self.slot = None
        self.defense = None
        self.image = None
        self.fire_res = None
        self.water_res = None
        self.thunder_res = None
        self.ice_res = None
        self.dragon_res = None
        self.skills = None


class linked_node_skill:  # nodo para lista encadeada de skills
    def __init__(self, data):
        self.data = data
        self.ranks = None
        self.next = None


class linked_node_armor:  # nodo para lista encadeada de armaduras
    def __init__(self, data):
        self.data = data
        self.next = None


class linkedlist:  # classe com as funções de lista encadeada, com inserção no final da lista, e inserção ordenada

    def insert_armor(self, data):
        node = linked_node_armor(data)

        if self.head is None:  # verifica se o nodo a ser inserido é o proprio head, insere se for o caso
            self.head = node

        else:
            last = self.head  # percorre a lista até encontrar o proximo lugar vazio para inserir
            while (last.next):
                last = last.next
            last.next = node
        return

    def insert(self, node):

        if self.head is None:
            self.head = node  # este código é igual ao acima, com a unica distinção de que ele não cria o nodo,
            # mas sim recebe como entrada. este funcionamento é necessario para a inserção de skills, que requer um
            # processo mais complicado
        else:
            last = self.head
            while (last.next):
                last = last.next
            last.next = node
        return

    def insert_sorted(self, data):  # inserção ordenada em uma linked list, créditos: ispectorG4dget /
        # https://stackoverflow.com/questions/19217647/sorted-linked-list-in-python
        curr = self.head
        if curr is None:
            n = linked_node_armor(data)
            self.head = n
            return
        if curr.data.defense > data.defense:  # o algoritmo usa o valor de defesa fisica como elemento para o sorting
            n = linked_node_armor(data)
            n.next = curr
            self.head = n
            return

        while curr.next is not None:
            if curr.next.data.defense > data.defense:
                break
            curr = curr.next
        n = linked_node_armor(data)
        n.next = curr.next
        curr.next = n
        return

    def deleteNode(self, id):  # função de deleção de um node especificado numa lista encadeada

        temp = self.head

        if (temp is not None):  # verifica se o nodo atual não é vazio
            if (temp.data.id == id):  # se o nodo head for o especificado, deleta imediatamente e retorna
                self.head = temp.next
                temp = None
                return

        while (temp is not None):  # loop percorrendo até o fim de lista
            if temp.data.id == id:  # quebra o loop quando encontra o elemento especificado
                break
            prev = temp  # avança a lista, mantendo na memoria o nodo anterior
            temp = temp.next

        if (temp == None):  # fim de função caso chege no fim sem encontrar, ou a lista esteja vazia
            return

        prev.next = temp.next  # fim de função caso encontre um nodo não vazio com os dados especificados, remove o
        # nodo da cadeia
        temp = None

    def search(self, id):  # busca de um elemento na lista por id

        current = self.head

        while current != None:  # percorre a lista até o fim
            if current.data.id == id:  # elemento encontrado = retorna o nodo inteiro
                return current

            current = current.next  # avança para o proximo nodo

        return False  # elemento não encontrado

    def __init__(self):
        self.head = None


def downloadarmor(s_list, db):  # função que baixa os dados de armaduras da api
    data = requests.get("https://mhw-db.com/armor/").json()  # armazena os dados em formato dict
    armor_list = linkedlist()  # inicializa a lista encadeada vazia

    for i in range(0, len(data)):  # leitura recursiva de todos os elementos de armadura (1444!)
        temp = armor_obj()  # cria um objeto armadura vazio
        temp.insert((data[i]), s_list)  # insere os dados lidos no objeto armadura
        armor_list.insert_armor(temp)  # insere o objeto na lista de armaduras

        if temp.rank == 'master':  # essa parte faz a verificação de onde na estrutura a armadura pertence
            dest = db.master
        elif temp.rank == 'high':  # primeiro é feita a verificação de rank (master, high ou low)
            dest = db.high
        elif temp.rank == 'low':
            dest = db.low  # o destino da armadura avança com cada passo, já que a estrutura é simétrica,
            # é possivel percorrer 15 possiveis arvores em 8 linhas

        if temp.slot == 'head':
            dest = dest.head
        elif temp.slot == 'chest':  # nesta parte se verifica qual slot a armadura é equipada
            dest = dest.chest
        elif temp.slot == 'gloves':
            dest = dest.gloves
        elif temp.slot == 'waist':
            dest = dest.waist
        elif temp.slot == 'legs':
            dest = dest.legs

        armorskills = data[i].get('skills')  # lê a lista de skills da armadura
        if armorskills:  # verifica se essa lista é vazia (alguns itens não tem skills)
            for j in range(0,len(armorskills)):
                level = armorskills[j].get('level') - 1 # determina o rank a ser inserido
                dest.search(armorskills[j].get('skill')).ranks[level].armorlist.insert_armor(temp) # insere o rank da
                # skill na lista da armadura

        temp = None
    return armor_list  # retorna a lista de armaduras a main


def downloadskill(db):  # download dos dados de skills da api
    data = requests.get("https://mhw-db.com/skills/").json()

    mhead = db.master.head
    mchest = db.master.chest  # essa parte inicializa diversas variaveis com os nodos da estrutura com listas de skills
    mgloves = db.master.gloves
    mwaist = db.master.waist  # cada slot de cada rank tem uma lista com todas as skills (porém os dados são
    mlegs = db.master.legs  # referenciados, não há informação redundante)

    hhead = db.high.head
    hchest = db.high.chest
    hgloves = db.high.gloves
    hwaist = db.high.waist
    hlegs = db.high.legs

    lhead = db.low.head
    lchest = db.low.chest
    lgloves = db.low.gloves
    lwaist = db.low.waist
    llegs = db.low.legs

    slot_l = list(
        [mhead, mchest, mgloves, mwaist, mlegs, hhead, hchest, hgloves, hwaist, hlegs, lhead, lchest, lgloves, lwaist,
         llegs])  # lista com os slots para facilitar rodar o código recursivamente em todos

    list_s = linkedlist()  # inicializa a lista de skills vazia

    for i in range(0, len(data)):  # lê recursivamente cada dado de skill da api (aproximadamente 160 skills distintas)
        temp = skill_obj()  # inicializa objeto skill vazio, e insere os dados lidos
        temp.insert((data[i]))
        node = linked_node_skill(temp)  # criação de nodo para inserção na lista encadeada
        rank_list = data[i].get('ranks')
        temp_list = []

        # essa parte pega os ranks de cada skill (são guardados em um array no dict), e monta uma lista
        # com referencias para cada rank

        for j in range(0, len(rank_list)):
            temp = rank_node()
            temp.insertskill(rank_list[j])
            temp_list.append(temp)
            temp = None

        # insere a lista terminada no elemento ranks do objeto skill, e insere o nodo criado na lista encadeada
        node.ranks = temp_list
        list_s.insert(node)

        for element in slot_l:
            node2 = linked_node_skill(node)
            node2.data = node.data
            node2.next = deepcopy(None)
            node2.ranks = deepcopy(temp_list)
            element.insert(node2)
            node2 = None

        ''' para evitar com que cada lista de armaduras seja uma copia da outra, por fim criando apenas uma lista enorme
        é criado uma instancia do objeto para cada lista onde é inserido. Porém, os dados são mantidos como
        referencia, pois esses não serão editados separadamente, e precisam manter a consistência. é utilizada a
        função deepcopy para criar a nova instância, da library padrão copy. o elemento instanciado é então
        inserido na lista, e o processo se repete 15 vezes; 5 para para cada rank, uma para cada slot. '''

        node = None
        node2 = None
        temp = None
        return list_s, db


def rebuild_database():
    s_list, db = downloadskill(database())
    a_list = downloadarmor(s_list, db)

    '''função que recria o banco de dados local, utilizando as funções acima.
    os resultados são salvos em arquivos binarios serializados, utilizado a biblioteca Pickle.'''

    s_file = open('assets/skill_list.bin', 'wb')
    a_file = open('assets/armor_list.bin', 'wb')
    db_file = open('assets/database.bin', 'wb')

    pickle.dump(s_list, s_file)
    pickle.dump(a_list, a_file)
    pickle.dump(db, db_file)
    s_file.close()
    a_file.close()
    db_file.close()

    return s_list, a_list, db


def main():
    sys.setrecursionlimit(9000)  # foi necessario elevar o limite de recursões, devido a complexidade da estrutura
    path = "assets/img"  # simples estrutura de pastas que é checada e criada se necessario

    if os.path.isdir(path) == False:
        try:
            os.makedirs(path)  # verifica se a estrutura de pastas atualmente existe, se falhar tenta criar
        except OSError as exc:
            if exc.errno != errno.EEXIST:  # tratamento de erro onde não foi possivel criar a pasta, programa falha
                raise
            pass
    if os.path.isdir(path) == True:
        if os.path.isfile('assets/skill_list.bin') is not True:  # verifica se os arquivos necessarios existem
            skill_list, armor_list, db = rebuild_database()
        if os.path.isfile('assets/armor_list.bin') is not True:  # caso um sequer não exista, é necessario reconstruir o banco de dados inteiro
            skill_list, armor_list, db = rebuild_database()
        if os.path.isfile('assets/database.bin') is not True:
            skill_list, armor_list, db = rebuild_database()

        s_file = open('assets/skill_list.bin', 'rb')
        a_file = open('assets/armor_list.bin', 'rb')
        db_file = open('assets/database.bin', 'rb')

        skill_list = pickle.load(s_file)  # carga das estruturas criadas previamente em execuções futuras
        armor_list = pickle.load(a_file)  # o tempo de processamento quando os dados são carregados do disco é exponencialmente menor
        db = pickle.load(db_file)

        s_file.close()
        a_file.close()
        db_file.close()

        '''DRIVER CODE PRA TESTAR AS ESTRUTURAS
        como pesquisar:
        mude a estrutura do argumento na função vars para o rank desejado, o slot desejado, 
        insira o id de skill desejado, 
        e o nivel de skill desejado no atributo "ranks" (nota: arrays começam do zero)
        
        exemplo:
        quero uma chestpiece de rank high com a skill de numero 100 no rank 3
        db.high.chest.search(100).ranks[2].armorlist = LISTA DE ARMADURAS QUE CAEM NESSES CRITERIOS
        para percorrer a lista, adicione .head e depois .nextno final
        ou seja, primeiro elemento: armorlist.head ; segundo elemento: armorlist.head.next, 
        terceiro elemento: armorlist.head.next.next ; etc...
        para acessar os dados do elemento selecionado. adicione .data
        
        ouseja, para acessar os dados do primeiro elemento na busca acima:
        db.high.chest.search(100).ranks[2].armorlist.head.data'''


        print("\nsearching for low rank headgears with the hunger resist skill @ level 1")
        attrs = vars(db.low.head.search(67)) # MUDE A BUSCA AQUI E EM TODAS AS OUTRAS LINHAS PROGRESSIVAMENTE
        print(''.join("%s: %s\n" % item for item in attrs.items()))
        print("inside 'ranks' :")
        attrs = vars(db.low.head.search(67).ranks[0])
        print(''.join("%s: %s\n" % item for item in attrs.items()))
        print("inside 'armorlist' :")
        attrs = vars(db.low.head.search(67).ranks[0].armorlist)
        print(''.join("%s: %s\n" % item for item in attrs.items()))
        print("first item data: ")
        attrs = vars(db.low.head.search(67).ranks[0].armorlist.head.data)
        print(''.join("%s: %s\n" % item for item in attrs.items()))


if __name__ == '__main__':
    main()
