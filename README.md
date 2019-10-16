# SpotClassification
Image processing algorithm for spot detection and labeling

[Este projeto foi desenvolvido em outra plataforma de controle de versionamento e exportada para o GitHub após o término da disciplina Introdução ao processamento de imagens - UnB]

Uma aplicação em biotecnologia resulta imagens binárias de manchas. O objetivo desse projeto é desenvolver um método para determinar se uma imagem contém alguma mancha e, se a resposta for positiva, classificar cada mancha como tipo A se ela não tem buracos ou como tipo B, caso contrário.

O algoritmo desenvolvido foi proposto pelo professor Alexandre Zagehetto - Departamento de Ciência da Computação, UnB - e está descrito no documento "labeling.pdf"

## Saída

Contagem do número de manchas de cada tipo e imagem com as manchas categorizadas por cor.

```
Numero de bacterias do tipo 1:  10
Numero de bacterias do tipo 2:  7
```

![result](data/result.png?raw=true)

## Instalação e uso

Install python
```
sudo apt-get update
sudo apt-get install python3.6
```

Create a virtual environment called "venv" and activate it
```
python3 -m venv venv
source venv/bin/activate
```

Install the required packages
```
python3 -m pip install -r requirements.txt
```

Run 
```
python3 classifier.py
```

