import pprint
#instalar pprint ou usar pipenv install
#bib para impressão organizada de dicionários

class Trie:
	def __init__(self):
		self.head = {}

	def add(self, nodo): #recebe um nodo, cria uma caminho na trie usando o nome do nodo, e insere o nodo na trie
		atual = self.head
					#nodo['name']
		for letra in nodo.data.name: #acesso ao nome do nodo
			if letra not in atual:
				#Se a letra não está inserida cria um dicionário para a letra
				atual[letra] = {}
			#Altera a posição da head para o dicionário em letra
			atual = atual[letra]
		#guarda o nodo no último dicionário
		atual['$'] = nodo

	def search(self, word):
		atual = self.head

		for letra in word:
			if letra not in atual:
				return False
			atual = atual[letra]

		if '$' in atual:
			return atual['$'] #retorna o nodo
		else:
			return False #ou retorna False

	def imprime(self):
		pprint.pprint(self.head) #imprime todo o dicionário que compoe a trie


if __name__ == "__main__":
	'''
	trie = Trie() #cria uma trie nova
	trie.add(nodo) #adiciona um novo nodo na trie
	trie.search("nome do nodo") #dado um nome de nodo, procura o nodo na trie
	trie.imprime() #imprime todo o dicionário que compoe a trie
	'''
