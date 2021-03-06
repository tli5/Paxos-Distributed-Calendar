#A calendar system with a user interface

#Distributed Systems Project 2
#Greg Weil
#Taoran Li

#Run with python 2.7.10
#Pass config path and what node index this is
#Example: ui-paxos.py config/local.cfg 0

import random
import sys
import time
import glob
import os
import paxosnew
import paxosCalendar
import leader, network

config = str(sys.argv[1])
node = int(sys.argv[2])
uiNetwork = network.Network(config, node)
paxos = paxosnew.Paxos(leader.LeaderNetwork(uiNetwork))
cal = paxosCalendar.Calendar(config, node, paxos)

def addAppointment():
	name = raw_input('appointment name:' )
	day = int(raw_input('appointment day:' ))
	start = int(raw_input('appointment start:' ))
	stop = int(raw_input('appointment stop:' ))
	memberStrArr = raw_input('appointment members(format [A B C]):' ).split(' ')
	members = [int(memberStr) for memberStr in memberStrArr ]
	appointment = paxosCalendar.Appointment(name, day, start, stop, members)

	DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	try:
		cal.addAppointment(appointment)
		print('appointment to add: ' + str(appointment))
	except Exception as other:
		other = other[0]
		print "conflicting with event:"
		print 'Name:', other.name
		print '\ton', DAYS[other.day], 'From', printTime(other.start), 'To', printTime(other.end)
		if len(other.members) > 1 :
			print '\tmembers:', str(other.members )


def delAppointment():
	print('select an appointment to delete:')
	nodesAppointments = showAppointments()
	if nodesAppointments:
		node = cal.node
		index = int(raw_input('name of appointment to delete:') )
		cal.removeAppointment(nodesAppointments[node][index])
		print('deleted appointment: ' + nodesAppointments[node][index].name)
		print '------------------------------------'
		print 'current appointments:'
		time.sleep(1)
		showAppointments()
	else:
		print('no appointments available')


def printTime(time):
	return (str) (time / 2) + ':' + ('00' if time % 2 == 0 else '30')

def showAppointments():
	nodesAppointments = cal.getAppointmentsByNodes()
	DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

	for node in range (len(nodesAppointments) ):
		"""skipping all other nodes' appointments"""
		if node != cal.node:
			continue
		appointments = nodesAppointments[node]
		
		for i in range(len(appointments)):
			appointment = appointments[i]
			print 'Name:', appointment.name, "index:", i
			print '\ton', DAYS[appointment.day], 'From', printTime(appointment.start), 'To', printTime(appointment.end)
			if len(appointment.members) > 1 :
				print '\tmembers:', str(appointments[i].members )
		print 'Current Node:', node
	return nodesAppointments

def clearLog():
	filePaths = ["./data*.sav", "paxos*.sav" ]
	for filePath in filePaths :
		files = glob.glob(filePath)
		for file in files:
			print 'deleting file:', file
			os.remove(file)

def proposeAppointment():
	print 'Choose: ', '1: Add Appointment', '2: Remove Appointment', '3: Main Menu'
	option = raw_input('Option:')
	exe = {
	    '1': addAppointment,
	    '2': delAppointment,
	    '3': mainMenu
	}[option]
	exe()


def mainMenu() :
	exe = {
		'1': proposeAppointment,
		'2': clearLog,
		'3': showAppointments
	}
	while True:
		print 'Menu: ', '1: Propose Adding/Deleting Apt', '2: Clear Local Log Files', '3: Display Appointments', '4: crash node'
		option = raw_input('Option:')
		if (option == '4'):
			break
		elif (option == '5'):
			print('Leader: ' + str(paxos.network.leader))
		if not option in exe:
			continue
		exe[option]()

mainMenu()

del paxos
