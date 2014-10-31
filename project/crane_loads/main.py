#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import cPickle
from crane_loads_read_input import Crane_Loads_Read_Input
from crane_loads_print_input import Crane_Loads_Print_Input
from crane_loads_calculate_forces import Calculate_Crane_Forces

class Crane_Loads:
    """
    Η βασική κλάση του υπολογισμού των φορτίων της γερανογέφυρας
    """
    def __init__(self):
        """
        Μέσα από τη μέθοδο __init__, με τη δημιουργία της instance της κλάσης, 
        γίνεται ο υπολογισμός των φορτίων της Γερανογέφυρας.
        """
        # Δημιουργία μιας instance της Crane_Loads_Read_Input() για να διαβαστούν
        # τα δεδομένα και στη συνέχεια να γίνουν pickle
        read_loads_input = Crane_Loads_Read_Input()
        
        # Εκτύπωση των δεδομένων
        print_loads_input = Crane_Loads_Print_Input()

        forces = Calculate_Crane_Forces()
            
#        print("Serviceability Limit States")
#        forces.Print_V_Table(Qr_min_1, Qr_min_2, Qr_min_3, Qr_min_4, Qr_min_5, \
#            Qr_max_1, Qr_max_2, Qr_max_3, Qr_max_4, Qr_max_5, H_1, H_1, H_4, H_4, H_4)

if __name__ == "__main__":
    # Redirecting stdout to a file named out.txt
#    cwd = os.curdir
#    sys.stdout = open(os.path.join(cwd, 'ofile_Loads.txt'), mode='w')
    
    crane_loads = Crane_Loads()
    
    os.system("xelatex -interaction=nonstopmode crane_loads.tex")
