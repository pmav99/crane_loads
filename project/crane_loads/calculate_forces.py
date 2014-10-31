#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import


from math import exp
import subprocess


class Calculate_Crane_Forces():
    """
    Η κλάση αυτή περιέχει τις μεθόδους που χρησιμοποιούνται για τον υπολογισμό
    των φορτίων της γερανογέφυρας
    """
    def __init__(self):
        """
        Με το που γίνεται initialization της instance, διαβάζονται τα δεδομένα
        της γερανογέφυρας και στη συνέχεια καλούνται οι συναρτήσεις για τον
        υπολογισμό της. Στη συνέχεια καλούνται οι συναρτήσεις για την εκτύπωση
        των αποτελεσμάτων.
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
        Qr_nom = i_dict["Qr_nom"]
        HC = i_dict["HC"]
        FC = i_dict["FC"]
        RT = i_dict["RT"]
        vh = i_dict["vh"]
        mf = i_dict["mf"]
        mw = i_dict["mw"]
        nr = i_dict["nr"]
        m = i_dict["m"]
        e1 = i_dict["e1"]
        e2 = i_dict["e2"]
        a_rad = i_dict["a_rad"]
        v1 = i_dict["v1"]
        v2 = i_dict["v2"]
        v3 = i_dict["v3"]
        v4 = i_dict["v4"]
        v5 = i_dict["v5"]
        v6 = i_dict["v6"]
        vfat = i_dict["vfat"]
        lfat_s = i_dict["lfat_s"]
        lfat_t = i_dict["lfat_t"]

        # Υπολογισμός των κατακόρυφων φορτίων για κάθε συνδυασμό.
        # Τα φορτία αποθηκεύονται σε dictionaries με όνομα v_out$
        v_out1 = self.calc_Qr(v1, v2, Gcr, Gtr, Qr_nom, L, e_min)
        v_out2 = self.calc_Qr(v1, v3, Gcr, Gtr, Qr_nom, L, e_min)
        v_out3 = self.calc_Qr(1 , 0,  Gcr, Gtr, Qr_nom, L, e_min)
        v_out4 = self.calc_Qr(v4, v4, Gcr, Gtr, Qr_nom, L, e_min)
        v_out5 = v_out4

        # Υπολογισμός των οριζόντιων φορτίων Ht για τους συνδυασμούς 1 και 4
        # Τα φορτία αποθηκεύονται σε dictionaries με όνομα Ηt_out$
        Ht_out1 = self.calc_Ht(L, a, v_out1["SQr_MAX"], v_out1["SQr_MIN"], v_out1["Qr_min"], mf, mw, v5, nr)
        Ht_out4 = self.calc_Ht(L, a, v_out4["SQr_MAX"], v_out4["SQr_MIN"], v_out4["Qr_min"], mf, mw, v5, nr)

        # Υπολογισμός των οριζόντιων φορτίων Hs για τους συνδυασμούς 1 και 5
        # Τα φορτία αποθηκεύονται σε dictionary με όνομα Ηs_out$
        Hs_out = self.calc_Hs(RT, L, nr, e1, e2, m, v_out5["SQr_MAX"], v_out5["SQr_MIN"], a_rad=0.015)

        # Υπολογισμός του φορτίου κόπωσης
        fat_out = self.calc_fatigue(Gcr, Gtr, Qr_nom, L, e_min, lfat_s, lfat_t, vfat)

        self.print_greek(v_out1, v_out2, v_out3, v_out4, v_out5, Ht_out1, Ht_out4, Hs_out, fat_out, vfat, lfat_s, lfat_t, a_rad, RT, FC)

    def print_greek(self, v_out1, v_out2, v_out3, v_out4, v_out5, Ht_out1, Ht_out4, Hs_out, fat_out, vfat, lfat_s, lfat_t, a_rad, RT, FC):

        # Διάβασμα του template αρχείου *.tex και αποθήκευση του στην "s"
        s = self.read_file("crane_loads_forces_raw.tex")

        # Εκτύπωση των κατακόρυφων φορτίων.
        s = self.print_Qr(s, v_out1)
        s = self.print_Qr(s, v_out2)
        s = self.print_Qr(s, v_out3)
        s = self.print_Qr(s, v_out4)

        # Εκτύπωση των οριζόντιων φορτίων
        s = self.print_Ht(s, Ht_out1)
        s = self.print_Ht(s, Ht_out4)

        s = self.choose_file(s, Hs_out, a_rad, RT)

        # Εγγραφή της s στο αρχείο *.tex
        self.write_to_file(s, "crane_loads_forces.tex")

        s = self.read_file("table_raw.tex")
        s = self.print_table(s, v_out1, v_out2, v_out3, v_out4, v_out5,
                             Ht_out1, Ht_out4, Hs_out)
        s = self.write_to_file(s, "table.tex")

        s = self.read_file("fatigue_raw.tex")
        s = self.print_fatigue(s, fat_out, vfat, lfat_s, lfat_t, FC)
        s = self.write_to_file(s, "fatigue.tex")

    def choose_file(self, s, Hs_out, a_rad, RT):
        raw_file = RT + "_raw.tex"
        tex_file = RT + ".tex"
        str = self.read_file(raw_file)
        str = self.print_Hs(str, Hs_out, a_rad)
        self.write_to_file(str, tex_file)
        s += "\input{./" + tex_file + "}"
        return s

    def read_file(self, filename):
        file = open(filename, "r")
        s = file.read()
        file.close()
        return s

    def write_to_file(self, str, filename):
        file = open(filename, "w")
        file.write(str)
        file.close()

    def calc_fatigue(self, Gcr, Gtr, Qr, L, e_min, lfat_s, lfat_t, vfat):
        """
        Η συνάρτηση αυτή υπολογίζει τα φορτία κόπωσης της γερανογέφυρας για
        ορθές και διατμητικές τάσεις.
        """
        SQmax_i = 0.5 * Gcr + (Gtr + Qr) * (L-e_min)/L     # Δυσμενής άξονας
        Qmax_i  = SQmax_i / 2

        Qes = vfat * lfat_s * Qmax_i
        Qet = vfat * lfat_t * Qmax_i

        out = {"SQmax_i":SQmax_i}
        out["Qmax_i"] = Qmax_i
        out["Qes"] = Qes
        out["Qet"] = Qet

        return out

    def calc_Ht(self, L, a, SQr_MAX, SQr_MIN, Qr_min, mf, mw, v5, nr):
        """
        Η συνάρτηση αυτή υπολογίζει τις οριζόντιες (εγκάρσιες και κατά μήκος)
        δυνάμεις που ασκούνται στη δοκό κύλισης εξαιτίας της επιτάχυνσης της
        γερανογέφυρας.

        L : το μήκος της γερανογέφυρας.
        a : η απόσταση μεταξύ των τροχών.
        Qmax : η λίστα με τα φορτία που αντιστοιχουν στην περισσότερο φορτισμένη
               δοκό κυλισης.
        Qmin : η λίστα με τα φορτία που αντιστοιχουν στη λιγότερο φορτισμένη
               δοκό κυλισης.
        mf : ο συντελεστής τριβής μ.
        mw : το πλήθος μεμονωμένων κινητήριων τροχών.
        v5 : ο δυναμικός συντελεστής φ5.
        nr : ο αριθμός δοκών κύλισης.

        SQr_max : το συνολικό φορτίο που αντιστοιχεί στην περισσότερο φορτισμένη
                  δοκό κυλισης.
        SQr_min : το συνολικό φορτίο που αντιστοιχεί στη λιγότερο φορτισμένη
                  δοκό κυλισης.
        Qr_min : το φορτίο που αντιστοιχει΄στον ένα τροχό της λιγότερο
                 φορτισμένης δοκού κύλισης.

        Κ : η κινητήρια δύναμη.
        """
        # Επειδή τα απαραίτητα φορτία δίνονται μέσα σε μια λίστα, εξάγουμε τα
        # φορτία που μας ενδιαφέρουν

        K = mf * mw * Qr_min
        HL = HL_1 = HL_2 = v5 * K / (nr)
        ksi1 = SQr_MAX / (SQr_MAX + SQr_MIN)
        ksi2 = 1 - ksi1
        Ls = (ksi1 - 0.5) * L
        M = K * Ls
        HT_1 = v5 * ksi2 * M / a
        HT_2 = v5 * ksi1 * M / a

        return locals()

    def calc_Qr(self, v_sw, v_hl, Gcr, Gtr, Qnom, L, e_min):
        """
        Η μέθοδος αυτή υπολογίζει τα κατακόρυφα φορτία που ασκούνται από τη
        γερανογέφυρα στη δοκό κυλίσεως. Οι υπολογισμοί γίνονται τόσο για τα
        ελάχιστα όσο και για τα μέγιστα φορτία.

        v_sw (selfweight) : ο δυναμικός συντελεστής φ για τον υπολογισμό του
                            ιδίου βάρους της γερανογέφυρας (πρακτικά φ1 για
                            ομάδες φορτίων 1, 2 και 8, φ4 για ομάδες φορτίων
                            4, 5 και 6 και μονάδα για τις υπόλοιπες.
        v_hl (hoist load) : ο δυναμικός συντελεστής για το ανυψούμενο φορτίο.
        L : το μήκος της γερανογέφυρας.
        e_min : η απόσταση της ακραίας θέσης του άγκιστρου ανάρτησης από τον
                άξονα της δοκού κύλισης.
        Gcr : το ίδιο βάρος του φορέα (χωρίς το φορείο).
        Gtr : το ίδιο βάρος του φορείου (συγκεντρωμένο φορτίο).
        Qr_nom : το φορτίο που φέρει η γερανογέφυρα.

        H μέθοδος επιστρέφει ένα dictionary με τις τιμές.
        """
        Gcr_v = Gcr * v_sw
        Gtr_v = Gtr * v_sw
        # Αφόρτιση γερανογέφυρα
        SQr_max = 0.5 * Gcr_v + Gtr_v * (L-e_min)/L     # Δυσμενής άξονας
        Qr_max = SQr_max / 2                            # Δυσμενής τροχός
        SQr_min = 0.5 * Gcr_v + Gtr_v * e_min/L         # Ευμενής άξονας
        Qr_min = SQr_min / 2                            # Ευμενής τροχός
        # Φορτισμένη γερανογέφυρα
        Qh = v_hl * Qnom
        SQr_MAX = 0.5 * Gcr_v + (Gtr_v + Qh) * (L-e_min)/L   # Δυσμενής άξονας
        Qr_MAX = SQr_MAX / 2                                 # Δυσμενής τροχός
        SQr_MIN = 0.5 * Gcr_v + (Gtr_v + Qh) * e_min/L       # Ευμενής άξονας
        Qr_MIN = SQr_MIN / 2                                 # Ευμενής τροχός

        return locals()

    def calc_Hs(self, RT, L, n, e1, e2, m, SQr_max, SQr_min, a_rad=0.015):
        """
        Αυτή η μέθοδος κάνει τον υπολογισμό των οριζόντιων φορτίων λόγω της
        παράγωγης κίνησης της γερανογέφυρας.
        """
        SQr = SQr_max + SQr_min

        ksi1 = SQr_max / SQr
        ksi2 = 1 - ksi1
        f = 0.3*(1-exp(-250*a_rad))

        if RT.endswith('FF'):
            h = (m * ksi1 * ksi2 * L**2 + e1**2 + e2**2)/(e1 + e2)
        elif RT.endswith('FM'):
            h = (m * ksi1 * L**2 + e1**2 + e2**2)/(e1 + e2)

        if RT == ("IFF"):
            l_s = 1 - (e1 + e2) / (n * h)
            l_s11L = 0
            l_s12L = 0
            l_s21L = 0
            l_s22L = 0
            l_s11T = (ksi2 / n) * (1 - e1 / h)
            l_s12T = (ksi2 / n) * (1 - e2 / h)
            l_s21T = (ksi1 / n) * (1 - e1 / h)
            l_s22T = (ksi1 / n) * (1 - e2 / h)
        elif RT == ("CFF"):
            l_s = 1 - (e1 + e2) / (n * h)
            l_s11L = (ksi1 * ksi2 * L) / (n * h)
            l_s12L = (ksi1 * ksi2 * L) / (n * h)
            l_s21L = (ksi1 * ksi2 * L) / (n * h)
            l_s22L = (ksi1 * ksi2 * L) / (n * h)
            l_s11T = (ksi2 / n) * (1 - e1 / h)
            l_s12T = (ksi2 / n) * (1 - e2 / h)
            l_s21T = (ksi1 / n) * (1 - e1 / h)
            l_s22T = (ksi1 / n) * (1 - e2 / h)
        elif RT == ("IFM"):
            l_s = ksi2 * (1 - (e1 + e2) / (n * h))
            l_s11L = 0
            l_s12L = 0
            l_s21L = 0
            l_s22L = 0
            l_s11T = (ksi2 / n) * (1 - e1 / h)
            l_s12T = (ksi2 / n) * (1 - e2 / h)
            l_s21T = 0
            l_s22T = 0
        elif RT == ("CFM"):
            l_s = ksi2 * (1 - (e1 + e2) / (n * h))
            l_s11L = (ksi1 * ksi2 * L) / (n * h)
            l_s12L = (ksi1 * ksi2 * L) / (n * h)
            l_s21L = (ksi1 * ksi2 * L) / (n * h)
            l_s22L = (ksi1 * ksi2 * L) / (n * h)
            l_s11T = (ksi2 / n) * (1 - e1 / h)
            l_s12T = (ksi2 / n) * (1 - e2 / h)
            l_s21T = 0
            l_s22T = 0

        S = f * l_s * SQr
        H_s11L = f * l_s11L * SQr
        H_s12L = f * l_s12L * SQr
        H_s21L = f * l_s21L * SQr
        H_s22L = f * l_s22L * SQr
        H_s11T = f * l_s11T * SQr
        H_s12T = f * l_s12T * SQr
        H_s21T = f * l_s21T * SQr
        H_s22T = f * l_s22T * SQr

        out = {"SQr":SQr}
        out["ksi1"] = ksi1
        out["ksi2"] = ksi2
        out["f"] = f
        out["h"] = h
        out["l_s"] = l_s
        out["l_s11L"] = l_s11L
        out["l_s12L"] = l_s12L
        out["l_s21L"] = l_s21L
        out["l_s22L"] = l_s22L
        out["l_s11T"] = l_s11T
        out["l_s12T"] = l_s12T
        out["l_s21T"] = l_s21T
        out["l_s22T"] = l_s22T
        out["S"] = S
        out["H_s11L"] = H_s11L
        out["H_s12L"] = H_s12L
        out["H_s21L"] = H_s21L
        out["H_s22L"] = H_s22L
        out["H_s11T"] = H_s11T
        out["H_s12T"] = H_s12T
        out["H_s21T"] = H_s21T
        out["H_s22T"] = H_s22T

        out["H_s1T"] = H_s11T - S
        out["H_s2T"] = H_s21T
        return out

    def print_Qr(self, s, out):
        """
        H συνάρτηση αυτή τυπώνει τα αποτελέσματα των κατακόρυφων φορτίων.

        s είναι το string με το αρχείο tex και out είναι το dictionary με τα
        αποτελέσματα των υπολογισμών.

        με πεζά γράμματα (max, min) είναι η αφόρτιστη γερανογέφυρα
        με κεφαλαία γράμματα (ΜΑΧ, ΜΙΝ) είναι η φορτισμένη γερανογέφρυα
        """

        s = s.replace("Gcr_v--" , "{0:6.2f}".format(out["Gcr_v"]), 1)
        s = s.replace("Gtr_v--" , "{0:6.2f}".format(out["Gtr_v"]), 1)
        s = s.replace("Q_h--"   , "{0:6.2f}".format(out["Qh"]), 1)

        s = s.replace("SQr_max--" , "{0:6.2f}".format(out["SQr_max"]), 1)
        s = s.replace("Qr_max--" , "{0:6.2f}".format(out["Qr_max"]), 1)
        s = s.replace("SQr_min--"   , "{0:6.2f}".format(out["SQr_min"]), 1)
        s = s.replace("Qr_min--"   , "{0:6.2f}".format(out["Qr_min"]), 1)

        s = s.replace("SQr_MAX--" , "{0:6.2f}".format(out["SQr_MAX"]), 1)
        s = s.replace("Qr_MAX--" , "{0:6.2f}".format(out["Qr_MAX"]), 1)
        s = s.replace("SQr_MIN--"   , "{0:6.2f}".format(out["SQr_MIN"]), 1)
        s = s.replace("Qr_MIN--"   , "{0:6.2f}".format(out["Qr_MIN"]), 1)

        return s

    def print_fatigue(self, s, out, vfat, lfat_s, lfat_t, FC):
        """
        H συνάρτηση αυτή τυπώνει τα αποτελέσματα τoυ φορτίου κόπωσης

        s είναι το string με το αρχείο tex και out είναι το dictionary με τα
        αποτελέσματα των υπολογισμών.
        """
        s = s.replace("SQmax_i--"   , "{0:6.2f}".format(out["SQmax_i"]), 1)
        s = s.replace("Qmax_i--"  , "{0:6.2f}".format(out["Qmax_i"]), 2)
        s = s.replace("vfat--", "{0:6.2f}".format(vfat), 1)
        s = s.replace("FC--", "{0}".format(FC), 1)
        s = s.replace("lfat_s--", "{0:6.2f}".format(lfat_s), 1)
        s = s.replace("lfat_t--", "{0:6.2f}".format(lfat_t), 1)
        s = s.replace("Qes--"   , "{0:6.2f}".format(out["Qes"]), 1)
        s = s.replace("Qet--"   , "{0:6.2f}".format(out["Qet"]), 1)

        return s

    def print_Ht(self, s, out):
        """
        H συνάρτηση αυτή τυπώνει τα αποτελέσματα των οριζόντιων φορτίων Ηt

        s είναι το string με το αρχείο tex και out είναι το dictionary με τα
        αποτελέσματα των υπολογισμών.
        """

        s = s.replace("K--"   , "{0:6.2f}".format(out["K"]), 1)
        s = s.replace("HL--"  , "{0:6.2f}".format(out["HL"]), 2)
        s = s.replace("ksi1--", "{0:6.2f}".format(out["ksi1"]), 1)
        s = s.replace("ksi2--", "{0:6.2f}".format(out["ksi2"]), 1)
        s = s.replace("Ls--"  , "{0:6.2f}".format(out["Ls"]), 1)
        s = s.replace("M--"   , "{0:6.2f}".format(out["M"]), 1)
        s = s.replace("HT_1--", "{0:6.2f}".format(out["HT_1"]), 1)
        s = s.replace("HT_2--", "{0:6.2f}".format(out["HT_2"]), 1)

        return s

    def print_Hs(self, s, out, a_rad):
        """
        Η μέθοδος αυτή εκτυπώνει τα υπόλοιπα αποτελέσματα από τον υπολογισμός
        """

        s = s.replace("SQr--"   , "{0:6.2f}".format(out["SQr"]), 1)
        s = s.replace("ksi1--"  , "{0:6.2f}".format(out["ksi1"]), 1)
        s = s.replace("ksi2--"  , "{0:6.2f}".format(out["ksi2"]), 1)
        s = s.replace("a_rad--" , "{0:6.4f}".format(a_rad), 1)
        s = s.replace("f--"     , "{0:6.2f}".format(out["f"]), 1)

        s = s.replace("h--"      , "{0:6.2f}".format(out["h"]), 1)
        s = s.replace("l_s--"      , "{0:6.2f}".format(out["l_s"]), 1)
        s = s.replace("l_s11L--" , "{0:6.2f}".format(out["l_s11L"]), 1)
        s = s.replace("l_s21L--" , "{0:6.2f}".format(out["l_s21L"]), 1)
        s = s.replace("l_s12L--" , "{0:6.2f}".format(out["l_s12L"]), 1)
        s = s.replace("l_s22L--" , "{0:6.2f}".format(out["l_s22L"]  ), 1)
        s = s.replace("l_s11T--" , "{0:6.2f}".format(out["l_s11T"]), 1)
        s = s.replace("l_s21T--" , "{0:6.2f}".format(out["l_s12T"]), 1)
        s = s.replace("l_s12T--" , "{0:6.2f}".format(out["l_s21T"]), 1)
        s = s.replace("l_s22T--" , "{0:6.2f}".format(out["l_s22T"]), 1)

        s = s.replace("S--"      , "{0:6.2f}".format(out["S"]), 1)
        s = s.replace("H_s11L--" , "{0:6.2f}".format(out["H_s11L"]), 1)
        s = s.replace("H_s21L--" , "{0:6.2f}".format(out["H_s21L"]), 1)
        s = s.replace("H_s12L--" , "{0:6.2f}".format(out["H_s12L"]), 1)
        s = s.replace("H_s22L--" , "{0:6.2f}".format(out["H_s22L"]), 1)
        s = s.replace("H_s11T--" , "{0:6.2f}".format(out["H_s11T"]), 1)
        s = s.replace("H_s21T--" , "{0:6.2f}".format(out["H_s21T"]), 1)
        s = s.replace("H_s12T--" , "{0:6.2f}".format(out["H_s12T"]), 1)
        s = s.replace("H_s22T--" , "{0:6.2f}".format(out["H_s22T"]), 1)

        s = s.replace("H_s1T--"  , "{0:6.2f}".format(out["H_s1T"] ), 1)
        s = s.replace("H_s21T--" , "{0:6.2f}".format(out["H_s2T"]), 1)
        return s

    def print_table(self, s, v_out1, v_out2, v_out3, v_out4, v_out5, Ht_out1, Ht_out4, Hs_out):
        """
        s είναι το αρχείο *_raw.tex
        """

        # SLS
        s = s.replace("QMIN_1--", "{0:6.2f}".format(v_out1["Qr_MIN"]), 1)
        s = s.replace("Qmin_1--", "{0:6.2f}".format(v_out1["Qr_min"]), 1)
        s = s.replace("QMAX_1--", "{0:6.2f}".format(v_out1["Qr_MAX"]), 1)
        s = s.replace("Qmax_1--", "{0:6.2f}".format(v_out1["Qr_max"]), 1)
        s = s.replace("QMIN_2--", "{0:6.2f}".format(v_out2["Qr_MIN"]), 1)
        s = s.replace("Qmin_2--", "{0:6.2f}".format(v_out2["Qr_min"]), 1)
        s = s.replace("QMAX_2--", "{0:6.2f}".format(v_out2["Qr_MAX"]), 1)
        s = s.replace("Qmax_2--", "{0:6.2f}".format(v_out2["Qr_max"]), 1)
        s = s.replace("Qmax_3--", "{0:6.2f}".format(v_out3["Qr_MIN"]), 1)
        s = s.replace("Qmin_3--", "{0:6.2f}".format(v_out3["Qr_min"]), 1)
        s = s.replace("QMIN_4--", "{0:6.2f}".format(v_out4["Qr_MIN"]), 1)
        s = s.replace("Qmin_4--", "{0:6.2f}".format(v_out4["Qr_min"]), 1)
        s = s.replace("QMAX_4--", "{0:6.2f}".format(v_out4["Qr_MAX"]), 1)
        s = s.replace("Qmax_4--", "{0:6.2f}".format(v_out4["Qr_max"]), 1)
        s = s.replace("QMIN_5--", "{0:6.2f}".format(v_out5["Qr_MIN"]), 1)
        s = s.replace("Qmin_5--", "{0:6.2f}".format(v_out5["Qr_min"]), 1)
        s = s.replace("QMAX_5--", "{0:6.2f}".format(v_out5["Qr_MAX"]), 1)
        s = s.replace("Qmax_5--", "{0:6.2f}".format(v_out5["Qr_max"]), 1)

        s = s.replace("HL_1--" , "{0:6.2f}".format(Ht_out1["HL"]), 4)
        s = s.replace("HT1_1--", "{0:6.2f}".format(Ht_out1["HT_1"]), 2)
        s = s.replace("HT2_1--", "{0:6.2f}".format(Ht_out1["HT_2"]), 2)
        s = s.replace("HL_4--" , "{0:6.2f}".format(Ht_out4["HL"]), 4)
        s = s.replace("HT1_4--", "{0:6.2f}".format(Ht_out4["HT_1"]), 2)
        s = s.replace("HT2_4--", "{0:6.2f}".format(Ht_out4["HT_2"]), 2)

        s = s.replace("HS1_5--", "{0:6.2f}".format(Hs_out["H_s1T"]), 1)
        s = s.replace("HS2_5--", "{0:6.2f}".format(Hs_out["H_s2T"]), 1)


        # ULS
        g = 1.35
        s = s.replace("QMIN_1--", "{0:6.2f}".format(g * v_out1["Qr_MIN"]), 1)
        s = s.replace("Qmin_1--", "{0:6.2f}".format(g * v_out1["Qr_min"]), 1)
        s = s.replace("QMAX_1--", "{0:6.2f}".format(g * v_out1["Qr_MAX"]), 1)
        s = s.replace("Qmax_1--", "{0:6.2f}".format(g * v_out1["Qr_max"]), 1)
        s = s.replace("QMIN_2--", "{0:6.2f}".format(g * v_out2["Qr_MIN"]), 1)
        s = s.replace("Qmin_2--", "{0:6.2f}".format(g * v_out2["Qr_min"]), 1)
        s = s.replace("QMAX_2--", "{0:6.2f}".format(g * v_out2["Qr_MAX"]), 1)
        s = s.replace("Qmax_2--", "{0:6.2f}".format(g * v_out2["Qr_max"]), 1)
        s = s.replace("Qmax_3--", "{0:6.2f}".format(g * v_out3["Qr_MIN"]), 1)
        s = s.replace("Qmin_3--", "{0:6.2f}".format(g * v_out3["Qr_min"]), 1)
        s = s.replace("QMIN_4--", "{0:6.2f}".format(g * v_out4["Qr_MIN"]), 1)
        s = s.replace("Qmin_4--", "{0:6.2f}".format(g * v_out4["Qr_min"]), 1)
        s = s.replace("QMAX_4--", "{0:6.2f}".format(g * v_out4["Qr_MAX"]), 1)
        s = s.replace("Qmax_4--", "{0:6.2f}".format(g * v_out4["Qr_max"]), 1)
        s = s.replace("QMIN_5--", "{0:6.2f}".format(g * v_out5["Qr_MIN"]), 1)
        s = s.replace("Qmin_5--", "{0:6.2f}".format(g * v_out5["Qr_min"]), 1)
        s = s.replace("QMAX_5--", "{0:6.2f}".format(g * v_out5["Qr_MAX"]), 1)
        s = s.replace("Qmax_5--", "{0:6.2f}".format(g * v_out5["Qr_max"]), 1)

        s = s.replace("HL_1--" , "{0:6.2f}".format(g * Ht_out1["HL"]), 4)
        s = s.replace("HT1_1--", "{0:6.2f}".format(g * Ht_out1["HT_1"]), 2)
        s = s.replace("HT2_1--", "{0:6.2f}".format(g * Ht_out1["HT_2"]), 2)
        s = s.replace("HL_4--" , "{0:6.2f}".format(g * Ht_out4["HL"]), 4)
        s = s.replace("HT1_4--", "{0:6.2f}".format(g * Ht_out4["HT_1"]), 2)
        s = s.replace("HT2_4--", "{0:6.2f}".format(g * Ht_out4["HT_2"]), 2)

        s = s.replace("HS1_5--", "{0:6.2f}".format(g * Hs_out["H_s1T"]), 1)
        s = s.replace("HS2_5--", "{0:6.2f}".format(g * Hs_out["H_s2T"]), 1)
        return s
