# -*- coding: utf-8 -*-
#
# AWL simulator - utility functions
#
# Copyright 2012-2013 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from awlsim.exceptions import *
from awlsim.enumeration import *

import sys
import os
import random
import struct


# isPyPy is True, if the interpreter is PyPy.
isPyPy = "PyPy" in sys.version

# isPy3Compat is True, if the interpreter is Python 3 compatible.
isPy3Compat = sys.version_info[0] == 3

# isPy2Compat is True, if the interpreter is Python 2 compatible.
isPy2Compat = sys.version_info[0] == 2

# Python 2/3 helper selection
def py23(py2, py3):
	if isPy3Compat:
		return py3
	if isPy2Compat:
		return py2
	raise AwlSimError("Failed to detect Python version")

class Logging(object):
	enum.start
	LOG_NONE	= enum.item
	LOG_ERROR	= enum.item
	LOG_INFO	= enum.item
	LOG_DEBUG	= enum.item
	enum.end

	_loglevel = LOG_INFO

	@classmethod
	def setLoglevel(cls, loglevel):
		if loglevel not in (cls.LOG_NONE,
				    cls.LOG_ERROR,
				    cls.LOG_INFO,
				    cls.LOG_DEBUG):
			raise AwlSimError("Invalid log level '%d'" % loglevel)
		cls._loglevel = loglevel

	@classmethod
	def printDebug(cls, text):
		if cls._loglevel >= cls.LOG_DEBUG:
			sys.stdout.write(text)
			sys.stdout.write("\n")
			sys.stdout.flush()

	@classmethod
	def printInfo(cls, text):
		if cls._loglevel >= cls.LOG_INFO:
			sys.stdout.write(text)
			sys.stdout.write("\n")
			sys.stdout.flush()

	@classmethod
	def printError(cls, text):
		if cls._loglevel >= cls.LOG_ERROR:
			sys.stderr.write(text)
			sys.stderr.write("\n")
			sys.stderr.flush()

def printDebug(text):
	Logging.printDebug(text)

def printInfo(text):
	Logging.printInfo(text)

def printError(text):
	Logging.printError(text)

# Warning message helper
printWarning = printError

def awlFileRead(filename):
	try:
		fd = open(filename, "rb")
		data = fd.read()
		data = data.decode("latin_1")
		fd.close()
	except (IOError, UnicodeError) as e:
		raise AwlParserError("Failed to read '%s': %s" %\
			(filename, str(e)))
	return data

def awlFileWrite(filename, data):
	data = "\r\n".join(data.splitlines()) + "\r\n"
	for count in range(1000):
		tmpFile = "%s-%d-%d.tmp" %\
			(filename, random.randint(0, 0xFFFF), count)
		if not os.path.exists(tmpFile):
			break
	else:
		raise AwlParserError("Could not create temporary file")
	try:
		fd = open(tmpFile, "wb")
		fd.write(data.encode("latin_1"))
		fd.flush()
		fd.close()
		if os.name.lower() != "posix":
			# Can't use safe rename on non-POSIX.
			# Must unlink first.
			os.unlink(filename)
		os.rename(tmpFile, filename)
	except (IOError, OSError, UnicodeError) as e:
		raise AwlParserError("Failed to write file:\n" + str(e))
	finally:
		try:
			os.unlink(tmpFile)
		except (IOError, OSError):
			pass

# Returns the index of a list element, or -1 if not found.
def listIndex(_list, value, start=0, stop=-1):
	if stop < 0:
		stop = len(_list)
	try:
		return _list.index(value, start, stop)
	except ValueError:
		return -1

# Convert an integer list to a human readable string.
# Example: [1, 2, 3]  ->  "1, 2 or 3"
def listToHumanStr(lst, lastSep="or"):
	if not lst:
		return ""
	string = ", ".join(str(i) for i in lst)
	# Replace last comma with 'lastSep'
	string = string[::-1].replace(",", lastSep[::-1] + " ", 1)[::-1]
	return string

def str2bool(string, default=False):
	s = string.lower()
	if s in ("true", "yes", "on", "enable", "enabled"):
		return True
	if s in ("false", "no", "off", "disable", "disabled"):
		return False
	try:
		return bool(int(s, 10))
	except ValueError:
		return default

# Returns value, if value is a list.
# Otherwise returns a list with value as element.
def toList(value):
	if isinstance(value, list):
		return value
	if isinstance(value, tuple):
		return list(value)
	return [ value, ]

def pivotDict(inDict):
	outDict = {}
	for key, value in inDict.items():
		if value in outDict:
			raise KeyError("Ambiguous key in pivot dict")
		outDict[value] = key
	return outDict
