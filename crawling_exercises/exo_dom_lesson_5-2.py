# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 17:50:12 2018

@author: JN
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import statsmodels.api as sm


#%%

#importation des données, et création d'une colonne 'code_dpt' pour faire des recoupements par département

df_honos = pd.read_excel(
        "C:/Users/JN/Desktop/Telecom PT/Kit data science/git_exos/Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2016.xls",
        sheet_name = "Spécialistes",
        na_values = ["nc"],
        )

df_honos.rename(columns = {
        'Spécialistes':"Specialistes",
       'DEPARTEMENT':"Dpt", 
       'EFFECTIFS':"effectifs",
       'HONORAIRES SANS DEPASSEMENT (Euros)':"honos_base",
       'FRAIS DE DEPLACEMENT (Euros)':"frais_dep", 
       'TOTAL DES HONORAIRES (Euros)':"total honos"}, 
        inplace = True)

df_honos['code_dpt'] = df_honos['Dpt'].str[:2]

df_medecins = pd.read_excel(
        "C:/Users/JN/Desktop/Telecom PT/Kit data science/git_exos/rpps-medecins18-tab7v3_70423322755452.xls",
        skiprows = [0,1,2,3,4],
        header = 0
        )

df_medecins.rename(columns = {"SPECIALITE":"dpt"}, inplace = True)
df_medecins['code_dpt'] = df_medecins['dpt'].str[:2]

df_pop = pd.read_excel(
        "C:/Users/JN/Desktop/Telecom PT/Kit data science/git_exos/estim-pop-dep-sexe-gca-1975-2018.xls",
        sheet_name = "2018",
        skiprows = range(4),
        usecols = range(8),
        skipfooter = 2
        )

df_pop.rename(columns = {'Unnamed: 0':"code_dpt", 'Unnamed: 1':"dpt"}, inplace = True)

#%%
# on va renommer les colonnes de df_medecins de manière à ce que leurs intitulés correspondent aux intitulés de df_honos
dico_medecins = {
        'Anatomie et cytologie pathologiques':'Anatomo-cyto-pathologie',
        'Anesthésie-réanimation':'Anesthésie-réanimation chirurgicale',
        'Biologie médicale':'Médecins biologistes',
        'Cardiologie et maladies vasculaires':'Pathologie cardio-vasculaire',
        'Chirurgie générale':'Chirurgie générale',
        'Chirurgie maxillo-faciale et stomatologie':'Stomatologie',
        'Chirurgie orthopédique et traumatologie':'Chirurgie orthopédique et traumatologie',
        'Chirurgie infantile':'Chirurgie infantile',
        'Chirurgie plastique reconstructrice et esthétique':'Chirurgie plastique reconstructrice et esthétique',
        'Chirurgie thoracique et cardio-vasculaire':'Chirurgie thoracique et cardio-vasculaire',
        'Chirurgie urologique':'Chirurgie urologique',
        'Chirurgie vasculaire':'Chirurgie vasculaire',
        'Chirurgie viscérale et digestive':'Chirurgie viscérale et digestive',
        'Dermatologie et vénéréologie':'Dermato-vénéréologie',
        'Endocrinologie et métabolisme':'Endocrinologie et métabolisme',
        'Génétique médicale':'Médecine génétique',
        'Gériatrie':'Gériatrie',
        'Gynécologie médicale':'Gynécologie médicale',
        'Gynécologie-obstétrique':'Gynécologie obstétrique',
        'Hématologie':'Hématologie',
        'Gastro-entérologie et hépatologie':'Gastro-entérologie et hépatologie',
        'Médecine nucléaire':'Médecine nucléaire',
        'Médecine physique et réadaptation':'Médecine physique et de réadaptation',
        'Néphrologie':'Néphrologie',
        'Neurochirurgie':'Neurochirurgie',
        'Neurologie':'Neurologie',
        'ORL et chirurgie cervico-faciale':'Oto-rhino-laryngologie',
        'Oncologie option médicale':'Oncologie médicale',
        'Ophtalmologie':'Ophtalmologie',
        'Pédiatrie':'Pédiatrie',
        'Pneumologie':'Pneumologie',
        'Psychiatrie':'Psychiatrie',
        'Radiodiagnostic et imagerie médicale':'Radiodiagnostic et imagerie médicale',
        'Radiothérapie':'Radiothérapie',
        'Réanimation médicale':'Réanimation médicale',
        'Rhumatologie':'Rhumatologie'
        }

