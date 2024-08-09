import os
import subprocess
from datetime import datetime
from escpos.printer import Usb
import netifaces

# Configurações da impressora USB (porta atualizada)
printer = Usb(0x04b8, 0x0e27, 0)

def is_network_ready():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface != 'lo' and netifaces.AF_INET in netifaces.ifaddresses(interface):
            return True
    return False

def get_network_interfaces():
    interfaces = netifaces.interfaces()
    interface_data = []
    
    for interface in interfaces:
        if interface == 'lo':  # Ignora a interface 'lo'
            continue
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ip_info = addresses[netifaces.AF_INET][0]
            ip_address = ip_info.get('addr')
            netmask = ip_info.get('netmask')
            gateways = netifaces.gateways()
            gw_address = gateways['default'][netifaces.AF_INET][0] if 'default' in gateways and netifaces.AF_INET in gateways['default'] else "N/A"
            if ip_address:
                interface_data.append((interface, ip_address, netmask, gw_address))
    
    return interface_data

def get_system_info():
    # Obtém a versão do sistema operacional
    os_version = None
    try:
        os_version = subprocess.check_output(['uname', '-a']).decode('utf-8').strip()
    except Exception as e:
        os_version = f"Erro ao obter a versão do SO: {str(e)}"
    return os_version

def check_server_connection(server_ip):
    # Verifica se o servidor responde ao ping
    try:
        subprocess.check_output(['ping', '-c', '1', server_ip], stderr=subprocess.STDOUT)
        return f"Conexão com o servidor ({server_ip}) - OK"
    except subprocess.CalledProcessError:
        return f"Servidor ({server_ip}) não respondendo"

def print_report():
    # Dados para o relatório
    interfaces = get_network_interfaces()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os_version = get_system_info()
    server_status = check_server_connection('192.168.30.202')

    # Imprime o relatório
    printer.set(align='center', bold=True, double_height=True)
    printer.text("Resumo de Inicialização\n\n")
    printer.set(align='left', bold=False, double_height=False)
    printer.text(f"Data e Hora: {current_time}\n\n")

    for interface, ip_address, netmask, gw_address in interfaces:
        printer.text(f"Interface: {interface}\n")
        printer.text(f"IP: {ip_address}\n")
        printer.text(f"Máscara: {netmask}\n")
        printer.text(f"Gateway: {gw_address}\n\n")

    printer.text(f"Versão do SO: {os_version}\n\n")

    printer.set(align='center', bold=True, double_height=True)
    printer.text("Status do Servidor\n\n")
    printer.set(align='center', bold=True, double_height=False)
    printer.text(f"{server_status}\n")

    printer.cut()

if __name__ == "__main__":
    # Aguarde até que a rede esteja pronta
    while not is_network_ready():
        print("Aguardando rede estar pronta...")
        time.sleep(5)

    # Executa a impressão do relatório
    print_report()
