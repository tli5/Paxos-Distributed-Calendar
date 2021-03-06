#A basic testing program for the paxos library

import sys, time

import paxosnew
import leader
import network

node = int(sys.argv[1])

cal = paxosnew.Paxos(leader.LeaderNetwork(network.Network('config/local.cfg', node)))

def onCommit(val, index):
	print(index, val)
cal.onCommit = onCommit
def onFail(val, index):
	print('fail', index, val)
	cal.propose(val)
cal.onFail = onFail

print('This is node ' + str(node))

while True:
	text = raw_input()
	if not text: break
	elif text == 'leader': print('leader: ' + str(cal.network.leader))
	elif text == 'proposals': print('proposals: ' + str(cal.proposals))
	elif text == 'log': print('log: ' + str(cal.retrieveLog()))
	else: cal.propose(text)
