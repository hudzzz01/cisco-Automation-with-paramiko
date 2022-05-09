import paramiko
import time
import sys
import os
from tqdm import tqdm
from ping3 import ping as pingpong

import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import random

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

deviceBerhasilPing = []
deviceConnectedReadyToSSH = []
deviceGagalSSH = []





def openKoneksiSSH(deviceConnectedReadyToSSH,count):
	forReturn = []
	#print(deviceConnectedReadyToSSH,count)
	host = str(deviceConnectedReadyToSSH[count][0])
	port = str(deviceConnectedReadyToSSH[count][1])
	username = str(deviceConnectedReadyToSSH[count][2])
	password = str(deviceConnectedReadyToSSH[count][3])
	devicePasswoed = str(deviceConnectedReadyToSSH[count][4])
	SSH_CLIENT = paramiko.SSHClient()
	SSH_CLIENT.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		SSH_CLIENT.connect(hostname=host,port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
		print("Connecting to", host )
		REMOTE_CONNECTION = SSH_CLIENT.invoke_shell()
		print("SSH Terhubung")
		REMOTE_CONNECTION.send("enable\n")
		REMOTE_CONNECTION.send(devicePasswoed + "\n")
		print("Interactive SSH session established")
		deviceName = str(REMOTE_CONNECTION.recv(50))
		deviceNamee = deviceName[6:len(deviceName)-2]
	except Exception as e:
		print("gagal masuk SSH", deviceConnectedReadyToSSH[count][0])
		deviceNamee = ""
		REMOTE_CONNECTION = ""
		forReturn.append(SSH_CLIENT)
		forReturn.append(REMOTE_CONNECTION)
		forReturn.append(devicePasswoed)
		forReturn.append(deviceNamee)
		return forReturn
		raise e
		
	forReturn.append(SSH_CLIENT)
	forReturn.append(REMOTE_CONNECTION)
	forReturn.append(devicePasswoed)
	forReturn.append(deviceNamee)
	#clientSSH[0],Remotconection[1],devicepass[2],devicename[3]
	return forReturn

def closeKoneksiSSH(SSH_CLIENT,REMOTE_CONNECTION):
	print(REMOTE_CONNECTION.recv(2048).decode())
	SSH_CLIENT.close()


def masukKeSSH(deviceConnectedReadyToSSH):
	global deviceBerhasilPing
	
	loop = tqdm(total = 100, position=0, leave=False)
	count = 0
	for i in range(len(deviceConnectedReadyToSSH)):
		#loading bar
		for j in range(int(100/len(deviceConnectedReadyToSSH))):
			loop.set_description("menghubungkan SSH ke semua perangkat .... ".format(j))
			loop.update(1)
			time.sleep(0.05)
		#masuk SSH
		connect = openKoneksiSSH(deviceConnectedReadyToSSH,count)
		SSH_CLIENT = connect[0]
		REMOTE_CONNECTION = connect[1]
		devicePasswoed = connect[2]
		deviceConnectedReadyToSSH[count].append(connect[3])
		if deviceConnectedReadyToSSH[count][5] == "":
			print("device dengan ip",deviceConnectedReadyToSSH[count][5]," gagal masuk SSH")
			deviceGagalSSH.append(deviceConnectedReadyToSSH[count])
			deviceConnectedReadyToSSH.pop(count)
			#print(deviceConnectedReadyToSSH)
			#input()

		else:
			# config #
			REMOTE_CONNECTION.send("show version\n")
			time.sleep(1) 
			closeKoneksiSSH(SSH_CLIENT,REMOTE_CONNECTION)
			count += 1
	loop.close()
	return deviceConnectedReadyToSSH


def getDeviceRedyConnectToSSH(pingBerhasilIndex0DanGagalIndex1,devices):
	deviceConnectedReadyToSSH = []
	count = 0
	#print(devices,"ini device")
	#print(pingBerhasilIndex0DanGagalIndex1,"ini ping berhasil dan gagal")
	#print(len(devices))
	#input()
	iterasi = 0
	#print(len(pingBerhasilIndex0DanGagalIndex1),len(devices))
	for i in pingBerhasilIndex0DanGagalIndex1[0]:
		print("Loading Data ....")
		for j in devices:
			#if str(pingBerhasilIndex0DanGagalIndex1[0][count][0]) == str(devices[iterasi][0]):
			#print(str(pingBerhasilIndex0DanGagalIndex1[0][count][0]) == str(devices[iterasi][0]))
			if  i[0] == j[0]:
				#print(i,j)
				deviceConnectedReadyToSSH.append(j)
			#input()
			iterasi += 1
		count +=1
	'''
	for i in range(len(devices[count][0])):
		if str(pingBerhasilIndex0DanGagalIndex1[0][count][0]) == str(devices[count][0]):
			deviceConnectedReadyToSSH.append(devices[count])
			print("plung")
		print(pingBerhasilIndex0DanGagalIndex1[0][count][0],"device : ",devices[count][0])
		input()
		count +=1
	'''
	#print(deviceConnectedReadyToSSH)
	#input()
		

	return deviceConnectedReadyToSSH

def tanyaSSH(ipResult):
	sshDesition = ""
	#print(ipResult[1])
	if ipResult[1] == []:
		sshDesition = input("Apakah anda ingin melanjutkan ke koneksi SSH ?  \n1.yes \n2.no\nMasukan jawaban berupa angka : ")

	elif ipResult[1] != []:
		sshDesition = input("Apakah anda ingin melanjutkan SSH ke Device yang terkoneksi saja ? \n1.yes \n2.no \nMasukan jawaban berupa angka : ")

	else:
		print("Tidak ada yang bisa dihubungkan silahkan cek kembali IP device anda")
		print(figlet_format("Termikasih telah menggunakan program ini, regard", font = "digital",width = 100))
		exit()
	

	return sshDesition


def validasiCekPing(tesPing):
	def trueFalseConverter(trueOrFalse):
		result = ""
		if trueOrFalse:
			result = "Ping Success"
		else:
			result = "Ping Failed"
		return result

	notSucsessPing = []
	SuccessPing = []
	result = []

	count = 0
	for i in range(len(tesPing)):
		if tesPing[count][1] == None:
			notSucsessPing.append([tesPing[count][0],tesPing[count][1]])
		else :
			SuccessPing.append([tesPing[count][0],tesPing[count][1]])
		count +=1
	
	#print(tesPing)
	jumlahTidakTerhubung = len(notSucsessPing)
	str(jumlahTidakTerhubung)
		
	count = 0
	ip = ""
	for i in range(len(tesPing)):
		ip += "\n"
		ip += "=> " + tesPing[count][0] + " : " + trueFalseConverter(tesPing[count][1])
		count +=1
	print(""" """,jumlahTidakTerhubung , """ device tidak dapat di ping.\n DEVICE DENGAN IP : """, ip,"\n")
	
	result.append(SuccessPing)
	result.append(notSucsessPing)

	return result

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def tesPing(devices):
	os.system('cls' if os.name == 'nt' else 'clear')
	
	count = 0
	tesPing = []
	errorPing =[]
	loop = tqdm(total = 100, position=0, leave=False)
	for i in range(len(devices)):
		tesPing.append([devices[count][0],pingpong(devices[count][0])])
		for j in range(int(100/len(devices))):
			loop.set_description("melakukan ping ke semua perangkat .... ".format(j))
			loop.update(1)
			time.sleep(0.05)
		printt=tesPing[i][0]
		if tesPing[i][1]:
			print(" ",printt," ...... Ok")
		else:
			print(printt," gagal terhubung dengan device")
		count += 1
	loop.close()
	
		
		
		


	'''
	count = 0
	a = 0
	for i in range(len(tesPing)):
		if tesPing[count][1] == False:
			errorPing.append([tesPing[count][0],tesPing[count][1]])
			a +=1
		count +=1
	return errorPing
	'''
	#print(tesPing)

	return tesPing


def networkDanPasswordDevice(devices):
	count=1
	device = []
	for i in range(len(devices)-1):
		device.append(devices[count].split(";"))
		count +=1
	return device

def bersihkanList(baris):
	count = 0
	for i in baris:
		if "\n" in i:
			baris[count]=i[0:len(i)-1]
		count +=1
	#print(baris)
	return baris

def bukafile(alamat,mode):
	with open(alamat,mode) as file:
		myfile = file.readlines()
		file.close
	return myfile



		



devices = bukafile("device.txt","r")
devices = bersihkanList(devices)


merek = devices[0]
devices = networkDanPasswordDevice(devices)
tesPing = tesPing(devices)

#os.system('cls' if os.name == 'nt' else 'clear')

pingBerhasilIndex0DanGagalIndex1 = validasiCekPing(tesPing)


tanyaSSH = tanyaSSH(pingBerhasilIndex0DanGagalIndex1)
tanyaSSH = str(tanyaSSH)

if tanyaSSH == "1":
	print("Mohon tunggu")
elif tanyaSSH == "2":
	print("Terimakasih telah menggunakan program ini")
	print(figlet_format("Regard", font = "banner3-D",width = 100))
	exit()

#print("ping behasil dan gagal : ", pingBerhasilIndex0DanGagalIndex1,"\n device pass : ", devices)

deviceConnectedReadyToSSH = getDeviceRedyConnectToSSH(pingBerhasilIndex0DanGagalIndex1=pingBerhasilIndex0DanGagalIndex1,devices=devices)
#print(deviceConnectedReadyToSSH)
#input()


#print(deviceConnectedReadyToSSH,"aaaaaaaaaa")

masukKeSSH = masukKeSSH(deviceConnectedReadyToSSH)

dataDevice = masukKeSSH #hostname,port,username,pass,devicepass,hostname len = count device


def menu():
	global dataDevice
	listFont = ["bulbhead","bubble","5lineoblique","digital"]
	#ipaddress,port,username,pass,devicepass,hostname len = count device
	def configGantiHostname(count):
		global dataDevice
		connect = openKoneksiSSH(dataDevice,count)
	

		SSH_CLIENT = connect[0]
		REMOTE_CONNECTION = connect[1]
		devicePasswoed = connect[2]
		os.system('cls' if os.name == 'nt' else 'clear')

		print("ada ingn mengubah menjadi hostname",[connect[len(connect)-1]], "menjadi apa ?")
		hostnameBaru = input("masukan nama hostname baru : ")
		# config #
		REMOTE_CONNECTION.send("configure terminal\n")
		REMOTE_CONNECTION.send("hostname "+hostnameBaru+"\n")
		REMOTE_CONNECTION.send("do wr\n")
		time.sleep(3) 
		

		closeKoneksiSSH(SSH_CLIENT,REMOTE_CONNECTION)
		print("berhasil mengubah hostname")
		time.sleep(2)
		
		dataDevice[count][5] = hostnameBaru

		return None

	def configGantiHostnameAll():
		global deviceConnectedReadyToSSH
		global dataDevice
		print(dataDevice)
		count = 0
		for i in range(len(dataDevice)):
			connect = openKoneksiSSH(dataDevice,count)
			SSH_CLIENT = connect[0]
			REMOTE_CONNECTION = connect[1]
			devicePasswoed = connect[2]
			deviceConnectedReadyToSSH[count]
			# config #
			REMOTE_CONNECTION.send("configure terminal\n")
			REMOTE_CONNECTION.send("hostname ROUTER"+str(count+1)+"\n")
			dataDevice[count][5] = "ROUTER"+str(count+1)
			time.sleep(1) 
			closeKoneksiSSH(SSH_CLIENT,REMOTE_CONNECTION)
			count += 1
		menu()


		return None

	def showVer(count):
		global dataDevice


		connect = openKoneksiSSH(dataDevice,count)
	

		SSH_CLIENT = connect[0]
		REMOTE_CONNECTION = connect[1]
		devicePasswoed = connect[2]
		os.system('cls' if os.name == 'nt' else 'clear')

		# config #
		REMOTE_CONNECTION.send("show version\n ")
		time.sleep(1)
		output =REMOTE_CONNECTION.recv(2048).decode()
		print(output[40:len(output)-6])
		SSH_CLIENT.close()
		
		
		print("\n\n diatas adalah data device dari : ", dataDevice[count][5])
		input()
		menu()

		return None

	def showVerAll():
		
		global dataDevice
		#print(dataDevice)
		count = 0
		for i in range(len(dataDevice)):
			connect = openKoneksiSSH(dataDevice,count)
			SSH_CLIENT = connect[0]
			REMOTE_CONNECTION = connect[1]
			devicePasswoed = connect[2]
			
			# config #
			REMOTE_CONNECTION.send("show version\n ")
			time.sleep(1) 
			closeKoneksiSSH(SSH_CLIENT,REMOTE_CONNECTION)
			output =REMOTE_CONNECTION.recv(2048).decode()
			print(output[40:len(output)-6])
			SSH_CLIENT.close()
		
			print("diatas adalah data device dari : ", dataDevice[count][5], "\n\n\n")
			count += 1
		
		input("tekan sembarang tombol untuk melanjutkan")
		menu()

	def ospfConfig(count):
		global dataDevice
		
		dataOspf = {}
		#jumlahNewtowk = input("Masukan jumlah network yang ingin di tambahkan : ")



		connect = openKoneksiSSH(dataDevice,count)
	

		SSH_CLIENT = connect[0]
		REMOTE_CONNECTION = connect[1]
		devicePasswoed = connect[2]
		os.system('cls' if os.name == 'nt' else 'clear')
		REMOTE_CONNECTION.send("configure terminal\n")

		idOspf = input("Masukan Id OSPF : ")
		jumlahNewtowk = int(input("Masukan Jumlah network : "))
		#networks = []
		for i in range(jumlahNewtowk):
			print("masukan network ke ",i," : ")
			network =input(" = ")
			print("masukan wilcard Mask ke ",i," : ")
			wilcardMask = input(" = ")
			print("masukan area ke ",i," : ")
			area = input(" = ")

			REMOTE_CONNECTION.send("router ospf "+idOspf+"\n")
			REMOTE_CONNECTION.send("network "+network+" "+wilcardMask+" area "+area+"\n")
			time.sleep(1)

		# config #
		
		SSH_CLIENT.close()
		
		print(REMOTE_CONNECTION.recv(2048).decode())
		print("selesai melakukan konfig ospf")
		input()
		menu()

		return None

	def saveConfig(count):
		global dataDevice
		#print(dataDevice)
		count = 0
		for i in range(len(dataDevice)):
			connect = openKoneksiSSH(dataDevice,count)
			SSH_CLIENT = connect[0]
			REMOTE_CONNECTION = connect[1]
			devicePasswoed = connect[2]
			
			# config #
			REMOTE_CONNECTION.send("wr\n ")
			time.sleep(1) 
			closeKoneksiSSH(SSH_CLIENT,REMOTE_CONNECTION)
			output =REMOTE_CONNECTION.recv(2048).decode()
			print(output[40:len(output)-6])
			SSH_CLIENT.close()
		
			
			count += 1
		
		input("tekan sembarang tombol untuk melanjutkan")
		menu()

		return None



	def showIP(count):
		global dataDevice
		connect = openKoneksiSSH(dataDevice,count)
	

		SSH_CLIENT = connect[0]
		REMOTE_CONNECTION = connect[1]
		devicePasswoed = connect[2]
		os.system('cls' if os.name == 'nt' else 'clear')

		
		# config #
		REMOTE_CONNECTION.send("configure terminal\n")
		#REMOTE_CONNECTION.send("hostname "+hostnameBaru+"\n")
		REMOTE_CONNECTION.send("do show ip int br\n")
		time.sleep(3) 
		

		#print(REMOTE_CONNECTION.recv(2048).decode())
		kata = str(REMOTE_CONNECTION.recv(2048).decode())

		lst = []
		for pos,char in enumerate(kata):
			if(char == "#"):
				lst.append(pos)
		
		lst2 = kata[lst[1]+20:len(kata)-1]

		

		lst2 = lst2.split("\n")

		lst3 = lst2[1:len(lst2)-1]
		lst2 =[]
		for i in lst3:
			i = i.replace(' ',';')
			lst2.append(i)
		lst3 = []
		for i in lst2:
			i = i.replace('\r','')
			lst3.append(i)
		lst2 = []
		for i in lst3:
			i = i.split(";")
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst2.append(i)

		lst3 = []
		for i in lst2:
			
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst3.append(i)
		lst2 = []
		for i in lst3:
			
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst2.append(i)

		lst3 = []
		for i in lst2:
			
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst3.append(i)

		lst2 = []
		for i in lst3:
			
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst2.append(i)

		lst3 = []
		for i in lst2:
			
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst3.append(i)

		lst2 = []
		for i in lst3:
			
			for x in enumerate(i):
				print("Loading Data .... Mohon Tunggu :)")
				if x[1] == "":
					#print("kososng")
					i.remove("")
					#print(i)
			lst2.append(i)

		print(lst2)

		os.system('cls' if os.name == 'nt' else 'clear')

		print("Di dapat data interface dari device ", dataDevice[count][5], " sebagai berikut :")
		#print("no   | Interface         | ip addres       |  ok    | status         protocol")
		count = 1
		for i in lst2:
			print(count," interface ",i[0])
			print("   Ip addres => ",i[1])
			print("   ok => ",i[2])
			print("   metod => ",i[3])
			if len(i)-1 == 6:
				print("   status => ",i[4]," ",i[5])
				print("   protocol => ",i[6],"\n")
			else:
				print("   status => ",i[4])
				print("   protocol => ",i[5],"\n")
			count += 1

		interface = int(input("Interface Mana yang ingin anda konfigur ? \n Masukan dengan nomor : "))
		
		if len(i)-1 == 6:
			status = str(lst2[interface-1][4]),str(lst2[interface-1][5])
		else:
			status = lst2[interface][4]

		interface = lst2[interface-1][0]

		print("Apa yang ingin anda lakukan ? \n 1. Mengubah ip interface ", interface, "\n 2. Mengaktifkan atau menonaktifkan Shutdown interface ",interface)
		
		answer = input("masukan dengan angka")

		if answer == "1":
			ipAddress = input("Masukan IP Address : ")
			Subnetmask = input("Masukan Subnetmask : ")

			REMOTE_CONNECTION.send("int "+interface+"\n")
			REMOTE_CONNECTION.send("ip add "+ipAddress+" "+Subnetmask+" "+"\n")

			if "up" in status:
				print("Berhasil ..... merubah ip \ninterface :",interface,"\n dengan ip : ",ipAddress,"\nSubnetmask :",Subnetmask,"\nstatus :",status)
			else :
				print("Interface dalam posisi",status,"Apakah anda ingin sekailan Mengaktifkanya ?\n 1. ya\n 2. tidak\n")
				answer = input("Jawab dengan angka : ")
				if answer == "1":
					REMOTE_CONNECTION.send("no shutdown \n")
				print("Berhasil ..... merubah ip \ninterface :",interface,"\ndengan ip : ",ipAddress,"\nSubnetmask :",Subnetmask,)
		elif answer == "2":

			

			print("1. nyalakan interface ",interface,"\n2. Matikan Interface ",interface,"\n")
			answer = input("Jawab dengan angka : ")
			if answer == "1":
				REMOTE_CONNECTION.send("int "+interface+"\n")
				time.sleep(1)
				REMOTE_CONNECTION.send("\n")
				REMOTE_CONNECTION.send("no sh\n")
				time.sleep(1)

				print(REMOTE_CONNECTION.recv(2048).decode())

				print("Berhasil ..... menyalakan")
			elif answer == "2":
				REMOTE_CONNECTION.send("int "+interface+"\n")
				time.sleep(1)
				REMOTE_CONNECTION.send("\n")
				REMOTE_CONNECTION.send("sh\n")
				time.sleep(1)
				print(REMOTE_CONNECTION.recv(2048).decode())

				print("Berhasil ..... men shutdown")


		

		#print(kata[lst[1]+18:len(kata)-1])
		SSH_CLIENT.close()


		input()
		
		#dataDevice[count][5] = hostnameBaru

		return None






	#menu Utama
	#print(dataDevice)

	c = 0 #count
	os.system('cls' if os.name == 'nt' else 'clear')
	print(figlet_format("Network Automation Cisco CLI by hudzzz01", font = random.choice(listFont),width = 100))
	time.sleep(1)
	print("Selamat datang di menu utama anda berhasil login ",str(len(dataDevice))," device Ready to Configure dengan data device yang tersedia sebagai berikut : \n")
	if deviceGagalSSH != []:
		print("Anda memiliki ",len(deviceGagalSSH)," buah kegagalan koneksi SSH yaitu di device berikut : ")
		for i in range(len(deviceGagalSSH)):
			print(i+1,"=>",deviceGagalSSH[i][0])
		print("Silahkan restar program ini jika anda ingin kembali menghubungkan SSH dengan Device Tersebut")
		if len(deviceGagalSSH) == len(deviceBerhasilPing):
			print(figlet_format("Regard", font = "banner3-D",width = 100))
			print("ternyata tidak ada device yang dapat di hubungkan SSH silahkan cek kembali file anda kemudian restar program ini \n terimakasih telah menggunakan program ini, ")
			exit()
	#print(len(deviceGagalSSH),len(deviceBerhasilPing))
	

	for i in range(len(dataDevice)):	
		print("Device yang tersedia :")
		print("......................................")
		print("Nama Device(hostname) : ",dataDevice[c][5],"\n")
		print("Ip addres : ",dataDevice[c][0],"\n")
		print("......................................")
		c +=1
	print("""Apa yang ingin anda lakukan ?
		1. Ganti Hostname
		2. Mengatur Ip Interface 
		3. Melihat Versi Perangkat
		4. OSPF
		5. Save
		6. keluar""")
	answer = str(input("Masukan jawaban anda dengan angka : "))
	if answer == "1":
		print("ଘ(੭*ˊᵕˋ)੭* Device mana yang ingin anda ganti hostnamenya ?\n")
		c = 0
		for i in range(len(dataDevice)):
			print(c+1, ". ",dataDevice[c][0]," ",dataDevice[c][5], "")
			c +=1
		print(c+1,". anda ingin mengubah semua device dengan urut?")
		answer = input("\nMasukan jawaban anda dengan angka : ")
		answer = int(answer)
		answer -=1
		if answer == len(dataDevice):
			os.system('cls' if os.name == 'nt' else 'clear')
			configGantiHostnameAll()
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			print(dataDevice[answer])
			devices =configGantiHostname(answer)
			print(devices, " dan ",dataDevice)
			menu()
	elif answer == "2":
		print("ଘ(੭*ˊᵕˋ)੭* Device mana yang ingin anda atur ap addresnya ?\n")
		c = 0
		for i in range(len(dataDevice)):
			print(c+1, ". ",dataDevice[c][0]," ",dataDevice[c][5], "")
			c +=1
		#print(c+1,".  anda ingin melihat show version semua device ")
		answer = input("\nMasukan jawaban anda dengan angka : ")
		answer = int(answer)
		answer -=1
		if answer == len(dataDevice):
			os.system('cls' if os.name == 'nt' else 'clear')
			showIPAll()
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			devices =showIP(answer)
			
			menu()



	elif answer == "3":
		print("ଘ(੭*ˊᵕˋ)੭* Device mana yang ingin melihat semua interface brief masing-masing device ?\n")
		c = 0
		for i in range(len(dataDevice)):
			print(c+1, ". ",dataDevice[c][0]," ",dataDevice[c][5], "")
			c +=1
		print(c+1,".  anda ingin melihat show version semua device ")
		answer = input("\nMasukan jawaban anda dengan angka : ")
		answer = int(answer)
		answer -=1
		if answer == len(dataDevice):
			os.system('cls' if os.name == 'nt' else 'clear')
			showVerAll()
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			devices =showVer(answer)
			
			menu()

	elif answer == "4":
		print("ଘ(੭*ˊᵕˋ)੭* Device mana yang ingin anda atur OSPFnya ?\n")
		c = 0
		for i in range(len(dataDevice)):
			print(c+1, ". ",dataDevice[c][0]," ",dataDevice[c][5], "")
			c +=1
		print(c+1,". Kembali ")
		answer = input("\nMasukan jawaban anda dengan angka : ")
		answer = int(answer)
		answer -=1
		if answer == len(dataDevice):
			os.system('cls' if os.name == 'nt' else 'clear')
			menu()
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			devices =ospfConfig(answer)
			
			menu()

			
			
			


	elif answer == "2":
		configInterface()
	elif answer == "3":
		configShowVersion(answer)
	elif answer == "4":
		configOSPF(answer)
	elif answer == "5":
		saveConfig(answer)
	elif answer == "6":
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Terimakasih Telah Menggunakan Program Ini")
		print(figlet_format("Regard", font = "banner3-D",width = 100))
	else :
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Masukan pilihan yang betul")
		time.sleep(1)


menu()


