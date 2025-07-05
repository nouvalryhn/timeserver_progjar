import socket
import sys
import logging
import time

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_client():
    host = '127.0.0.1'
    port = 45000

    try:
        # Buat socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"Connecting to {host}:{port}")
        client_socket.connect((host, port))
        logging.info("Connected to the time server.")

        # Mengirim request "TIME" dan menerima respons
        request_time = "TIME\r\n"
        logging.info(f"Sending request: '{request_time.strip()}'")
        client_socket.sendall(request_time.encode('utf-8'))
        
        response = client_socket.recv(1024).decode('utf-8').strip()
        logging.info(f"Received response: '{response}'")

        time.sleep(1)

        # Mengirim request "QUIT" untuk menutup koneksi
        request_quit = "QUIT\r\n"
        logging.info(f"Sending request: '{request_quit.strip()}'")
        client_socket.sendall(request_quit.encode('utf-8'))
        

    except ConnectionRefusedError:
        logging.error(f"Connection to {host}:{port} refused. Make sure the server is running.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Closing socket.")
        client_socket.close()

if __name__ == "__main__":
    run_client() 