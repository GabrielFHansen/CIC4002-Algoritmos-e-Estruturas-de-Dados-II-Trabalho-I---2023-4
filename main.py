import struct
import os

registros = []

#Pega valores do arquivo principal arquivofinal.csv
def pegavalores(pos):
    with open("arquivofinal.csv", 'r', errors='ignore') as indexIdFile:

        for _ in range(pos):
            next(indexIdFile)
        rowList = next(indexIdFile).split(";")

        return rowList

#rowCount - Conta número total de linhas
def rowCount(dataFile):
    for high, line in enumerate(dataFile):
        pass 
    high += 1
    return high

#nao terminado
def inserir_registro_ordenado(data_file, registro):
    registros = []
    
    # Lê os registros existentes do arquivo binário
    with open(data_file, 'rb') as file:
        while True:
            try:
                tamanho_campo = struct.unpack('I', file.read(4))[0]
                campo_bytes = file.read(tamanho_campo)
                campo = campo_bytes.decode('utf-8')
                registros.append(campo)
            except struct.error:
                break
    
    # Insere o novo registro na posição correta com base no App Id
    registro[0] = input("App Name:")
    registro[1] = input("App Id:")
    registro[2] = input("Category:")
    registro[3] = input("Rating:")
    registro[4] = input("Installs:")
    registro[5] = input("Released:")
    registro[6] = input("LastUpdated:")
    registro[7] = input("Price:")
    registro[8] = input("Currency:")
    registro[9] = input("Size:")
    registro[10] = input("DeveloperId:")
    registros.append(registro)
    registros.sort(key=lambda x: x.split(";")[1])  # Ordena os registros pelo App Id
    
    # Escreve os registros ordenados de volta no arquivo
    with open(data_file, 'wb') as file:
        for campo in registros:
            campo_bytes = campo.encode('utf-8')
            tamanho_campo = len(campo_bytes)
            file.write(struct.pack('I', tamanho_campo))
            file.write(campo_bytes)

# Cria indice em arquivo pelo app id (chave ordenado)
def criar_indice_app_id(datafile):
    if(os.path.exists("Data/IndexID.csv")):
        os.remove("Data/IndexID.csv")
    indexIdFile = open("Data/IndexID.csv", 'w')
    pos = 0
    i = 0

    for row in datafile:
        rowCsv = row.split(";")
        indexIdFile.write(str(i).ljust(6)+';'+str(pos).ljust(6)+';'+rowCsv[0]+'\n')
        pos+=1
        i+=1

    indexIdFile.close()

# Cria indice em arquivo pela categoria (repete, nao ordenado)
def criar_indice_category(datafile):
    if(os.path.exists("Data/CategoryIndex.csv")):
        os.remove("Data/CategoryIndex.csv")
    indexCategoryFile = open("Data/CategoryIndex.csv", 'w')
    pos = 0
    i = 0

    for row in datafile:
        rowCsv = row.split(";")
        indexCategoryFile.write(str(i).ljust(6)+';'+str(pos).ljust(6)+';'+rowCsv[2]+'\n')
        pos+=1
        i+=1

    indexCategoryFile.close()

#Usa pesquisa binária para realizar uma consulta por app id. Ex.: a.dev.mobile.thread
def consultar_por_app_id(id):
    found = False
    low = 0
    mid = 0

    with open('arquivofinal.csv', 'r', errors='ignore') as datafile:
        high = rowCount(datafile)

    while low <= high:
        mid = (high+low)//2

        with open("Data/indexID.csv", 'r') as indexIdFile:

            for _ in range(mid):
                next(indexIdFile)
            rowList = next(indexIdFile).split(";")

            if len(rowList) >= 3:
                rowId = rowList[2][0:19].strip()

            if rowId < id:
                low = mid
            elif rowId > id:
                high = mid
            else:
                found = True
                break

    if found == False:
        return None 
    else:
        return rowList

#Usa pesquisa binária para realizar uma consulta por category. Ex.: Education
def consultar_por_category(category):
    found = False
    low = 0
    mid = 0

    with open('arquivofinal.csv', 'r', errors='ignore') as datafile:
        high = rowCount(datafile)

    while low <= high:
        mid = (high+low)//2

        with open("Data/CategoryIndex.csv", 'r') as categoryFile:

            for _ in range(mid):
                next(categoryFile)
            rowList = next(categoryFile).split(";")

            if len(rowList) >= 3:
                rowId = rowList[2][0:19].strip()

            if rowId < id:
                low = mid
            elif rowId > id:
                high = mid
            else:
                found = True
                break

    if found == False:
        return None 
    else:
        return rowList

#Exibe valores de toda a linhas selecionada
def exibir_resultados(registros):
    if not registros:
        print("Nenhum resultado encontrado.")
        return

    print("\nResultados da Consulta:")
    print("============================================")
    
    for registro in registros:
        print("App Name:", registro[0])
        print("App Id:", registro[1])
        print("Category:", registro[2])
        print("Rating:", registro[3])
        print("Installs:", registro[4])
        print("Released:", registro[5])
        print("LastUpdated:", registro[6])
        print("Price:", registro[7])
        print("Currency:", registro[8])
        print("Size:", registro[9])
        print("DeveloperId:", registro[10])
        print("============================================")

#Função main para chamar todas as outras e com menu interativo por console
def main():
    data_file = "dados.bin"

    while True:
        print("\nOpções:")
        print("1. Inserir índice por App Id")
        print("2. Inserir índice por Category")
        print("3. Consultar por App Id")
        print("4. Consultar por Category")
        print("5. Inserir registro")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "0":
            print("Saindo.")
            break

        elif escolha == "1":
            datafile = open('arquivofinal.csv', 'r', errors='ignore')
            criar_indice_app_id(datafile)

        elif escolha == "2":
            datafile = open('arquivofinal.csv', 'r', errors='ignore')
            criar_indice_category(datafile)

        elif escolha == "3":
            app_id = input("Digite o Id: ")
            resultado = consultar_por_app_id(app_id)

            if resultado:
                register = pegavalores(int(resultado[1]))
                exibir_resultados([register])
            else:
                print("App Id não encontrado.")

        elif escolha == "4":
            category = input("Digite a Categoria: ")
            resultado = consultar_por_category(category)

            if resultado:
                register = pegavalores(int(resultado[1]))
                exibir_resultados([register])
            else:
                print("Category não encontrada.")

        elif escolha == "5":
            for registro in registros:
                inserir_registro_ordenado(data_file, registro)

if __name__ == "__main__":
    main()