from pymodbus.client.sync_diag import ModbusTcpClient

#Crea una instancia del cliente Modbus PLC
ip='ip_del_plc'
port=555
plc = ModbusTcpClient(ip,port)
print(plc)

#Conecta al PLC
plc.connect()

#Lee el valor de una bobina coil en el PLC
resultado = plc.read_coils(address=0,count=1,unit=1)
valor_bobina = resultado.bits[0]

#Escribe un valor en un registro (holding register) en el PLC
valor = 12345
plc.write_register(address=0,value=valor, unit=1)

plc.close()