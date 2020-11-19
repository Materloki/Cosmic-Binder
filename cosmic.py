'''
Biblioteca para funções de manipulação e análise de dados do projeto de raios cósmicos
'''
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
import numpy as np

def Byte_Change_Endianess_16(x):
	return ((x & 0xFF) << 8) + ((x & 0xFF00) >> 8)

def Byte_Change_Endianess_24(x):
	return ((x & 0xFF) << 16) + ((x & 0xFF00)) + ((x & 0xFF0000) >> 16)

def Byte_Change_Endianess_32(x):
	return ((x & 0xFF) << 24) + ((x & 0xFF00) << 8) + ((x & 0xFF0000) >> 8) + ((x & 0xFF000000) >> 24)

def Remove_Parity_Bit(x):
	return x % 2**23

def Abrir(nome,linhas): #DONE
    
    # Função que abre o Dataset
    # Atributos: nome   - Arquivo a ser aberto, incluindo seu caminho
    #            linhas - Numero de linhas para abrir por vez
    #
    # Retornos:  iter   - Um iterador feito para abrir as próximas partes do dataset
    #            df     - O dataset que é manipulável
    
    iterador = pd.read_json(nome, orient='records', lines=True, chunksize=linhas)
    df = Proximo(iterador)
    return iterador, df

def Proximo(iterador): #DONE
    
    # Abre a próxima parte do Dataset
    # Atributos: iter - Iterador returnado pela função Abrir()
    #
    # Retornos:  df   - O dataset que é manipulável
    data = next(iterador)
    df = data.copy()
    df.pop("ClockCount")        #Coluna Vazia
    df.pop("TriggerCounter")    #Coluna Vazia
    df.pop("Epoch")             #N tem sentido analisa-la, ja que temos o TimeStamp (instante com precisão de segundos)
    return df

def HistogramaPorHora(df,dia=29):
    data_frame = df.copy()
    data_frame["hora"] = data_frame.Timestamp.dt.hour
    data_frame["dia"] = data_frame.Timestamp.dt.day
    events = data_frame[data_frame["dia"]==dia]["hora"].value_counts(sort=False).to_frame()
    fig= plt.figure(figsize=(10,6))
    plt.bar(x=events.index, height=events.hora, label="Dia "+str(dia))
    plt.title("DIA "+str(dia))
    plt.xlabel("Horas")
    plt.ylabel("Quantidade de Eventos")
    plt.show()

def HistogramaPorMinuto(df,dia=29, hora=18):
    data_frame = df.copy()
    data_frame["hora"] = data_frame.Timestamp.dt.hour
    data_frame["dia"] = data_frame.Timestamp.dt.day
    data_frame["minuto"] = data_frame.Timestamp.dt.minute
    data_frame["bin"] =data_frame.minuto.map(lambda minuto: int(minuto/5))
    events = data_frame[(data_frame["dia"]==dia) & (data_frame["hora"] == hora)]["bin"].value_counts(sort=False).to_frame()
    fig= plt.figure(figsize=(10,6))
    plt.bar(x=events.index, height=events.bin, label="Hora "+str(hora))
    plt.title("DIA "+str(dia))
    plt.xlabel("Horas")
    plt.ylabel("Quantidade de Eventos")
    plt.show()

def MediaPorHora(df,dia=29):
    data_frame = df.copy()
    data_frame["hora"] = data_frame.Timestamp.dt.hour
    data_frame["dia"] = data_frame.Timestamp.dt.day
    events = data_frame[data_frame["dia"]==dia]["hora"].value_counts(sort=False).to_frame()
    print("Média diária:" +str(events.hora.mean()))
    print(events)

def Histograma(df, dia=29, bin=10):
    data_frame = df.copy()
    data_frame["hora"] = data_frame.Timestamp.dt.hour.astype(str)
    data_frame["hora"] = data_frame["hora"].map(lambda h: h.zfill(2))
    data_frame["dia"] = data_frame.Timestamp.dt.day
    data_frame["minuto"] = data_frame.Timestamp.dt.minute
    data_frame["bin"] =data_frame.minuto.map(lambda minuto: int(minuto/bin))
    data_frame["bin"] = bin*data_frame["bin"]
    data_frame["bin"] = data_frame["bin"].astype(str)
    data_frame["bin"] = data_frame["bin"].map(lambda h: h.zfill(2))
    data_frame["bin"] =  data_frame['hora'] + ":" + data_frame['bin']
    dfn = data_frame[data_frame["dia"]==dia]
    events = dfn.bin.value_counts(sort=False).to_frame()
    events = events.sort_index()
    x = dfn["hora"].unique() + ":00"
    if events.index[0] != x[0]:
        x = np.delete(x, 0)
    fig= plt.figure(figsize=(20,6))
    plt.plot(events.index, events.bin)
    plt.xlim([events.index[0],events.index[-1]])
    plt.title("DIA "+str(dia))
    plt.xlabel("Horas")
    plt.ylabel("Quantidade de Eventos")
    plt.xticks(x)
    plt.show()
    

    