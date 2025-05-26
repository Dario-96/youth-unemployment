import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

pil = pd.read_csv("C:/Users/....../Pil.csv")
disoccupati = pd.read_csv("C:/Users/....../Disoccupati.csv")
occupati = pd.read_csv("C:/Users/....../Occupati.csv")
inattivi = pd.read_csv("C:/Users/....../Inattivi.csv")
popolazione = pd.read_csv("C:/Users/....../Popolazione.csv")

#inserire al posto di "/....../" l'indirizzo dove vengono salvati i file
#Insert in place of "/....../" the address where the files are saved.

anni = ["2018", "2019", "2020", "2021", "2022"]
years = ["2019", "2020", "2021", "2022", "2023"]
regioni = ["Piemonte", "Valle d'Aosta / Vallée d'Aoste", "Liguria", "Lombardia", "Trentino Alto Adige / Südtirol", "Veneto", "Friuli-Venezia Giulia",
           "Emilia-Romagna", "Toscana", "Umbria", "Marche", "Lazio", "Abruzzo", "Molise", "Campania", "Puglia", "Basilicata", "Calabria", "Sicilia", "Sardegna"]
regioni.sort()

df_pop_2019 = pd.DataFrame(columns=['Regione', '15-34 anni'])
df_pop_2020 = pd.DataFrame(columns=['Regione', '15-34 anni'])
df_pop_2021 = pd.DataFrame(columns=['Regione', '15-34 anni'])
df_pop_2022 = pd.DataFrame(columns=['Regione', '15-34 anni'])
df_pop_2023 = pd.DataFrame(columns=['Regione', '15-34 anni'])

df_pil_anni = []
df_dis_anni = []
df_occ_anni = []
df_inn_anni = []
df_pop_anni = []

#FILTRAGGIO DATI

for anno in anni:
    pil_anno = pil.copy()
    pil_anno = pil_anno[(pil_anno['Tipo aggregato'] == "prodotto interno lordo ai prezzi di mercato") &
                        (pil_anno['Valutazione'] == "prezzi correnti") &
                        (pil['Edizione'].str.contains("Dic-2023")) &
                        (pil_anno['TIME'] == int(anno)) & 
                        (pil_anno['Correzione'] == "dati grezzi")]
    valori = pil_anno['Value']
    territorio = pil_anno['Territorio']
    df_pil = pd.DataFrame(zip(territorio, valori))
    df_pil = df_pil.drop([2, 4, 5, 9, 10, 11, 14, 16, 22, 27, 28, 29], axis=0) #Italia indice 14
    df_pil = df_pil.reset_index(drop=False)
    df_pil = df_pil.drop('index', axis=1)
    df_pil = df_pil.sort_values(by=df_pil.columns[0]).reset_index(drop=True)
    if anno == "2018":
        df_pil_2018 = df_pil
    elif anno == "2019":
        df_pil_2019 = df_pil
    elif anno == "2020":
        df_pil_2020 = df_pil
    elif anno == "2021":
        df_pil_2021 = df_pil
    elif anno == "2022":
        df_pil_2022 = df_pil
    
#print(f"data frame territorio-valori Pil 2018: \n {df_pil_2018}\n")
#print(f"data frame territorio-valori Pil 2019: \n {df_pil_2019}\n")
#print(f"data frame territorio-valori Pil 2020: \n {df_pil_2020}\n")
#print(f"data frame territorio-valori Pil 2021: \n {df_pil_2021}\n")
#print(f"data frame territorio-valori Pil 2022: \n {df_pil_2022}\n")
    
for anno in anni:
    dis_temp = disoccupati.copy()
    dis_temp = dis_temp[(dis_temp['ETA1'] == "Y15-34") &
                        (dis_temp['TIME'] == anno) &
                        (dis_temp['Sesso'] == "totale")]
    osservazioni = dis_temp['Value']
    territorio = dis_temp['Territorio']
    df_tax_disocc = pd.DataFrame(zip(territorio, osservazioni))
    df_tax_disocc = df_tax_disocc.drop([5, 7, 10, 13, 15, 17, 18, 24, 27], axis=0) #Italia indice 13
    df_tax_disocc = df_tax_disocc.reset_index(drop=False)
    df_tax_disocc = df_tax_disocc.drop('index', axis=1)
    df_tax_disocc = df_tax_disocc.sort_values(by=df_tax_disocc.columns[0]).reset_index(drop=True)
    df_tax_disocc[1] = df_tax_disocc[1].map(lambda x: x / 100)
    if anno == "2018":
        df_tax_disocc_2018 = df_tax_disocc
    elif anno == "2019":
        df_tax_disocc_2019 = df_tax_disocc
    elif anno == "2020":
        df_tax_disocc_2020 = df_tax_disocc
    elif anno == "2021":
        df_tax_disocc_2021 = df_tax_disocc
    elif anno == "2022":
        df_tax_disocc_2022 = df_tax_disocc

