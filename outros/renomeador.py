#
#   Código para renomear automáticamente os arquivos e alterar metadados
#

import os
from mutagen import File #rode esse cmd no seu terminal: pip install mutagen

#   Função responsável por deletar metadados de áudios (album, artista, titulo, etc)
def apagar_metadados(caminho_arquivo):
    try:
        audio = File(caminho_arquivo, easy=False)
        if audio is None:
            return False
        
        audio.delete()
        audio.save()
        
        return True
    except Exception as e:
        print(f"Erro ao limpar metadados de {caminho_arquivo}: {e}")
        return False


# Função para renomear os arquivos de áudio (excluir, substituir, metadados)
def renomear_arquivos(pasta, remover_texto=None, substituir_de=None, substituir_para=None, limpar_meta=False):
    if not os.path.isdir(pasta):
        print("Pasta não encontrada.")
        return

    for arquivo in os.listdir(pasta):
        caminho_antigo = os.path.join(pasta, arquivo)

        if os.path.isdir(caminho_antigo):
            continue

        if limpar_meta:
            if apagar_metadados(caminho_antigo):
                print(f"METADADOS APAGADOS: {arquivo}")

        novo_nome = arquivo

        if remover_texto and remover_texto in novo_nome:
            novo_nome = novo_nome.replace(remover_texto, "")

        if substituir_de and substituir_de in novo_nome:
            novo_nome = novo_nome.replace(substituir_de, substituir_para)

        if novo_nome != arquivo:
            caminho_novo = os.path.join(pasta, novo_nome)
            os.rename(caminho_antigo, caminho_novo)
            print(f"SUCCESS: {arquivo} -> {novo_nome}")

    print("\nFinalizado!")
    
#   Função principal para deixar tudo em ordem
def menu_principal():
    while True:
        print("=== Renomeador de Arquivos ===\n")
        pasta = input("Caminho da pasta: ")

        print("\nOpções:")
        print("1 - Remover texto\n2 - Substituir texto\n3 - Ambas")
        print("4 - Apagar metadados\n0 - Finalizar")
        op = input("\nEscolha uma opção: ")

        remover = None
        sub_de = None
        sub_para = None
        limpar_meta = False

        if op == "1" or op == "3":
            remover = input("Texto a remover: ")

        if op == "2" or op == "3":
            sub_de = input("Texto a substituir: ")
            sub_para = input("Substituir por: ")

        if op == "4":
            limpar_meta = True

        if op == "0":
            break

        renomear_arquivos(pasta, remover, sub_de, sub_para, limpar_meta)

menu_principal()
