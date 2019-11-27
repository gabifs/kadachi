import pickle
import os
import requests
import sys
from copy import deepcopy
import errno
import json

class armorset:

    def insertarmor(self,armor):
        if armor.slot == 'head':
            self.head = armor
        elif armor.slot == 'chest':
            self.chest = armor
        elif armor.slot == 'gloves':
            self.gloves = armor
        elif armor.slot == 'waist':
            self.waist = armor
        elif armor.slot == 'legs':
            self.legs = armor

    def get_max(self, ll, slot, rank):
        if ll.next is None:
            return ll.data
        else:
            tail_max = self.get_max(ll.next, slot, rank)
            if tail_max is not None:
                if ll.data.defense > tail_max.defense and ll.data.slot == slot and ll.data.rank == rank:
                    return ll.data
                elif tail_max.slot == slot:
                        return tail_max
            else:
                return None

    def autocomplete(self,armor_list,rank):
        if self.head is None:
            self.head = armor_list.get_max_arm('head', rank)

        if self.chest is None:
            self.chest = armor_list.get_max_arm('chest', rank)

        if self.gloves is None:
            self.gloves = armor_list.get_max_arm('gloves', rank)

        if self.waist is None:
            self.waist = armor_list.get_max_arm('waist', rank)

        if self.legs is None:
            self.legs = armor_list.get_max_arm('legs', rank)

        else:
            return

    def __init__(self):
        self.head = None
        self.chest = None
        self.gloves = None
        self.waist = None
        self.legs = None

class player:

    def get_def_sum(self):
        sum = 0
        if self.head is not None:
            if isinstance(self.head.defense, int):
                sum = sum + self.head.defense
        if self.chest is not None:
            if isinstance(self.chest.defense, int):
                sum = sum + self.chest.defense
        if self.gloves is not None:
            if isinstance(self.gloves.defense, int):
                sum = sum + self.gloves.defense
        if self.waist is not None:
            if isinstance(self.waist.defense, int):
                sum = sum + self.waist.defense
        if self.legs is not None:
            if isinstance(self.legs.defense, int):
                sum = sum + self.legs.defense

        return sum

    def get_res(self):
        fire = 0
        water = 0
        thunder = 0
        ice = 0
        dragon = 0

        if self.head is not None:
            fire = fire + self.head.fire_res
            water = water + self.head.water_res
            thunder = thunder + self.head.thunder_res
            ice = ice + self.head.ice_res
            dragon = dragon + self.head.dragon_res
        if self.chest is not None:
            fire = fire + self.chest.fire_res
            water = water + self.chest.water_res
            thunder = thunder + self.chest.thunder_res
            ice = ice + self.chest.ice_res
            dragon = dragon + self.chest.dragon_res
        if self.gloves is not None:
            fire = fire + self.gloves.fire_res
            water = water + self.gloves.water_res
            thunder = thunder + self.gloves.thunder_res
            ice = ice + self.gloves.ice_res
            dragon = dragon + self.gloves.dragon_res
        if self.waist is not None:
            fire = fire + self.waist.fire_res
            water = water + self.waist.water_res
            thunder = thunder + self.waist.thunder_res
            ice = ice + self.waist.ice_res
            dragon = dragon + self.waist.dragon_res
        if self.legs is not None:
            fire = fire + self.legs.fire_res
            water = water + self.legs.water_res
            thunder = thunder + self.legs.thunder_res
            ice = ice + self.legs.ice_res
            dragon = dragon + self.legs.dragon_res

        return fire, water, thunder, ice, dragon


    def get_skills(self,skill_list):

        head = self.head
        chest = self.chest
        gloves = self.gloves
        waist = self.waist
        legs = self.legs

        slot_list = list([head,chest,gloves,waist,legs])

        for element in slot_list:
            added = False
            if element is not None:
                if element.skills:
                    for i in range(0,len(element.skills)):
                        for j in range(0,len(self.skills)):
                            if self.skills[j].skill_id == element.skills[i].skill_id:
                                combined_lvl = self.skills[j].level + element.skills[i].level
                                if len(skill_list.search(self.skills[j].skill_id).ranks) >= combined_lvl-1:
                                    temp = skill_list.search(self.skills[j].skill_id).ranks[combined_lvl-1]
                                    self.skills[j] = temp.rankdata
                                added = True
                            break
                        if added == False:
                            self.skills.append((element.skills[i]))


        return


    def buildplayer(self,set,skill_list):

        self.head = set.head
        self.chest = set.chest
        self.gloves = set.gloves
        self.waist = set.waist
        self.legs = set.legs
        self.defense = self.get_def_sum()
        self.fire_res,self.water_res,self.thunder_res,self.ice_res,self.dragon_res = self.get_res()
        self.get_skills(skill_list)


    def __init__(self):
        self.head = None
        self.chest = None
        self.gloves = None
        self.waist = None
        self.legs = None
        self.defense = 0
        self.fire_res = 0
        self.water_res = 0
        self.thunder_res = 0
        self.ice_res = 0
        self.dragon_res = 0
        self.skills = []

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

    def insertskill(self, rank, desc):  # função que recebe os dados da api e insere nos elementos apropriados da classe

        self.rankdata = skill_rank()
        self.rankdata.level = rank.get('level')
        self.rankdata.name = rank.get('skillName')
        self.rankdata.skill_id = rank.get('skill')
        self.rankdata.description = desc
        if rank.get('modifiers') is not False:
            self.rankdata.modifiers = rank.get('modifiers')
        self.rankdata.effects = rank.get('description')

    def __init__(self):
        self.armorlist = linkedlist()
        self.rankdata = None


