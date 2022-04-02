import sys
import socket
import logging
import json
import dicttoxml
import os
import ssl
import threading

alldata = dict()
alldata['1']=dict(nomor=1, nama="Cortouis", posisi="kiper")
alldata['2']=dict(nomor=2, nama="Maguiare", posisi="bek kiri")
alldata['3']=dict(nomor=3, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['4']=dict(nomor=4, nama="victor lindelof", posisi="bek tengah kanan")
alldata['5']=dict(nomor=5, nama="Cortouis", posisi="kiper")
alldata['6']=dict(nomor=6, nama="Maguiare", posisi="bek kiri")
alldata['7']=dict(nomor=7, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['8']=dict(nomor=8, nama="victor lindelof", posisi="bek tengah kanan")
alldata['9']=dict(nomor=9, nama="De Gea", posisi="kiper")
alldata['10']=dict(nomor=10, nama="Maguiare", posisi="bek kiri")
alldata['11']=dict(nomor=11, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['12']=dict(nomor=12, nama="victor lindelof", posisi="bek tengah kanan")
alldata['13']=dict(nomor=13, nama="Cortouis", posisi="kiper")
alldata['14']=dict(nomor=14, nama="Maguiare", posisi="bek kiri")
alldata['15']=dict(nomor=15, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['16']=dict(nomor=16, nama="victor lindelof", posisi="bek tengah kanan")
alldata['17']=dict(nomor=17, nama="Maguiare", posisi="bek kiri")
alldata['18']=dict(nomor=18, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['19']=dict(nomor=19, nama="victor lindelof", posisi="bek tengah kanan")
alldata['20']=dict(nomor=20, nama="Cortouis", posisi="kiper")


def version():
    return "versi 0.0.1"


def proses_request(request_string):
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            pemain_number = cstring[1].strip()
            try:
                #logging.warning(f"data {nomorpemain} ketemu")
                hasil = alldata[pemain_pemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(data):
    serialized =  json.dumps(data)
    logging.warning("serialized data")
    return serialized

def handle_client(client_addres, connection) :
    
    selesai=False
    data_received="" #string
    
    while True :
        
        data = connection.recv(32)
        logging.warning(f"received {data}")
        if data:
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                selesai=True
                if (selesai==True):
                    hasil = proses_request(data_received)
                    hasil = serialisasi(hasil)
                    hasil += "\r\n\r\n"
                    connection.sendall(hasil.encode())
                    selesai = False
                    data_received = ""  
                    break

                else:
                    logging.warning(f"no more data from {client_address}")
                    break
    

def run_server(server_address,is_secure=False):
    # ------------------------------ SECURE SOCKET INITIALIZATION ----
    if is_secure == True:
        print(os.getcwd())
        cert_location = os.getcwd() + '/certs/'
        socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        socket_context.load_cert_chain(
            certfile=cert_location + 'domain.crt',
            keyfile=cert_location + 'domain.key'
        )
    # ---------------------------------

    #--- INISIALISATION ---
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the port
    print(f"[STARTING] starting up on {server_address}")
    server_sock.bind(server_address)
    
    # Listen for incoming connections
    server_sock.listen(1000)
    
    texec_index = 0
    texec = dict()
    
    
    while True:
        # Wait for a connection
        print(f"[WAITING] waiting for a connection")
        koneksi, client_address = server_sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:
            if is_secure == True:
                connection = socket_context.wrap_socket(koneksi, server_side=True)
            else:
                connection = koneksi
                
                texec[texec_index] = threading.Thread(target=handle_client, args=(client_address, connection))
                texec[texec_index].start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count()}" )
                texec_index += 1
                
            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000),is_secure=False)
    except KeyboardInterrupt:
        logging.warning("Control-C: STOPPED")
        exit(0)
    finally:
        logging.warning("selesai")