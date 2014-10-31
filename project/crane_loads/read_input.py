#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 14:03:34 2010

@author: Black

This script holds the data values needed for the calculation of the Crane Loads
The data are cPickled in a file named "ifile.txt"

This file is supposed to be run (double clik) when the crane data are changed

The created (pickled) file is read by a read_data() method defined in Crain_data class
"""

from __future__ import division
from math import exp
import cPickle



class Crane_Loads_Read_Input:
    """
    Στην κλάση αυτή ορίζονται τα χαρακτηριστικά της γερανογέφυρας.
    Καλείται από το βασικό script-άκι
    """
    def __init__(self):
        """
        Στη μέθοδο αυτή γίνεται ο ορισμός των δεδομένων της γερανογέφυρας.

        Με το που δημιουργείται η instance της κλάσης διαβάζονται τα δεδομένα και
        γράφονται σε ένα dictionary με ονομάσία data.
        Στη συνέχεια το dictionary γίνεται cPickled σε ένα αρχείο με όνομα 'ifile.txt'
        """

        data = {}

        # Γεωμετρία
        data["L"] =  15               # Πλάτος γερανογέφυρας σε m
        data["e_min"] = 0.780          # Απόσταση της ακραίας θέσης του άγκιστρου ανάρτησης από τον άξονα της δοκού κύλισης σε m
        data["a"] = 1.6              # Απόσταση μεταξύ των τροχών σε m
        data["br"] = 0.05             # Πλάτος τροχιάς σε m
        data["e"] = data["br"] / 4   # Eκκεντρότητα τροχιάς σε m

        # Φορτία
        data["Gcr"] = 27.27             # Συνολικό φορτίο γερανογέφυρας σε KN (χωρίς το φορείο)
        data["Gtr"] = 2.8              # Φορτίο φορείου σε KN
        data["Gtot"] = float(data["Gcr"]) + float(data["Gtr"])
        data["Qr_nom"] = 32           # Ονομαστικό φορτίο Γερανογέφυρας σε ΚΝ

        # Γενικά χαρακτηριστικά
        data["HC"] = "HC2"             # Κατηγορία ανύψωσης της γερανογέφυρας (Hoisting Class)
        data["fatigue_class"] = "S2"   # Κατηγορία κόπωσης της γερανογέφυρας
        data["rolling_type"] = "IFF"   # Σύστημα κύλισης
        data["m"] = 0                  # Αριθμός coupled τροχών. Για IFF και IFM είναι 0

        data["vh"] = 20./60.            # Ταχύτητα ανύψωσης της γερανογέφυρας σε m/sec
        data["mf"] =  0.2              # Συντελεστής τριβής μ τροχιάς - τροχού
                                        # (0.2 για μέταλλo-μέταλλο ή 0.5 για ελαστικο-μετάλλο)
        data["mw"] =  2                # Πλήθος μεμονωμένων κινητήριων τροχών
        data["nr"] =  2                # Αριθμός δοκών κύλισης

        data["e1"] = 0                              # Απόσταση τροχων 1 από τα μέσα καθοδήγησης
        data["e2"] = data["e1"] + data["a"]        # Απόσταση τροχων 2 από τα μέσα καθοδήγησης

        # Δυναμικοί συντελεστές φ1 ως φ5
        b2, v2, v2_min = self.v2_Function(data["HC"], data["vh"])

        data["b2"] = b2
        data["v2_min"] = v2_min

        data["v1"] = 1.1               # v1_max = 1.1 , v1_min = 0.9
        data["v2"] = v2                # Ανάλογα με το HC και την ταχύτητα
        data["v3"] = 1                 # Το δυσμενέστερο
        data["v4"] = 1                 # Με την προϋπόθεση ότι τηρούνται οι κατασκευαστικές ανοχές
        data["v5"] = 1.5                 # Ανάλογα με το πως μεταβάλλονται οι οριζόντιες δυνάμεις
        data["v6"] = 1                 # Το φορτίο ελέγχου είναι >125% του φορτίου λειτουργίας
        data["vfat"] = self.v_fatigue(data["v1"], data["v2"])
        data["a_rad"] = 0.0015         # Η γωνία που μπαίνει στον υπολογισμό των Hs

        data["lfat_s"], data["lfat_t"] = self.l_fatigue(data["fatigue_class"])

        ifile = open('ifile_Loads.txt', 'w')
        cPickle.dump(data, ifile)
        ifile.close()
