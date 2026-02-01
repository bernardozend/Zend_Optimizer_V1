import os
import shutil
import subprocess
import datetime
import sys
import hashlib
import time

# Cores Matrix
VERDE = '\033[92m'
RESET = '\033[0m'

def gerar_hash_arquivo():
    try:
        sha256_hash = hashlib.sha256()
        with open(sys.argv[0], "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except: return "Erro ao gerar Hash"

def cabecalho_matrix():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(VERDE + r"""
  ______ _   _ _____  
 |___  /| \ | |  __ \ 
    / / |  \| | |  | |
   / /  | . ` | |  | |
  / /__ | |\  | |__| |
 /_____||_| \_|_____/ 
                      
   ZEND - OPTIMIZER V1.0
    """ + RESET)

def barra_progresso(percentual, tarefa=""):
    tamanho_barra = 30
    preenchido = int(tamanho_barra * percentual // 100)
    barra = '█' * preenchido + '░' * (tamanho_barra - preenchido)
    # Mostra a barra e a tarefa atual
    sys.stdout.write(f'\r{VERDE}[{barra}] {percentual}% - {tarefa}{RESET}')
    sys.stdout.flush()

def get_dir_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(): total += entry.stat().st_size
            elif entry.is_dir(): total += get_dir_size(entry.path)
    except: pass
    return total

def start_limpeza():
    espaco_inicial = shutil.disk_usage("C:").free / (1024**3)
    
    print(f"\n{VERDE}[!] INICIANDO OPERAÇÕES DE INFRAESTRUTURA...{RESET}\n")

    # OPERAÇÃO 1: Hibernação e Reservado
    barra_progresso(10, "Limpando Hibernação...")
    subprocess.run("powercfg -h off", shell=True)
    
    barra_progresso(20, "Limpando Armazenamento Reservado...")
    subprocess.run("DISM /Online /Set-ReservedStorageState /State:Disabled", shell=True)

    # OPERAÇÃO 2: Perfis de Usuários
    print(f"\n\n{VERDE}[!] ANALISANDO PERFIS (C:\\Users):{RESET}")
    for user in os.listdir("C:\\Users"):
        full_path = os.path.join("C:\\Users", user)
        if os.path.isdir(full_path) and user not in ["All Users", "Default", "Public", "desktop.ini"]:
            tamanho = get_dir_size(full_path) / (1024**3)
            data_acesso = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%d/%m/%Y')
            print(f" -> {user.ljust(15)} | Espaço: {tamanho:6.2f} GB | Acesso: {data_acesso}")
    
    barra_progresso(40, "Perfis analisados.")
    time.sleep(1)

    # OPERAÇÃO 3: Caches de Navegadores
    print(f"\n\n{VERDE}[!] LIMPANDO CACHES DE NAVEGADORES...{RESET}")
    appdata = os.environ.get('LOCALAPPDATA')
    caminhos = {
        "Chrome": "Google\\Chrome\\User Data\\Default\\Cache",
        "Edge": "Microsoft\\Edge\\User Data\\Default\\Cache",
        "Brave": "BraveSoftware\\Brave-Browser\\User Data\\Default\\Cache"
    }
    for nome, p in caminhos.items():
        alvo = os.path.join(appdata, p)
        if os.path.exists(alvo):
            shutil.rmtree(alvo, ignore_errors=True)
            print(f"[OK] {nome} limpo.")
    
    barra_progresso(60, "Caches limpos.")

    # OPERAÇÃO 4: Deep Clean (DISM e VSS) - ESSES DEMORAM
    print(f"\n\n{VERDE}[!] EXECUTANDO LIMPEZA DE COMPONENTES (DISM)...{RESET}")
    barra_progresso(70, "Limpando WinUpdate (Aguarde)...")
    subprocess.run("dism /online /cleanup-image /startcomponentcleanup /resetbase", shell=True)
    
    print(f"\n{VERDE}[!] REMOVENDO SHADOW COPIES (VSS)...{RESET}")
    barra_progresso(85, "Limpando Pontos de Restauração...")
    subprocess.run("vssadmin delete shadows /all /quiet", shell=True)

    # OPERAÇÃO 5: Integridade
    print(f"\n{VERDE}[!] VERIFICANDO INTEGRIDADE DO SISTEMA (SFC)...{RESET}")
    barra_progresso(95, "Finalizando...")
    subprocess.run("sfc /scannow", shell=True)

    barra_progresso(100, "CONCLUÍDO!")
    
    espaco_final = shutil.disk_usage("C:").free / (1024**3)
    deletado = espaco_final - espaco_inicial

    print(f"\n\n{VERDE}" + "="*60)
    print(f"         RELATÓRIO FINAL - ZEND OPTIMIZER")
    print(f"[*] Espaço recuperado: {deletado:.2f} GB")
    print(f"[*] Espaço livre total: {espaco_final:.2f} GB")
    print(f"[*] SHA-256 ID: {gerar_hash_arquivo()}")
    print("="*60 + RESET)
    print(f"\n{VERDE}Obrigado por utilizar a ferramenta!{RESET}")
    input("\nPressione ENTER para fechar...")

# MENU INICIAL
if __name__ == "__main__":
    cabecalho_matrix()
    print(f"{VERDE}1 - START LIMPEZA PROFUNDA{RESET}")
    print(f"2 - SAIR")
    if input(f"\n{VERDE}Zend@Console:~# {RESET}") == '1':
        start_limpeza()