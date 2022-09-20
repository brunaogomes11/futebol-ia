import json
from app.iaModel import redeNeural
import os
from flask import Flask, jsonify, render_template, request
import pandas as pd

app = Flask(__name__)


# Dados - Campeonato
campeonatosPorPais = [
    {"pais": "Alemanha", "value": "germany", "campeonatos": [
        {"nome": "Bundesliga 1", "value": "bdl1", "nome_dataset": "D1"},
        {"nome": "Bundesliga 2", "value": "bdl2", "nome_dataset": "D2"}
    ]},
    {"pais": "Brasil", "value": "brazil", "campeonatos": [
        {"nome": "Brasileirão Série A", "value": "brasileiraoA", "nome_dataset": "BRA"}
    ]},
    {"pais": "Inglaterra", "value": "england", "campeonatos": [
        {"nome": "Premier League", "value": "premierLeague", "nome_dataset": "E0"},
        {"nome": "EFL Championship", "value": "eflChm", "nome_dataset": "E1"}
    ]}
]

@app.route("/treinar", methods=["POST"])
def criarModelos():
    form_requested = request.form
    for i in range(0, len(campeonatosPorPais)):
        if (campeonatosPorPais[i]["value"] == pais):
            for j in range (0, len(campeonatosPorPais[i]["campeonatos"])):
                if (campeonatosPorPais[i]["campeonatos"][j]["value"] == campeonatoEscolhido):
                    campeonatoEscolhido = campeonatosPorPais[i]["campeonatos"][j]["nome"]
                    datasetEscolhido = campeonatosPorPais[i]["campeonatos"][j]["nome_dataset"]
    pais, campeonato, nome, lr, momentum, hiddenSize, epocas, entradas = form_requested['pais'], form_requested['campeonato'], form_requested['nome'], form_requested['lr'], form_requested['momentum'], form_requested['hiddenSize'], form_requested['epocas'], form_requested['entradas'],
    tempo, erros, previsoes, reais = redeNeural(nome, momentum, lr, epocas, hiddenSize, datasetEscolhido, entradas)
    salvarEstatisticas(nome, datasetEscolhido, lr, momentum, hiddenSize, epocas, reais, previsoes, entradas)
    return jsonify(pais, campeonato, nome, lr, momentum, hiddenSize, entradas, tempo, erros)

@app.route('/modelos')
def mostrarModelos():
    return render_template('modelosCriados.html')

@app.route('/testar-modelo')
def testarModelos():
    return "Qual o modelo?"

def salvarEstatisticas(nome, dataset, lr, momentum, hiddenSize, epocas, real, previsao, entradas):
    for i in range(0, len(previsao)):
        if previsao[i] > 0.50:
            previsao[i] = 1
        elif previsao[i] <= 0.50 and previsao[i] >= -0.50:
            previsao[i] = 0
        elif previsao[i] < -0.50:
            previsao[i] = -1
    acertos = 0
    for i in range (0, len(real)):
        if real[i] == previsao[i]:
            acertos += 1
    tabela = pd.read_excel("app/data/Estatisticas.xlsx")
    tamanho_tabela = int(len(tabela))
    tabela.loc[tamanho_tabela, "Nome"] = nome
    tabela.loc[tamanho_tabela, "Dataset"] = dataset
    tabela.loc[tamanho_tabela, "Learning Rate"] = lr
    tabela.loc[tamanho_tabela, "Momentum"] = momentum
    tabela.loc[tamanho_tabela, "Tamanho Camada Oculta"] = hiddenSize
    tabela.loc[tamanho_tabela, "Epocas"] = epocas
    tabela.loc[tamanho_tabela, "Acertos/Total"] = f'{acertos} de {len(real)}'
    tabela.loc[tamanho_tabela, "Entradas"] = str(entradas)
    tabela.to_excel("app/data/Estatisticas.xlsx", index=False)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))