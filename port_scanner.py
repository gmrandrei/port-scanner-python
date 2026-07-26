import argparse
import ipaddress
import socket


def scan_port(ip: str, port: int, timeout: float = 1.0) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    result = sock.connect_ex((ip, port))
    sock.close()

    return result == 0


def scan_range(ip: str, start_port: int, end_port: int) -> list[int]:
    open_ports = []

    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            open_ports.append(port)

    return open_ports


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Escaner de puertos TCP educativo."
    )
    parser.add_argument("ip", help="Direccion IP objetivo")
    parser.add_argument("-s", "--start-port", type=int, default=1, help="Puerto inicial (default: 1)")
    parser.add_argument("-e", "--end-port", type=int, default=1024, help="Puerto final (default: 1024)")

    args = parser.parse_args()

    try:
        ipaddress.ip_address(args.ip)
    except ValueError:
        parser.error(f"'{args.ip}' no es una direccion IP valida.")

    if not (1 <= args.start_port <= args.end_port <= 65535):
        parser.error("Rango de puertos invalido. Debe cumplir 1 <= start <= end <= 65535.")

    return args


def confirm_authorization(ip: str) -> bool:
    if ipaddress.ip_address(ip).is_private:
        return True

    respuesta = input(
        f"[!] {ip} no es una IP privada/local. "
        "Confirmas que tienes autorizacion explicita para escanearla? (s/n): "
    )
    return respuesta.strip().lower() == "s"


def print_results(ip: str, open_ports: list[int]) -> None:
    print(f"\nResultados del escaneo para {ip}:")

    if not open_ports:
        print("No se encontraron puertos abiertos en el rango especificado.")
        return

    for port in open_ports:
        print(f"  Puerto {port}/tcp -> ABIERTO")


def main() -> None:
    args = parse_arguments()

    if not confirm_authorization(args.ip):
        print("Escaneo cancelado: autorizacion no confirmada.")
        return

    print(f"Escaneando {args.ip} en el rango de puertos {args.start_port}-{args.end_port}...")
    open_ports = scan_range(args.ip, args.start_port, args.end_port)
    print_results(args.ip, open_ports)


if __name__ == "__main__":
    main()
