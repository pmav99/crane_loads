#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file can act as input data for the calculation of the crane loads.

Some of the data are derived from the other values. If you want to give
them values yourself, just comment out the lines that calculate them
and type the values you need.

author: Panagiotis Mavrogiorgos
email : gmail, pmav99
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from crane_loads import tables

### Geometry
# L     :
# e_min :
# a     :
# br    :
# e     :
L       = 15
e_min   = 0.78
a       = 1.6
br      = 0.05
e       = br / 4

### Loads
# G,cr      :
# G,tr      :
# T,tot     :
# Qr,nom    :
Gcr     = 27.27
Gtr     = 2.8
Gtot    = Gcr + Gtr
Qr_nom  = 32

### General
# HC : Hoisting class
# FC : fatigue class
# RT : rolling type
# m  :
HC = "HC2"
FC = "S2"
RT = "IFF"
m = 0

vh = 20 / 60
mf = 0.2
mw = 2
nr = 2
e1 = 0
e2 = e1 + a

### Dynamic coefficients
b2 = tables.B2[HC]
v2_min = tables.V2_MIN[HC]

v1 = 1.1
v2 = v2_min + b2 * vh
v3 = 1
v4 = 1
v5 = 1.5
v6 = 1
vfat = max((1 + v1) / 2, (1 + v2) / 2)
a_rad = 0.0015

ls = tables.LS[FC]
lt = tables.LT[FC]