class skill_rank:  # objeto que armazena os dados de um rank de uma skill, utilizado na classe acima

    def __init__(self):
        self.name = None
        self.skill_id = None
        self.level = None
        self.description = None
        self.effects = None
        self.modifiers = None


class armor_obj:  # objeto que armazena os dados de uma peça de armadura; os elementos de 'skills' são ponteiros para
    # o banco de dados de skills, onde estão os dados de cada skill da armadura

    def insert_manually(self, armor, skill_db,armorlist):
        self.name = armor.get('name')

        node = armorlist.head
        while node.next is not None:
            node = node.next
        self.id = node.data.id + 1
        self.rank = armor.get('rank')
        self.slot = armor.get('slot')
        self.defense = armor.get('defense')
        url = 'https://cdn.discordapp.com/attachments/406499527516749844/648968553910894689/unknown.png'
        url = url[39:]
        url = url.replace("/", ".", 2)
        img = "assets/img/" + url
        self.image = img
        self.fire_res = 0
        self.water_res = 0
        self.thunder_res = 0
        self.ice_res = 0
        self.dragon_res = 0
        temp_list = []

        skill_lvl = armor.get('level') - 1
        if not isinstance(skill_db.search_name(armor.get('skill')), bool):
            skill_data = skill_db.search_name(armor.get('skill')).ranks[skill_lvl].rankdata
            temp_list.append(skill_data)
        self.skills = temp_list
        self.custom = True

    def insert(self, armor, skill_db):  # função que recebe os dados da api e insere nos elementos apropriados da classe
        self.name = armor.get('name')
        self.id = armor.get('id')
        self.rank = armor.get('rank')
        self.slot = armor.get('type')
        #self.defense = armor.get('defense').get('augmented')
        self.defense = max(armor.get('defense').get('augmented'), armor.get('defense').get('base'))

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
            if not isinstance(skill_db.search(skill_list[i].get('skill')), bool):
                skill_data = skill_db.search(skill_list[i].get('skill')).ranks[skill_lvl].rankdata
                temp_list.append(skill_data)
        self.skills = temp_list
        self.custom = False

    def __init__(self):
        self.name = None
        self.id = None
        self.rank = None
        self.slot = None
        self.defense = 0
        self.image = None
        self.fire_res = 0
        self.water_res = 0
        self.thunder_res = 0
        self.ice_res = 0
        self.dragon_res = 0
        self.skills = 0
        self.custom = None


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

    def get_max_arm(self, slot, rank):
        node = self.head
        largest = linked_node_armor(armor_obj())
        while node.next is not None:
            if node.data.defense > largest.data.defense and node.data.slot == slot and node.data.rank == rank:
                largest = node
            node = node.next
        return largest.data

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

    def deleteNode(self, name):  # função de deleção de um node especificado numa lista encadeada

        temp = self.head

        if (temp is not None):  # verifica se o nodo atual não é vazio
            if (temp.data.name == name):  # se o nodo head for o especificado, deleta imediatamente e retorna
                self.head = temp.next
                temp = None
                return

        while (temp is not None):  # loop percorrendo até o fim de lista
            if temp.data.name == name:  # quebra o loop quando encontra o elemento especificado
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

    def search_name(self, name):  # busca de um elemento na lista por nome

        current = self.head

        while current != None:  # percorre a lista até o fim
            if current.data.name == name:  # elemento encontrado = retorna o nodo inteiro
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

    slot_l = list([mhead, mchest, mgloves, mwaist, mlegs, hhead, hchest, hgloves, hwaist, hlegs, lhead, lchest, lgloves, lwaist, llegs])  # lista com os slots para facilitar rodar o código recursivamente em todos

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
            temp.insertskill(rank_list[j],data[i].get('description'))
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

        node = None
        node2 = None
        temp = None

    return list_s, db


