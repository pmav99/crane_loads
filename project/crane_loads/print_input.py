#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
#from __future__ import print_function
from __future__ import division
from math import exp
import cPickle

class Crane_Loads_Print_Input:
    """
    Στην κλάση αυτή υπάρχουν οι συναρτήσεις για την εκτύπωση των δεδομένων
    """
    def __init__(self):
        """
        Με το που δημιουργείται η instance της κλάσης εκτυπώνονται τα δεδομένα
        από το αρχείο "ifile_Loads.txt"
        """
        # Άνοιγμα του cPickled αρχείου των δεδομένων και εγγραφή τους στο i_dict
        i_file = open("ifile_Loads.txt","r")
        i_dict = cPickle.load(i_file)

        # Διάβασμα των δεδομένων από το dictionary. Η περιγραφή των δεδομένων
        # υπάρχει στο crain_input.py
        L   = i_dict["L"]
        e_min   = i_dict["e_min"]
        a = i_dict["a"]
        br = i_dict["br"]
        e = i_dict["e"]
        Gcr = i_dict["Gcr"]
        Gtr = i_dict["Gtr"]
        Gtot = i_dict["Gtot"]
        Qr_nom = i_dict["Qr_nom"]
        HC = i_dict["HC"]
        fatigue_class = i_dict["fatigue_class"]
        rolling_type = i_dict["rolling_type"]
        vh = i_dict["vh"]
        mf = i_dict["mf"]
        mw = i_dict["mw"]
        nr = i_dict["nr"]
        e1 = i_dict["e1"]
        e2 = i_dict["e2"]
        a_rad = i_dict["a_rad"]
        m = i_dict["m"]
        b2 = i_dict["b2"]
        v2_min = i_dict["v2_min"]
        v1 = i_dict["v1"]
        v2 = i_dict["v2"]
        v3 = i_dict["v3"]
        v4 = i_dict["v4"]
        v5 = i_dict["v5"]
        v6 = i_dict["v6"]

        # Διάβασμα του template αρχείου *.tex και αποθήκευση του στην "s"
        file = open("crane_loads_input_raw.tex","r")
        s = file.read()
        file.close()
        s
        # Αντικατάσταση των λέξεων κλειδιών της "s"
        s = s.replace("fatigue_class--", "{0:s}".format(fatigue_class))
        s = s.replace("rolling_type--", "{0:s}".format(rolling_type))
        s = s.replace("nr--", "{0:d}".format(nr))
        s = s.replace("mw--", "{0:d}".format(mw))
        s = s.replace("mf--", "{0:.3f}".format(mf))
        s = s.replace("HC--", "{0:s}".format(HC))
        s = s.replace("v2_min--", "{0:.3f}".format(v2_min))
        s = s.replace("b2--", "{0:.3f}".format(b2))
        s = s.replace("vh--", "{0:.3f}".format(vh))

        s = s.replace("Gcr--" , "{0:6.3f}".format(Gcr))
        s = s.replace("Gtr--" , "{0:6.3f}".format(Gtr))
        s = s.replace("Gtot--", "{0:6.3f}".format(Gtot))
        s = s.replace("Qr_nom--", "{0:6.3f}".format(Qr_nom))

        s = s.replace("L--", "{0:5.3f}".format(L))
        s = s.replace("e_min--", "{0:5.3f}".format(e_min))
        s = s.replace("a--", "{0:5.3f}".format(a))
        s = s.replace("e1--", "{0:5.3f}".format(e1))
        s = s.replace("e2--", "{0:5.3f}".format(e2))
        s = s.replace("a_rad--", "{0:5.4f}".format(a_rad))

        s = s.replace("v1--", "{0:4.3f}".format(v1))
        s = s.replace("v2--", "{0:4.3f}".format(v2))
        s = s.replace("v3--", "{0:4.3f}".format(v3))
        s = s.replace("v4--", "{0:4.3f}".format(v4))
        s = s.replace("v5--", "{0:4.3f}".format(v5))
        s = s.replace("v6--", "{0:4.3f}".format(v6))


        # Εγγραφή της "s" στο αρχείο που διαβάζει το master file του LaTeX
        file = open("crane_loads_input.tex","w")
        file.write(s)
        file.close()