df_medecins.rename(columns = dico_medecins, inplace = True)
cols_to_drop = [
        "Ensemble des spécialités d'exercice",
        'Spécialistes',
        'Médecine du travail',
        'Recherche médicale',
        'Santé publique et médecine sociale',
        'Généralistes',
        'Médecine générale',
        'dpt'
        ]

df_medecins.drop(cols_to_drop, axis = 1, inplace = True)

#%%

#on "melte" df_medecins:
med_flat = pd.melt(df_medecins, id_vars = 'code_dpt', 
                   var_name = 'spe', value_name = 'nb_praticiens')

#on crée une colonne 'dpt_x_spe' dans med_flat et df_honos pour joindre les tables dans un dataframe nommé df
med_flat['dpt_x_spe'] = med_flat['code_dpt']+med_flat['spe']
df_honos['dpt_x_spe'] = df_honos['code_dpt']+df_honos['Specialistes'].str[4:]
depassements = pd.concat([df_honos['dpt_x_spe'],
                          df_honos['honos_base'],
                          df_honos['depassements']],axis = 1).dropna()

df = pd.merge(depassements, med_flat, how = "inner", on = 'dpt_x_spe')

# on ajoute la popultation par département à df
df_pop.set_index('code_dpt',inplace = True)

def get_pop(row):
    if str(row['code_dpt']) in df_pop.index.values:
        return df_pop.loc[str(row['code_dpt']),'Total']
    else:
        return np.nan
    
df['pop_dpt']=df.apply(get_pop, axis=1)

#%%

# on supprime les entrées vides de df, et on calcule des taux moyens de
#dépassement, ainsi que la densité de médecins par habitant pour chaque spécialité
df = df.dropna()
df['tx_depassement'] = df['depassements']/df['honos_base']
df['densite_doc'] = df['nb_praticiens']/df['pop_dpt']

#on représente les taux de dépassement en fonction des densités, et on fait une
#régression linéaire
X = sm.add_constant(df['densite_doc'])
Y = df['tx_depassement']

alpha = 0.05

plt.scatter(df['densite_doc']*1000,Y*100)
plt.xlabel = 'nb de praticiens pour 1000 habitants'
plt.ylabel = 'taux moyen de dépassements constaté (en %)'
plt.show()

model = sm.OLS(Y,X)
results = model.fit()

print()
print("les coefficients de la régression linéaire des dépassements sur les densités sont les suivants :")
print(results.params)
print()
print("les p-values de la régression sont les suivantes :")
print(results.pvalues)

#%%
#on reproduit la mêle démarche spécialité par spécialité, en écartant les spécialités pour lesquelles on dispose de trop peu de données
# on stocke les p-values par spécialité dans dictionnaire

dico = {}
for s in df['spe'].unique():
    specialite = df[df['spe']==s]
    if len(specialite.index.values) < 20:
        pass
    else:
        plt.scatter(specialite['densite_doc']*1000,specialite['tx_depassement']*100, label = s)
        plt.xlabel = 'nb de praticiens pour 1000 habitants'
        plt.ylabel = 'taux moyen de dépassements constaté (en %)'
        plt.legend()
        plt.show()
        
        X_spe = sm.add_constant(specialite['densite_doc'])
        Y_spe = specialite['tx_depassement']
        model_spe = sm.OLS(Y_spe,X_spe)
        results_spe = model_spe.fit()
        pval = results_spe.pvalues
        
        print()
        print("les coefficients de la régression linéaire des dépassements sur les densités sont les suivants :")
        print(results_spe.params)
        print()
        print("les p-values de la régression sont les suivantes :")
        print(pval)
        dico[s] = pval[1]
#%%

synthese = pd.DataFrame([dico])
synthese = synthese.T
synthese.rename(columns={0:'p-value'}, inplace=True)
synthese['regression significative?'] = (synthese['p-value'] < alpha)
synthese['regression significative?']
