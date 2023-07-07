import socket
import sys
import datetime as dtime
from datetime import datetime
import json
import logging
import signal

from server_part import app, db

#app.run(host='0.0.0.0', port=5035)

from server_part.model.part_info import Part
from server_part.model.rework_part_info import ReworkPart

def receiveSignal(signalNumber, frame):
    current_time = dtime.datetime.now()
    labelTime = current_time.strftime("%Y/%m/%d %H:%M:%S")
    logging.info('\n\t API stoped at {}'.format(labelTime))
    #print('Received:', signalNumber)
    sys.exit(0)

def generateTextLogging(textFunction, text, spaceText):
	return '{}{} --> {}'.format(spaceText, textFunction, text)

def generateLogging(textFunction, text, spaceText, loggingType = 'info'):
	loggingTypes = ['info', 'error', 'warning', 'debug']
	text_ = generateTextLogging(textFunction, text, spaceText)
	if loggingType is loggingTypes[1]:
		logging.error(text_)
		return
	if loggingType is loggingTypes[2]:
		logging.warning(text_)
		return
	if loggingType is loggingTypes[3]:
		logging.debug(text_)
		return
	logging.info(text_)


def create_object_Part(dataBytesStr = b""):
    if len(dataBytesStr) == 0:
        return None
    ### .... 
    try:
        data_str = dataBytesStr.decode("utf-8").replace("'", '"')
        #print(data_str)
        data_json = json.loads(data_str)
        #print(data_json)
        generateLogging('create_object_Part:: json:: ', '{}'.format(data_json), '\n\t', loggingType='info')
    except Exception as e:
        generateLogging('create_object_Part:: ', '{}'.format(e), '\n\t', loggingType='error')
        return None
    #for elem in data_json:
    #    print(elem, data_json[elem])
    if 'status' not in data_json or 'working_time' not in data_json:
        return None
    ### ......
    id_machine = 0
    timestamp = datetime.now()
    status = data_json['status']
    working_time = data_json['working_time']
    rework_part = None
    if status == 1:
        rework = data_json['rework']
        if rework == 1:
            rework_status = data_json['rework_status']
            reworking_time = data_json['reworking_time']
            rework_part = ReworkPart(timestamp=timestamp, status=rework_status, working_time=reworking_time)
    part = Part(id_machine=id_machine, timestamp=timestamp, status=status, working_time=working_time)
    return part, rework_part

def save_to_database(part_new):
    if part_new is None:
        return
    try:
        db.session.add(part_new)
        db.session.commit()
        #print(part_new)
        generateLogging('Save in db::: ', '{}'.format(part_new), '\n\t', loggingType='info')
    except Exception as e:
        generateLogging('When saving in db::: ', '{}'.format(e), '\n\t', loggingType='error')


fileNameLog = './logs/socketapp.log'

signal.signal(signal.SIGINT, receiveSignal)

logging.basicConfig(filename=fileNameLog, level=logging.INFO)

current_time = dtime.datetime.now()
labelTime = current_time.strftime("%d/%m/%Y %H:%M:%S")
logging.info('\n\t Starting (or re-starting) app at {}'.format(labelTime))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
ip_ = '192.168.0.19'
server_address = (ip_, 10001)
print('starting up on {} port {}'.format(*server_address))
text_info = 'starting up on {} port {}'.format(*server_address)
generateLogging('Socket:: ', '{}'.format(text_info), '\n\t', loggingType='info')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


while True:
    # Wait for a connection
    #print('waiting for a connection')
    text_info = 'waiting for a connection'
    generateLogging('Socket loop:: ', '{}'.format(text_info), '\n\t', loggingType='info')
    connection, client_address = sock.accept()
    print("Conexion establecida desde: ",client_address)
    try:
        #print('connection from', client_address)
        text_info = 'connection from', client_address
        generateLogging('Socket loop:: ', '{}'.format(text_info), '\n\t', loggingType='info')

        # Receive the data in small chunks and retransmit it
        whole_data = b""
        while True:
            data = connection.recv(16)
            #print(type(data))
            #print('received {!r}'.format(data))
            if data:
                whole_data += data
                #print('sending data back to the client')
                connection.sendall(data)
            else:
                #print('no data from', client_address)
                break
        #print(type(whole_data), ":: Whole data: ", whole_data)
        text_info = type(whole_data), ":: Whole data: ", whole_data
        generateLogging('Socket loop:: ', '{}'.format(text_info), '\n\t', loggingType='info')
        part_new, rework_part_new  = create_object_Part(dataBytesStr = whole_data)
        #print(part_new)
        #print(rework_part_new)
        save_to_database(part_new)
        if rework_part_new is not None:
            rework_part_new.id = part_new.id
        save_to_database(rework_part_new)

    finally:
        # Clean up the connection
        connection.close()

