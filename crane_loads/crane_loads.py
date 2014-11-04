#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Panagiotis Mavrogiorgos
# email : gmail, pmav99

"""
Calculate crane Loads according to Eurocode 1991-2
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import logging
import numbers
import subprocess

from math import exp
from collections import namedtuple


# In the code we follow these conventions:
#       ABC#    : The "#" corresponds to the combination index.
#       ABC_#   # The "#" corresponds to the rail index (1 or 2).


QR = namedtuple("QR", "Gcr_v Gtr_v Qh SQr_MIN Qr_MIN SQr_min Qr_min SQr_MAX Qr_MAX SQr_max Qr_max")
HT = namedtuple("HT", "K HL ksi1 ksi2 Ls M HT_1 HT_2")

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


class CraneError(ValueError):
    pass


class CraneLoads(object):
    # necessary input
    _mandatory_values = set(
        """
        HC FC RT mf nr mw m
        L e1 e_min a br a_rad
        g Gcr Gtr Qr_nom vh
        v1 v3 v4 v5 v6
        """.split()
    )

    def __init__(self, data):
        """
        data: A dictionary containing all the necessary input

        """
        self.logger = logging.getLogger().getChild("cranes")
        self.data = d = data
        self._validate_input()

        # calc derived input
        d["e"] = d["br"] / 4
        d["Gtot"] = d["Gcr"] + d["Gtr"]
        d["e2"] = d["e1"] + d["a"]
        d["b2"] = B2[d["HC"]]
        d["v2_min"] = V2_MIN[d["HC"]]
        d["v2"] = d["v2_min"] + d["b2"] * d["vh"]
        d["vfat"] = max((1 + d["v1"]) / 2, (1 + d["v2"]) / 2)
        d["lfat_s"] = LS[d["FC"]]
        d["lfat_t"] = LT[d["FC"]]

    def _validate_input(self):
        """ Assert that all the necessary input is present. """
        missing = []
        input_ = self.data.keys()
        for name in self._mandatory_values:
            if name not in input_:
                missing.append(name)
        if missing:
            msg = "Input is missing mandatory data: %s" % ", ".join(missing)
            self.logger.error(msg)
            raise CraneError(msg)

    def calc(self):
        self.calc_Qr()
        self.calc_Ht()
        self.calc_Hs()
        self.calc_fatigue()

    @classmethod
    def from_module(cls, module_name):
        """ Load input from the given python module. """
        logger = logging.getLogger().getChild("input")
        logger.info("Instantiating from module: %r", os.path.abspath(module_name))
        input_module = __import__(os.path.splitext(module_name)[0])

        # Get the variables from the input file excluding the imports
        input_data = {}
        imports = set(["division", "tables"])
        for attribute in dir(input_module):
            if attribute.startswith("_") or attribute in imports:
                continue
            else:
                input_data[attribute] = getattr(input_module, attribute)
        logger.info("Succesfully loaded data.")
        return cls(input_data)

    def calc_Qr(self):
        # local names
        d = self.data
        v1, v2, v3, v4 = d["v1"], d["v2"], d["v3"], d["v4"]

        # Υπολογισμός των κατακόρυφων φορτίων για κάθε συνδυασμό.
        QR1 = self._calc_Qr(v1, v2)
        QR2 = self._calc_Qr(v1, v3)
        QR3 = self._calc_Qr(1, 0)
        QR4 = self._calc_Qr(v4, v4)
        QR5 = QR4

        self.data.update({
            "QR1": QR1,
            "QR2": QR2,
            "QR3": QR3,
            "QR4": QR4,
            "QR5": QR5,
        })

    def _calc_Qr(self, v_sw, v_hl):
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
        """

        # local names
        d = self.data
        Gcr, Gtr, Qnom, L, e_min  = d["Gcr"], d["Gtr"], d["Qr_nom"], d["L"], d["e_min"]

        # calculations
        Gcr_v = Gcr * v_sw
        Gtr_v = Gtr * v_sw
        # Unloaded crane
        SQr_max = 0.5 * Gcr_v + Gtr_v * (L - e_min) / L # Unfavorable axis
        Qr_max = SQr_max / 2                            # Unfavorable axis
        SQr_min = 0.5 * Gcr_v + Gtr_v * e_min / L       # Favorable axis
        Qr_min = SQr_min / 2                            # Favorable axis
        # Loaded crane
        Qh = v_hl * Qnom
        SQr_MAX = 0.5 * Gcr_v + (Gtr_v + Qh) * (L - e_min) / L  # Unfavorable axis
        Qr_MAX = SQr_MAX / 2                                    # Unfavorable axis
        SQr_MIN = 0.5 * Gcr_v + (Gtr_v + Qh) * e_min / L        # Favorable axis
        Qr_MIN = SQr_MIN / 2                                    # Favorable axis

        return QR(Gcr_v, Gtr_v, Qh, SQr_MIN, Qr_MIN, SQr_min, Qr_min, SQr_MAX, Qr_MAX, SQr_max, Qr_max)

    def calc_Ht(self):
        QR1, QR4 = self.data["QR1"], self.data["QR4"]
        HT1 = self._calc_Ht(QR1.SQr_MAX, QR1.SQr_MIN, QR1.Qr_min)
        HT4 = self._calc_Ht(QR4.SQr_MAX, QR4.SQr_MIN, QR4.Qr_min)
        self.data.update({
            "HT1": HT1,
            "HT4": HT4,
        })

    def _calc_Ht(self, SQr_MAX, SQr_MIN, Qr_min):
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
        # local names
        data = self.data
        L, a, mf, mw, v5, nr = data["L"], data["a"], data["mf"], data["mw"], data["v5"], data["nr"],

        # calculations
        K = mf * mw * Qr_min
        HL = HL_1 = HL_2 = v5 * K / (nr)
        ksi1 = SQr_MAX / (SQr_MAX + SQr_MIN)
        ksi2 = 1 - ksi1
        Ls = (ksi1 - 0.5) * L
        M = K * Ls
        HT_1 = v5 * ksi2 * M / a
        HT_2 = v5 * ksi1 * M / a

        return HT(K, HL, ksi1, ksi2, Ls, M, HT_1, HT_2)

    def calc_Hs(self):
        """
        Αυτή η μέθοδος κάνει τον υπολογισμό των οριζόντιων φορτίων λόγω της
        παράγωγης κίνησης της γερανογέφυρας.
        """

        # local namespace
        d = self.data
        RT, L, nr, e1, e2, m, a_rad, QR5 = \
            d["RT"], d["L"], d["nr"], d["e1"], d["e2"], d["m"], d["a_rad"], d["QR5"]

        SQr = QR5.SQr_MAX + QR5.SQr_MIN

        ksi1 = QR5.SQr_MAX / SQr
        ksi2 = 1 - ksi1
        f = 0.3 * (1 - exp(-250 * a_rad))

        self.logger.info(f)

        if RT.endswith('FF'):
            h = (m * ksi1 * ksi2 * L**2 + e1**2 + e2**2)/(e1 + e2)
        elif RT.endswith('FM'):
            h = (m * ksi1 * L**2 + e1**2 + e2**2)/(e1 + e2)

        if RT == ("IFF"):
            l_s = 1 - (e1 + e2) / (nr * h)
            l_s11L = 0
            l_s12L = 0
            l_s21L = 0
            l_s22L = 0
            l_s11T = (ksi2 / nr) * (1 - e1 / h)
            l_s12T = (ksi2 / nr) * (1 - e2 / h)
            l_s21T = (ksi1 / nr) * (1 - e1 / h)
            l_s22T = (ksi1 / nr) * (1 - e2 / h)
        elif RT == ("CFF"):
            l_s = 1 - (e1 + e2) / (nr * h)
            l_s11L = (ksi1 * ksi2 * L) / (nr * h)
            l_s12L = (ksi1 * ksi2 * L) / (nr * h)
            l_s21L = (ksi1 * ksi2 * L) / (nr * h)
            l_s22L = (ksi1 * ksi2 * L) / (nr * h)
            l_s11T = (ksi2 / nr) * (1 - e1 / h)
            l_s12T = (ksi2 / nr) * (1 - e2 / h)
            l_s21T = (ksi1 / nr) * (1 - e1 / h)
            l_s22T = (ksi1 / nr) * (1 - e2 / h)
        elif RT == ("IFM"):
            l_s = ksi2 * (1 - (e1 + e2) / (nr * h))
            l_s11L = 0
            l_s12L = 0
            l_s21L = 0
            l_s22L = 0
            l_s11T = (ksi2 / nr) * (1 - e1 / h)
            l_s12T = (ksi2 / nr) * (1 - e2 / h)
            l_s21T = 0
            l_s22T = 0
        elif RT == ("CFM"):
            l_s = ksi2 * (1 - (e1 + e2) / (nr * h))
            l_s11L = (ksi1 * ksi2 * L) / (nr * h)
            l_s12L = (ksi1 * ksi2 * L) / (nr * h)
            l_s21L = (ksi1 * ksi2 * L) / (nr * h)
            l_s22L = (ksi1 * ksi2 * L) / (nr * h)
            l_s11T = (ksi2 / nr) * (1 - e1 / h)
            l_s12T = (ksi2 / nr) * (1 - e2 / h)
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

        H_s1T = H_s11T - S
        H_s2T = H_s21T

        # update self.data
        local_vars = locals()
        useful_vars = ("SQr", "ksi1", "ksi2", "f", "h", "l_s", "l_s11L", "l_s12L", "l_s21L", "S",
                       "l_s22L", "l_s11T", "l_s12T", "l_s21T", "l_s22T", "H_s11L", "H_s12L",
                       "H_s21L", "H_s22L", "H_s11T", "H_s12T", "H_s21T", "H_s22T", "H_s1T", "H_s2T")
        self.data.update({name: local_vars[name] for name in useful_vars})

    def calc_fatigue(self):

        """
        Η συνάρτηση αυτή υπολογίζει τα φορτία κόπωσης της γερανογέφυρας για
        ορθές και διατμητικές τάσεις.
        """
        d = self.data
        SQmax_i = 0.5 * d["Gcr"] + (d["Gtr"] + d["Qr_nom"]) * (d["L"] - d["e_min"]) / d["L"]  # Δυσμενής άξονας
        Qmax_i  = SQmax_i / 2
        Qes = d["vfat"] * d["lfat_s"] * Qmax_i
        Qet = d["vfat"] * d["lfat_t"] * Qmax_i

        self.data.update({
            "SQmax_i": SQmax_i,
            "Qmax_i": Qmax_i,
            "Qes": Qes,
            "Qet": Qet,
        })