def rebuild_database():
    print("Downloading Skill Data from API")
    print("Initializing Database")
    s_list, db = downloadskill(database())
    print("Downloading Armor Data from API")
    print("Indexing Skill Data")
    a_list = downloadarmor(s_list, db)
    print("DONE")



    '''função que recria o banco de dados local, utilizando as funções acima.
    os resultados são salvos em arquivos binarios serializados, utilizado a biblioteca Pickle.'''

    print("Creating Local Files")
    s_file = open('assets/skill_list.bin', 'wb')
    a_file = open('assets/armor_list.bin', 'wb')
    db_file = open('assets/database.bin', 'wb')

    print("Serializing Database")
    pickle.dump(s_list, s_file)
    pickle.dump(a_list, a_file)
    pickle.dump(db, db_file)
    s_file.close()
    a_file.close()
    db_file.close()
    print("DONE")

    print("Database Updated")

    return s_list, a_list, db

def makeset(sklname,rank,autoc,db,armor_list, s_list, player):
    set = armorset()

    if rank == 'low':
        dest = db.low
    elif rank == 'high':
        dest = db.high
    elif rank == 'master':
        dest = db.master

    headlist = dest.head
    chestlist = dest.chest
    glovelist = dest.gloves
    waistlist = dest.waist
    leglist = dest.legs

    slot_l = list([headlist, chestlist, glovelist, waistlist, leglist])
    max_lvl = headlist.search_name(sklname).data.max_lvl
    for element in slot_l:
        found_skill = element.search_name(sklname)

        found = False
        current_lvl = max_lvl
        expected_lvl = max_lvl
        while found is False:
            if len(found_skill.ranks) >= current_lvl-1:
                dest = found_skill.ranks[current_lvl-1].armorlist

                if dest.head is not None:
                    if dest.head.data.slot == 'head':
                        set.head = dest.head.data
                    if dest.head.data.slot == 'chest':
                        set.chest = dest.head.data
                    if dest.head.data.slot == 'gloves':
                        set.gloves = dest.head.data
                    if dest.head.data.slot == 'waist':
                        set.waist = dest.head.data
                    if dest.head.data.slot == 'legs':
                        set.legs = dest.head.data
                    max_lvl = max_lvl - current_lvl
                    found = True
                    break
                current_lvl = current_lvl - 1
            if current_lvl == 0:
                break

        if max_lvl <= 0:
            break
    if autoc == True:
        set.autocomplete(armor_list, rank)

    actual_level = expected_lvl - max_lvl
    if actual_level != expected_lvl:
        found = 0
    else:
        found = 1

    return set,found

def additem(db,armorlist,s_list,itemname,itemdef,itemrank,skillname,skillrank,slot):

    item = dict({'name': itemname, 'defense': itemdef, 'skill': skillname, 'level': skillrank+1, 'slot': slot, 'rank': itemrank})
    temp = armor_obj()  # cria um objeto armadura vazio
    temp.insert_manually(item, s_list,armorlist)  # insere os dados lidos no objeto armadura
    armorlist.insert_armor(temp)  # insere o objeto na lista de armaduras

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

    if skillname is not 'None':  # verifica se essa lista é vazia (alguns itens não tem skills)
            dest.search_name(skillname).ranks[skillrank].armorlist.insert_armor(temp)  # insere o rank da
            # skill na lista da armadura

    s_file = open('assets/skill_list.bin', 'wb')
    a_file = open('assets/armor_list.bin', 'wb')
    db_file = open('assets/database.bin', 'wb')

    pickle.dump(s_list, s_file)
    pickle.dump(armorlist, a_file)
    pickle.dump(db, db_file)
    s_file.close()
    a_file.close()
    db_file.close()

    print("Item Added")

    return

def removeitem(itemname,db, armorlist,s_list):

    temp = armorlist.search_name(itemname)
    if temp is not False:
        temp = temp.data

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

        for i in range(0,len(temp.skills)):
            found_list = dest.search_name(temp.skills[i].name).ranks[temp.skills[i].level-1].armorlist
            found_list.deleteNode(itemname)
            found_list = s_list.search_name(temp.skills[i].name).ranks[temp.skills[i].level-1].armorlist
            found_list.deleteNode(itemname)

        armorlist.deleteNode(itemname)

        s_file = open('assets/skill_list.bin', 'wb')
        a_file = open('assets/armor_list.bin', 'wb')
        db_file = open('assets/database.bin', 'wb')

        pickle.dump(s_list, s_file)
        pickle.dump(armorlist, a_file)
        pickle.dump(db, db_file)
        s_file.close()
        a_file.close()
        db_file.close()

        print("item deleted")

    else:
        print("item not found")
    return

def getskillnames(s_list):

    out_list = []

    node = s_list.head
    while node.next is not None:
        out_list.append(node.data.name)
        node = node.next

    return out_list