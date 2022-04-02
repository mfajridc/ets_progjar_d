import sys
import socket
import json
import logging
import xmltodict
import ssl
import os
import time
import datetime
import threading
import random
from tabulate import tabulate


IP = '172.16.16.101'
PORT = 12000
SERVER_ADDR = (IP, PORT)

def make_socket(SERVER_ADDR):
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # server_address = (destination_address, port)
        logging.warning(f"connecting to {SERVER_ADDR}")
        client_sock.connect(SERVER_ADDR)
        return client_sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def make_secure_socket(SERVER_ADDR):
    try:    

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode=ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/domain.crt')

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_address = (destination_address, port)
        logging.warning(f"connecting to {SERVER_ADDR}")
        client_sock.connect(SERVER_ADDR)
        secure_socket = context.wrap_socket(client_sock,SERVER_ADDR)
        logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(data):
    #logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(data)
    

def send_command(command_str,is_secure=False):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if is_secure == True:
        client_sock = make_secure_socket(SERVER_ADDR)
    else:
        client_sock = make_socket(SERVER_ADDR)

    #logging.warning(f"connecting to {SERVER_ADDR}")
    try:
        logging.warning(f"sending message ")
        client_sock.sendall(command_str.encode())
        data_received="" #empty string
        while True:
            data = client_sock.recv(16)
            time.sleep(0.5)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:                    
                    break
            else:
                break
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False



def getdatapemain(nomor=0,is_secure=False):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil

def lihatversi(is_secure=False):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil


def data_pemain(total_request, table_data):
    total_response = 0
    texec = dict()
    catat_awal = datetime.datetime.now()

    for n in range(total_request):
        texec[n] = threading.Thread(target=getdatapemain, args=(random.randint(1, 20),))
        texec[n].start()

    for n in range(total_request):
        if (texec[n]):
            total_response += 1
        texec[n].join()

    catat_akhir = datetime.datetime.now()
    selesai = catat_akhir - catat_awal
    table_data.append([total_request, total_request, total_response, selesai])

if __name__ == '__main__':

    total_request = [1, 5, 10, 20]
    table_data = []
    
    for request in total_request:
        data_pemain(request, table_data)
        
    table_header = ["Jumlah Thread", "Jumlah Request", "Jumlah Response", "Latency"]
    print(tabulate(table_data, headers=table_header, tablefmt="fancy_grid"))
