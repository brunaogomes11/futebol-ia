from app.iaModel import redeNeural
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


# Dados - Campeonato
campeonatosPorPais = [
    {"pais": "Inglaterra", "value": "england", "campeonatos": [
        {"nome": "Premier League", "value": "premierLeague", "nome_dataset": "E0"},
        {"nome": "EFL Championship", "value": "eflChm", "nome_dataset": "E1"}
    ]}, 
    {"pais": "Alemanha", "value": "germany", "campeonatos": [
        {"nome": "Premier League", "value": "premierLeague", "nome_dataset": "E0"},
        {"nome": "EFL Championship", "value": "eflChm", "nome_dataset": "E1"}
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
        descModeloIA = request.form['descModelo']
        lrModelo = request.form['lrModelo']
        momentumModelo = request.form['momentumModelo']
        hiddenSize = request.form['hsModelo']
        epocas = request.form['epochsModelo']
        entradas = request.form['entradasSelecionadas']
        tempo, erros= redeNeural(momentumModelo, lrModelo, epocas, hiddenSize, datasetEscolhido, entradas)
        return render_template("modeloCriado.html", pais=paisEscolhido, campEscolhido=campeonatoEscolhido, nome=nomeModeloIA, descricao=descModeloIA, learningRate=lrModelo, momentum=momentumModelo, hiddenSize=hiddenSize, entradas=entradas, tempo=tempo, erros=erros, filename='graficoTrain.png')
    return render_template('criarModelos.html')

@app.route('/modelos')
def mostrarModelos():
    return render_template('modelosCriados.html')

def descartarIA():
    return redirect('/')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='temp/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))