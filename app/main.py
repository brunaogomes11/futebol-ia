import pandas as pd
from app.iaModel import redeNeural
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)


# Dados - Campeonato
campeonatosPorPais = [
    {"pais": "Inglaterra", "value": "england", "campeonatos": [
        {"nome": "Premier League", "value": "premierLeague", "nome_dataset": "E0"},
        {"nome": "EFL Championship", "value": "eflChm", "nome_dataset": "E1"}
    ]}, 
    {"pais": "Alemanha", "value": "germany", "campeonatos": [
        {"nome": "Bundesliga 1", "value": "bdl1", "nome_dataset": "D1"},
        {"nome": "Bundesliga 2", "value": "bdl2", "nome_dataset": "D2"}
    ]}
]

@app.route("/", methods=["GET", "POST"])
def criarModelos():
    if request.method == 'POST':
        paisEscolhido = request.form['paises']
        campeonatoEscolhido = request.form['campeonato']
        for i in range(0, len(campeonatosPorPais)):
            if (campeonatosPorPais[i]["value"] == paisEscolhido):
                paisEscolhido = campeonatosPorPais[i]["pais"]
                for j in range (0, len(campeonatosPorPais[i]["campeonatos"])):
                    if (campeonatosPorPais[i]["campeonatos"][j]["value"] == campeonatoEscolhido):
                        campeonatoEscolhido = campeonatosPorPais[i]["campeonatos"][j]["nome"]
                        datasetEscolhido = campeonatosPorPais[i]["campeonatos"][j]["nome_dataset"]
        nomeModeloIA = request.form['nomeModelo']
        lrModelo = request.form['lrModelo']
        momentumModelo = request.form['momentumModelo']
        hiddenSize = request.form['hsModelo']
        epocas = request.form['epochsModelo']
        entradas = request.form['entradasSelecionadas']
        tempo, erros, previsoes, reais = redeNeural(nomeModeloIA, momentumModelo, lrModelo, epocas, hiddenSize, datasetEscolhido, entradas)
        salvarEstatisticas(nomeModeloIA, datasetEscolhido, lrModelo, momentumModelo, hiddenSize, epocas, reais, previsoes, entradas)
        # return jsonify(nomeModeloIA, datasetEscolhido, lrModelo, momentumModelo, hiddenSize, epocas, entradas)
        return render_template('modeloCriado.html',pais=paisEscolhido, campEscolhido=campeonatoEscolhido, nome=nomeModeloIA, dataset=datasetEscolhido, learningRate=lrModelo, momentum=momentumModelo, hiddenSize=hiddenSize, erros=erros, tempo=tempo, filename='graficoTrain.png')
    return render_template('criarModelos.html')

@app.route('/modelos')
def mostrarModelos():
    return render_template('modelosCriados.html')

def descartarIA():
    return redirect('/')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='temp/' + filename), code=301)

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