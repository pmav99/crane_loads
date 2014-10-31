#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some constant values from the eurocode

author: Panagiotis Mavrogiorgos
email : gmail, pmav99
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


# fatigue coefficient λ,σ
LS = {
    "S0": 0.198,
    "S1": 0.250,
    "S2": 0.315,
    "S3": 0.397,
    "S4": 0.500,
    "S5": 0.630,
    "S6": 0.794,
    "S7": 1.000,
    "S8": 1.260,
    "S9": 1.587,
}

# fatigue coefficient λ,τ
LT = {
    "S0": 0.379,
    "S1": 0.436,
    "S2": 0.500,
    "S3": 0.575,
    "S4": 0.660,
    "S5": 0.758,
    "S6": 0.871,
    "S7": 1.000,
    "S8": 1.149,
    "S9": 1.320,
}

B2 = {
    "HC1": 0.17,
    "HC2": 0.34,
    "HC3": 0.51,
    "HC4": 0.68,
}

V2_MIN = {
    "HC1": 1.05,
    "HC2": 1.10,
    "HC3": 1.15,
    "HC4": 1.20,
}