#print(f"data frame TASSO DISOCCUPAZION 2018: \n {df_tax_disocc_2018}\n")
#print(f"data frame TASSO DISOCCUPAZION 2019: \n {df_tax_disocc_2019}\n")
#print(f"data frame TASSO DISOCCUPAZION 2020: \n {df_tax_disocc_2020}\n")
#print(f"data frame TASSO DISOCCUPAZION 2021: \n {df_tax_disocc_2021}\n")
#print(f"data frame TASSO DISOCCUPAZION 2022: \n {df_tax_disocc_2022}\n")
    

for anno in anni:
    occ_temp = occupati.copy()
    occ_temp = occ_temp[(occ_temp['ETA1'] == "Y15-34") & 
                        (occ_temp['TIME'] == anno) &
                        (occ_temp['Sesso'] == "totale")]
    osservazioni = occ_temp['Value']
    territorio = occ_temp['Territorio']
    df_occupati = pd.DataFrame(zip(territorio, osservazioni))
    df_occupati = df_occupati.drop([0, 1, 2, 3, 4, 5, 12, 22], axis=0) #Italia indice 0
    df_occupati = df_occupati.reset_index(drop=False)
    df_occupati = df_occupati.drop('index', axis=1)
    df_occupati = df_occupati.sort_values(by=df_occupati.columns[0]).reset_index(drop=True)
    df_occupati[1] = df_occupati[1].map(lambda x: x * 1000)
    df_occupati[1] = df_occupati[1].apply(lambda x: int(x))
    if anno == "2018":
        df_occupati_2018 = df_occupati
    elif anno == "2019":
        df_occupati_2019 = df_occupati
    elif anno == "2020":
        df_occupati_2020 = df_occupati
    elif anno == "2021":
        df_occupati_2021 = df_occupati
    elif anno == "2022":
        df_occupati_2022 = df_occupati

#print(f"data frame OCCUPATI 2018: \n {df_occupati_2018}\n")
#print(f"data frame OCCUPATI 2019: \n {df_occupati_2019}\n")
#print(f"data frame OCCUPATI 2020: \n {df_occupati_2020}\n")
#print(f"data frame OCCUPATI 2021: \n {df_occupati_2021}\n")
#print(f"data frame OCCUPATI 2022: \n {df_occupati_2022}\n")

    
for anno in anni:
    inn_temp = inattivi.copy()
    inn_temp = inn_temp[(inn_temp['ETA1'] == "Y15-34") & 
                        (inn_temp['TIME'] == anno) &
                        (inn_temp['Sesso'] == "totale")]
    osservazioni = inn_temp['Value']
    territorio = inn_temp['Territorio']
    df_inattivi = pd.DataFrame(zip(territorio, osservazioni))
    df_inattivi = df_inattivi.drop([0, 1, 4, 14, 16, 18, 24, 25], axis=0) #Italia indice 14
    df_inattivi = df_inattivi.reset_index(drop=False)
    df_inattivi = df_inattivi.drop('index', axis=1)
    df_inattivi = df_inattivi.sort_values(by=df_inattivi.columns[0]).reset_index(drop=True)
    df_inattivi[1] = df_inattivi[1].map(lambda x: x * 1000)
    df_inattivi[1] = df_inattivi[1].apply(lambda x: int(x))
    if anno == "2018":
        df_inattivi_2018 = df_inattivi
    elif anno == "2019":
        df_inattivi_2019 = df_inattivi
    elif anno == "2020":
        df_inattivi_2020 = df_inattivi
    elif anno == "2021":
        df_inattivi_2021 = df_inattivi
    elif anno == "2022":
        df_inattivi_2022 = df_inattivi

