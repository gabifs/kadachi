from gui import *


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
            print("DATABASE INCOMPLETE, REBUILD NECESSARY")
            rebuild_database()
        if os.path.isfile('assets/armor_list.bin') is not True:  # caso um sequer não exista, é necessario reconstruir o banco de dados inteiro
            print("DATABASE INCOMPLETE, REBUILD NECESSARY")
            rebuild_database()
        if os.path.isfile('assets/database.bin') is not True:
            print("DATABASE INCOMPLETE, REBUILD NECESSARY")
            rebuild_database()
        else:
            print("All files present")

        s_file = open('assets/skill_list.bin', 'rb')
        a_file = open('assets/armor_list.bin', 'rb')
        db_file = open('assets/database.bin', 'rb')

        skill_list = pickle.load(s_file)  # carga das estruturas criadas previamente em execuções futuras
        armor_list = pickle.load(a_file)  # o tempo de processamento quando os dados são carregados do disco é exponencialmente menor
        db = pickle.load(db_file)

        s_file.close()
        a_file.close()
        db_file.close()

        print("Launching app...")

        root = tk.Tk()
        app = mainWindow(root,db,skill_list,armor_list)
        root.mainloop()

if __name__ == '__main__':
    main()
