import os
import schedule
import pathlib
import shutil
import time
import sys
from win10toast import ToastNotifier

caminho = ''
caminho2 = ''
list_file = []
new_list_file = []
new_file = []
notificacao = ToastNotifier()
# função que lista todos os arquivos da pasta
def lista_arquivos_inicial(caminho):
    lista = []
    for root, files in os.walk(caminho):
        for file in files:
            lista.append(os.path.join(root, file))
    return lista


class TransferenciaArquivos:
    def __init__(self):
        pass


    def valida_dir(self, caminho) -> bool:
        if os.path.isdir(pathlib.Path(caminho)):
            return True

        print('Diretório inserido não é valido!!')
        return False


    def iniciar(self, old_dir, new_dir):
        new_list_file = self.lista_arquivos_inicial(old_dir)
        new_file = self.separa_arquivos_novos(list_file, new_list_file)
        self.copia_arquivos(new_dir, new_file)

    # função que lista todos os arquivos dentro da pasta
    def lista_arquivos_inicial(self, caminho):
        lista = []
        for root, dir, files in os.walk(caminho):
            for file in files:
                lista.append(os.path.join(root, file))
        return lista

    # função que extrai todos os arquivos recentes que não estavam na primeira consulta
    def separa_arquivos_novos(self, old_list, new_list):
        lista = []
        for file in new_list:
            if file not in old_list:
                lista.append(file)
        return lista

    # função que transfere os arquivos para a pasta de destino
    def copia_arquivos(self, caminho, list_arquivo):
        if len(list_arquivo) == 0:
            pass
        else:
            for file in list_arquivo:
                name_arq = pathlib.Path(file).name
                new_dir = os.path.join(caminho, name_arq)
                list_file.append(file)
                try:
                    shutil.copy(file, new_dir)
                    notificacao.show_toast('Movimentação de arquivo', f'O arquivo {name_arq} foi transferido com sucesso',duration=10)

                except Exception:
                    notificacao.show_toast('Movimentação de arquivo', f'Não foi possivel copiar o arquivo {name_arq}',duration=10)
                    continue

if __name__ == "__main__":

    print('     =================================================================')
    print('     Pressione ctrl + C no prompt de comando para cancelar o programa')
    print('     =================================================================')
    # ================= INICIO DO PROGRAMA ==============================='
    # insere caminho de arquivos
    parametros: dict = {}
    program = TransferenciaArquivos()
    tempo_freq: int = 20
    try:
        
        origem = input('Digite o diretório de origem: ').strip()
        var_origem = program.valida_dir(origem)
        if not var_origem:
            sys.exit()
        destino = input('Digite o diretório de Destino: ').strip()
        var_destino = program.valida_dir(destino)
        if not var_destino:
            sys.exit()
        freq = int(input('Consultar a cada (segundo) padrão 20 segundos: '))

        if freq > 0:
            tempo_freq = freq
        else:
            print('Tempo padrão acionado 20 segundos!')
            pass 

    except KeyboardInterrupt:
        print('O Programa foi finalizado')
        sys.exit()


    # lista todos os arquivos dentro da pasta
    list_file = lista_arquivos_inicial(caminho)
    # definição de rotina (frequencia que sera executado)
    schedule.every(tempo_freq).seconds.do(program.iniciar, origem, destino)
    # loop de repetição de rotina

    while 1:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print('Programa finalizado')
            sys.exit()