#print(f"data frame INATTIVI 2018: \n {df_inattivi_2018}\n")
#print(f"data frame INATTIVI 2019: \n {df_inattivi_2019}\n")
#print(f"data frame INATTIVI 2020: \n {df_inattivi_2020}\n")
#print(f"data frame INATTIVI 2021: \n {df_inattivi_2021}\n")
#print(f"data frame INATTIVI 2022: \n {df_inattivi_2022}\n")

    
for anno in years:
    df_pop_anni = []
    for regione in regioni:
        df_regione = popolazione[(popolazione['TIME'] == int(anno)) &
                                 (popolazione['Territorio'] == regione) &
                                 (popolazione['Stato civile'] == "totale") &
                                 (popolazione['Sesso'] == "totale")]
        osservazioni = df_regione['Value']
        age = df_regione['ETA1']
        df_pop = pd.DataFrame(zip(age, osservazioni))
        df_pop[0] = df_pop[0].str.replace("Y", "")
        df_pop[0] = df_pop[0].str.replace("_GE", "")
        df_pop[0] = df_pop[0].str.replace("TOTAL", "000")
        df_pop[0] = df_pop[0].apply(lambda x: int(x))
        tot_regione = df_pop[(df_pop[0] >= 15) & (df_pop[0] <= 34)][1].sum()
        df_pop_anni.append(tot_regione)      
    if anno == "2019":
        df_pop_2019 = pd.DataFrame({'Regione': regioni, '15-34 anni': df_pop_anni})    
    elif anno == "2020":
        df_pop_2020 = pd.DataFrame({'Regione': regioni, '15-34 anni': df_pop_anni})    
    elif anno == "2021":
        df_pop_2021 = pd.DataFrame({'Regione': regioni, '15-34 anni': df_pop_anni})    
    elif anno == "2022":
        df_pop_2022 = pd.DataFrame({'Regione': regioni, '15-34 anni': df_pop_anni})    
    elif anno == "2023":
        df_pop_2023 = pd.DataFrame({'Regione': regioni, '15-34 anni': df_pop_anni})
    
#print(f"data frame POPOLAZIONE 2019: \n {df_pop_2019}\n")
#print(f"data frame POPOLAZIONE 2020: \n {df_pop_2020}\n")
#print(f"data frame POPOLAZIONE 2021: \n {df_pop_2021}\n")
#print(f"data frame POPOLAZIONE 2022: \n {df_pop_2022}\n")
#print(f"data frame POPOLAZIONE 2023: \n {df_pop_2023}\n")

df_forza_lav_2018 = df_pop_2019["15-34 anni"] - df_inattivi_2018[1]
df_forza_lav_2018 = pd.DataFrame(zip(regioni , df_forza_lav_2018))
#print(f"Questo è il data frame della FORZA LAVORO 2018 \n {df_forza_lav_2018}\n")

df_forza_lav_2019 = df_pop_2020["15-34 anni"] - df_inattivi_2019[1]
df_forza_lav_2019 = pd.DataFrame(zip(regioni , df_forza_lav_2019))
#print(f"Questo è il data frame della FORZA LAVORO 2019 \n {df_forza_lav_2019}\n")

df_forza_lav_2020 = df_pop_2021["15-34 anni"] - df_inattivi_2020[1]
df_forza_lav_2020 = pd.DataFrame(zip(regioni , df_forza_lav_2020))
#print(f"Questo è il data frame della FORZA LAVORO 2020 \n {df_forza_lav_2020}\n")

df_forza_lav_2021 = df_pop_2022["15-34 anni"] - df_inattivi_2021[1]
df_forza_lav_2021 = pd.DataFrame(zip(regioni , df_forza_lav_2021))
#print(f"Questo è il data frame della FORZA LAVORO 2021 \n {df_forza_lav_2021}\n")

df_forza_lav_2022 = df_pop_2023["15-34 anni"] - df_inattivi_2022[1]
df_forza_lav_2022 = pd.DataFrame(zip(regioni , df_forza_lav_2022))
#print(f"Questo è il data frame della FORZA LAVORO 2022 \n {df_forza_lav_2022}\n")

df_disoccupati_2018 = df_forza_lav_2018[1] - df_occupati_2018[1]
df_disoccupati_2018 = pd.DataFrame(zip(regioni, df_disoccupati_2018))
#print(f"Data frame DISOCCUPATI 2018 \n{df_disoccupati_2018}\n")

df_disoccupati_2019 = df_forza_lav_2019[1] - df_occupati_2019[1]
df_disoccupati_2019 = pd.DataFrame(zip(regioni, df_disoccupati_2019))
#print(f"Data frame DISOCCUPATI 2019 \n{df_disoccupati_2019}\n")

df_disoccupati_2020 = df_forza_lav_2020[1] - df_occupati_2020[1]
df_disoccupati_2020 = pd.DataFrame(zip(regioni, df_disoccupati_2020))
#print(f"Data frame DISOCCUPATI 2020 \n{df_disoccupati_2020}\n")

df_disoccupati_2021 = df_forza_lav_2021[1] - df_occupati_2021[1]
df_disoccupati_2021 = pd.DataFrame(zip(regioni, df_disoccupati_2021))
#print(f"Data frame DISOCCUPATI 2021 \n{df_disoccupati_2021}\n")

