#A distributed calendar system

import log

class Appointment:
	def __init__(self, name, day, start, end):
		self.name = name
		self.day = day
		self.start = start
		self.end = end
	
	def __str__(self):
		return str((self.name, self.day, self.start, self.end))
	
	def checkConflict(self, other):
		"""Check if this event conflicts with another"""
		if (self.day != other.day):
			return False
		if (self.start >= other.end):
			return False
		if (self.end <= other.start):
			return False
		return True

class Calendar:
	def __init__(self, node, count):
		self.log = log.Log(node, count)
	
	def getAppointments(self):
		"""Get a list of all appointments in the local calendar"""
		"""Order is completely arbitrary"""
		events = {}
		for ev in self.log.events:
			if isinstance(ev.op, Appointment):
				events[ev.op.name] = ev.op
			elif isinstance(ev.op, basestring):
				del events[ev.op]
		return [events[n] for n in events]
	
	def addAppointment(self, apt):
		"""Add an appointment to the calendar"""
		"""If other users are a member, they will be invited"""
		if self.checkConflicts(apt):
			raise Exception('conflict')
		self.log.event(apt)
	
	def removeAppointment(self, apt):
		"""Remove an event from the calendar"""
		"""If other users are members, they will be notified"""
		self.log.event(apt.name)
	
	def checkConflicts(self, apt):
		"""Check if an appointment conflicts with the local calendar"""
		for check in self.getAppointments():
			if apt.checkConflict(check):
				return True
		return False
