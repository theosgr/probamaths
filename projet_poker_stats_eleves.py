from scipy.stats import *
import numpy as np
import csv
import statistics

""" On reprÃƒÆ’Ã‚Â©sente les classes de valeurs en utilisant la borne sup de chaque intervalle :
    les classes [0,0.3], ]0.3,0.6], ]0.6,0.8], ]0.8,1] sont reprÃƒÆ’Ã‚Â©sentÃƒÆ’Ã‚Â©es par [0.3,0.6,0.8,1]
"""
categories = [0.3,0.6,0.8,1]

class Profile :
    """ Classe reprÃƒÆ’Ã‚Â©sentant le profil d'un joueur
    """
    def __init__(self,actions_stats_csv,name) :
        self.name = name
        self.actions_stats = {}
        for c in categories :
            self.actions_stats[str(c)] = {}
        with open(actions_stats_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader :
                r = dict(row)
                self.actions_stats[r['hand_value']][r['action']]=float(r['value'])
        csvfile.close()
    def get_frequencies_from_category(self,cat) :
        """ Fonction retournant les frÃƒÆ’Ã‚Â©quences de coups du profil pour la classe de valeurs cat
        """
        return np.array([self.actions_stats[str(cat)]['Fold'],self.actions_stats[str(cat)]['Check'],self.actions_stats[str(cat)]['Call'],self.actions_stats[str(cat)]['Raise']])

class Actions :
    """ Classe pour le traitement des actions d'un joueur :
        recorded_actions : dictionnaire contenant les diffÃƒÆ’Ã‚Â©rents coups jouÃƒÆ’Ã‚Â© par le joueur
    """
    def __init__(self,actions_csv) :
        self.recorded_actions = {}
        for x in categories :
            self.recorded_actions[str(x)]={'Fold':0,'Check':0,'Call':0,'Raise':0}
        with open(actions_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader :
                r = dict(row)
                self.recorded_actions[self.get_category(r['hand_value'])][r['action']]+=1
        csvfile.close()

    def get_category(self,x) :
        """ fonction interne
        """
        for y in categories :
            if float(x) < y :
                return str(y)
        return "No catetory"

    def get_numbers_from_category(self,cat) :
        """ fonction retournant le tableau des effectifs pour la classe de valeur cat
        """
        return np.array([self.recorded_actions[str(cat)]['Fold'],self.recorded_actions[str(cat)]['Check'],self.recorded_actions[str(cat)]['Call'],self.recorded_actions[str(cat)]['Raise']])

    def get_best_profile(self,profiles) :
        res = "No profile"
        eff_obs03 = self.get_numbers_from_category(0.3)
        eff_obs06 = self.get_numbers_from_category(0.6)
        eff_obs08 = self.get_numbers_from_category(0.8)
        eff_obs1 = self.get_numbers_from_category(1)
        agg_serr_03 = agg_serr.get_frequencies_from_category(0.3)
        agg_serr_06 = agg_serr.get_frequencies_from_category(0.6)
        agg_serr_08 = agg_serr.get_frequencies_from_category(0.8)
        agg_serr_1 = agg_serr.get_frequencies_from_category(1)
        agg_larg_03 = agg_larg.get_frequencies_from_category(0.3)
        agg_larg_06 = agg_larg.get_frequencies_from_category(0.6)
        agg_larg_08 = agg_larg.get_frequencies_from_category(0.8)
        agg_larg_1 = agg_larg.get_frequencies_from_category(1)
        pass_serr_03 = pass_serr.get_frequencies_from_category(0.3)
        pass_serr_06 = pass_serr.get_frequencies_from_category(0.6)
        pass_serr_08 = pass_serr.get_frequencies_from_category(0.8)
        pass_serr_1 = pass_serr.get_frequencies_from_category(1)
        pass_larg_03 = pass_larg.get_frequencies_from_category(0.3)
        pass_larg_06 = pass_larg.get_frequencies_from_category(0.6)
        pass_larg_08 = pass_larg.get_frequencies_from_category(0.8)
        pass_larg_1 = pass_larg.get_frequencies_from_category(1)
        eff_att=agg_serr_03*np.sum(eff_obs03)
        (Y,p_agg_serr03) = chisquare(eff_obs03,f_exp=eff_att)
        eff_att=agg_larg_03*np.sum(eff_obs03)
        (Y,p_agg_larg03) = chisquare(eff_obs03,f_exp=eff_att)
        eff_att=pass_serr_03*np.sum(eff_obs03)
        (Y,p_pass_serr03) = chisquare(eff_obs03,f_exp=eff_att)
        eff_att=pass_larg_03*np.sum(eff_obs03)
        (Y,p_pass_larg03) = chisquare(eff_obs03,f_exp=eff_att)
        eff_att=agg_serr_06*np.sum(eff_obs06)
        (Y,p_agg_serr06) = chisquare(eff_obs06,f_exp=eff_att)
        eff_att=agg_larg_06*np.sum(eff_obs06)
        (Y,p_agg_larg06) = chisquare(eff_obs06,f_exp=eff_att)
        eff_att=pass_serr_06*np.sum(eff_obs06)
        (Y,p_pass_serr06) = chisquare(eff_obs06,f_exp=eff_att)
        eff_att=pass_larg_06*np.sum(eff_obs06)
        (Y,p_pass_larg06) = chisquare(eff_obs06,f_exp=eff_att)
        eff_att=agg_serr_08*np.sum(eff_obs08)
        (Y,p_agg_serr08) = chisquare(eff_obs08,f_exp=eff_att)
        eff_att=agg_larg_08*np.sum(eff_obs08)
        (Y,p_agg_larg08) = chisquare(eff_obs08,f_exp=eff_att)
        eff_att=pass_serr_08*np.sum(eff_obs08)
        (Y,p_pass_serr08) = chisquare(eff_obs08,f_exp=eff_att)
        eff_att=pass_larg_08*np.sum(eff_obs08)
        (Y,p_pass_larg08) = chisquare(eff_obs08,f_exp=eff_att)
        eff_att=agg_serr_1*np.sum(eff_obs1)
        (Y,p_agg_serr1) = chisquare(eff_obs1,f_exp=eff_att)
        eff_att=agg_larg_1*np.sum(eff_obs1)
        (Y,p_agg_larg1) = chisquare(eff_obs1,f_exp=eff_att)
        eff_att=pass_serr_1*np.sum(eff_obs1)
        (Y,p_pass_serr1) = chisquare(eff_obs1,f_exp=eff_att)
        eff_att=pass_larg_1*np.sum(eff_obs1)
        (Y,p_pass_larg1) = chisquare(eff_obs1,f_exp=eff_att)
        j_pass_larg=[p_pass_larg03,p_pass_larg06,p_pass_larg08,p_pass_larg1]
        j_pass_serr=[p_pass_serr03,p_pass_serr06,p_pass_serr08,p_pass_serr1]
        j_agg_serr=[p_agg_serr03,p_agg_serr06,p_agg_serr08,p_agg_serr1]
        j_agg_larg=[p_agg_larg03,p_agg_larg06,p_agg_larg08,p_agg_larg1]
        p_agg_serr=statistics.mean(j_agg_serr)
        p_agg_larg=statistics.mean(j_agg_larg)
        p_pass_larg=statistics.mean(j_pass_larg)
        p_pass_serr=statistics.mean(j_pass_serr)
        a = [p_agg_serr,p_agg_larg,p_pass_serr,p_pass_larg]
        b = a.index(max(a))
        if b == 0 :
            res="Agressif/serré"
        if b == 1 :
            res = "Agressif/large"
        if b == 2 :
            res = "Passif/serré"
        if b == 3 :
            res = "Passif/large"
        return res

agg_serr = Profile("actions_agressif_serre.csv","Agressif/serrÃ©")
agg_larg = Profile("actions_agressif_large.csv","Agressif/large")
pass_serr = Profile("actions_passif_serre.csv","Passif/serrÃ©")
pass_larg = Profile("actions_passif_large.csv","Passif/large")

profiles = [agg_larg,agg_serr,pass_larg,pass_serr]

actions_joueurA = Actions("joueurA.csv")
actions_joueurB = Actions("joueurB.csv")
actions_joueurC = Actions("joueurC.csv")
actions_joueurD = Actions("joueurD.csv")
actions_joueurE = Actions("joueurE.csv")
actions_joueurF = Actions("joueurF.csv")

print("Joueur A : "+actions_joueurA.get_best_profile(profiles))
print("Joueur B : "+actions_joueurB.get_best_profile(profiles))
print("Joueur C : "+actions_joueurC.get_best_profile(profiles))
print("Joueur D : "+actions_joueurD.get_best_profile(profiles))
print("Joueur E : "+actions_joueurE.get_best_profile(profiles))
print("Joueur F : "+actions_joueurF.get_best_profile(profiles))