df_disoccupati_2022 = df_forza_lav_2022[1] - df_occupati_2022[1]
df_disoccupati_2022 = pd.DataFrame(zip(regioni, df_disoccupati_2022))
#print(f"Data frame DISOCCUPATI 2022 \n{df_disoccupati_2022}\n")

#CREAZIONE DATA FRAME PER OGNI ANNO

df_2018 = pd.concat([df_occupati_2018, df_disoccupati_2018[1], df_inattivi_2018[1], df_pil_2018[1]], axis=1)
df_2018.columns = ['REGIONI', 'OCCUPATI', 'DISOCCUPATI', 'INATTIVI', 'PIL']
#print(f"DATA FRAME RIFERENTE ALL'ANNO 2018\n {df_2018}\n\n")

df_2019 = pd.concat([df_occupati_2019, df_disoccupati_2019[1], df_inattivi_2019[1], df_pil_2019[1]], axis=1)
df_2019.columns = ['REGIONI', 'OCCUPATI', 'DISOCCUPATI', 'INATTIVI', 'PIL']
#print(f"DATA FRAME RIFERENTE ALL'ANNO 2019\n {df_2019}\n\n")

df_2020 = pd.concat([df_occupati_2020, df_disoccupati_2020[1], df_inattivi_2020[1], df_pil_2020[1]], axis=1)
df_2020.columns = ['REGIONI', 'OCCUPATI', 'DISOCCUPATI', 'INATTIVI', 'PIL']
#print(f"DATA FRAME RIFERENTE ALL'ANNO 2020\n {df_2020}\n\n")

df_2021 = pd.concat([df_occupati_2021, df_disoccupati_2021[1], df_inattivi_2021[1], df_pil_2021[1]], axis=1)
df_2021.columns = ['REGIONI', 'OCCUPATI', 'DISOCCUPATI', 'INATTIVI', 'PIL']
#print(f"DATA FRAME RIFERENTE ALL'ANNO 2021\n {df_2021}\n\n")

df_2022 = pd.concat([df_occupati_2022, df_disoccupati_2022[1], df_inattivi_2022[1], df_pil_2022[1]], axis=1)
df_2022.columns = ['REGIONI', 'OCCUPATI', 'DISOCCUPATI', 'INATTIVI', 'PIL']
#print(f"DATA FRAME RIFERENTE ALL'ANNO 2022\n {df_2022}\n\n")

dfs = [df_2018, df_2019, df_2020, df_2021, df_2022]
merged_df = pd.concat(dfs)
grouped_df = merged_df.groupby('REGIONI')
df_regioni = {}
for regione, anno in grouped_df:
    df_regioni[regione] = anno
for regione, df in df_regioni.items():
    print(f"DATA FRAME PER LA REGIONE {regione}:\n{df}\n\n")

#CALCOLO STATISTICO SUI DATA FRAME

# Calcolo e visualizzazione della regressione lineare per ogni regione
regions = list(df_regioni.keys())
group_size = 4
region_groups = [regions[i:i+group_size] for i in range(0, len(regions), group_size)]

for region_group in region_groups:
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    for i, regione in enumerate(region_group):
        row = i // 2
        col = i % 2
        df = df_regioni[regione]
        ax = axs[row, col]
        X = df['PIL'].values.reshape(-1, 1)  # Variabile indipendente (X)
        y = df['DISOCCUPATI'].values  # Variabile dipendente (y)
        # Inizializzazione del modello di regressione lineare
        model = LinearRegression()
        # Addestramento del modello sui dati
        model.fit(X, y)        
        # Calcolo del coefficiente di determinazione (R^2)
        r_squared = model.score(X, y)        
        # Calcolo dei coefficienti di regressione
        coefficients = model.coef_
        intercept = model.intercept_
        # Calcolo dei valori predetti
        predicted_y = model.predict(X)
        # Calcolo del coefficiente di Pearson e P-Value
        pearson_corr, p_value_pearson = pearsonr(X.flatten(), y)
        print(f"Coefficiente di Pearson per la regione {regione}: {pearson_corr:.4f}, P-Value: {p_value_pearson:.4f}")
        # Plot dei punti dati
        ax.scatter(X, y) #, label='Dati reali')        
        # Plot della retta di regressione
        ax.plot(X, predicted_y, color='red', label=f'Regressione lineare: y = {coefficients[0]:.2f}x + {intercept:.2f}, $R^2$ = {r_squared:.2f}')        
        # Etichette degli assi e legenda
        ax.set_xlabel('PIL')
        ax.set_ylabel('DISOCCUPATI')
        ax.set_title(f'Regressione lineare {regione}')
        ax.legend()

    plt.tight_layout()
    plt.show()