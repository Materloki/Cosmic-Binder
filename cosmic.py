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
    df["hora"] = df.Timestamp.dt.hour
    df["dia"] = df.Timestamp.dt.day
    events = data_frame[data_frame["dia"]==dia]["hora"].value_counts(sort=False).to_frame()
    fig= plt.figure(figsize=(10,6))
    plt.bar(x=events.index, height=events.hora, label="Dia "+str(dia))
    plt.title("DIA "+str(dia))
    plt.xlabel("Horas")
    plt.ylabel("Quantidade de Eventos")
    plt.show()

def HistogramaPorMinuto(df,dia=29, hora=18):
    data_frame = df.copy()
    df["hora"] = df.Timestamp.dt.hour
    df["dia"] = df.Timestamp.dt.day
    df["minuto"] = df.Timestamp.dt.minute
    df["bin"] =df.minuto.map(lambda minuto: int(minuto/5))
    events = data_frame[(data_frame["dia"]==dia) & (data_frame["hora"] == hora)]["bin"].value_counts(sort=False).to_frame()
    fig= plt.figure(figsize=(10,6))
    plt.bar(x=events.index, height=events.bin, label="Hora "+str(hora))
    plt.title("DIA "+str(dia))
    plt.xlabel("Horas")
    plt.ylabel("Quantidade de Eventos")
    plt.show()

def MediaPorHora(df,dia=29):
    data_frame = df.copy()
    df["hora"] = df.Timestamp.dt.hour
    df["dia"] = df.Timestamp.dt.day
    events = data_frame[data_frame["dia"]==dia]["hora"].value_counts(sort=False).to_frame()
    print("Média diária:" +str(events.hora.mean()))
    print(events)
   