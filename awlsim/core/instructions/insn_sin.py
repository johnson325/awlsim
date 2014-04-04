# -*- coding: utf-8 -*-
#
# AWL simulator - instructions
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

from awlsim.core.instructions.main import *


class AwlInsn_SIN(AwlInsn):
	def __init__(self, cpu, rawInsn):
		AwlInsn.__init__(self, cpu, AwlInsn.TYPE_SIN, rawInsn)
		self.assertOpCount(0)

	def run(self):
		accu1 = math.sin(self.cpu.accu1.getPyFloat())
		for extremum in (-1.0, 0.0, 1.0):
			if pyFloatEqual(accu1, extremum):
				accu1 = extremum
		self.cpu.accu1.setPyFloat(accu1)
		self.cpu.statusWord.setForFloatingPoint(accu1)