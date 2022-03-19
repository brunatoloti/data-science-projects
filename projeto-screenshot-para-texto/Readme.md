# Projeto screenshot para texto

### Objetivo
Criar uma ferramenta com tkinter para converter texto de imagens em texto copiável.

### Ferramentas utilizadas
- para a interface gráfica:
    - tkinter
- para o screenshot da tela:
    - pyautogui
- para manipulação de imagens:
    - opencv
- para a extração de texto de imagens:
    - pytesseract

### Linguagem utilizada
- Python

### Funcionamento
Rodando no terminal 
```
python screenshot_para_texto.py
```
aparecerá a interface gráfica criada nesse código. Essa interface gráfica possui 2 botões e 1 caixa de texto.
- Botão de Nova captura: é o botão responsável por nos abrir a possibilidade de selecionar uma área da imagem ou da tela de interesse.
- **OBS.:** Para que a seleção seja efetiva, após selecionar a área de interesse deve-se apertar a tecla **ENTER** do teclado, dessa forma o resultado sairá na caixa de texto da interface gráfica. Caso tenha selecionado errado e queira selecionar novamente, deve-se apertar a tecla **C** do teclado. 
- Caixa de texto: é responsável por mostrar o texto extraído da imagem, após clicar no botão de Nova captura e clicar na tecla **ENTER** do teclado.
- Botão de Copiar texto: tendo o texto extraído na caixa de texto, esse botão, ao ser clicado, copia o texto para a área de transferência de forma que seja possível colá-lo em outro lugar.
- **OBS.:** Esse botão de Copiar texto não exclui, obviamente, a possibilidade de se selecionar o texto diretamente da caixa de texto. Foi implementado para facilitar esse processo.

### Uso
- crie um ambiente virtual na pasta do projeto, da forma:
```
python -m venv <nome-venv-sua-escolha>
```
- ative esse ambiente virtual criado:
```
<nome-venv-sua-escolha>\Scripts\activate
```
- instale todas as bibliotecas necessárias:
```
pip install -r requirements.txt
```
- **OBS.: se estiver rodando no Windows**, é necessário instalar o Tesseract para Windows. Portanto, acesse <a href="https://github.com/UB-Mannheim/tesseract/wiki">Tesseract para Windows</a> e baixe o instalador. Por esse motivo, na linha 25 do arquivo screenshot_para_texto.py, é passado o caminho do instalador na máquina. Se o seu instalador estiver em outro caminho, é necessário editar essa linha.
- rode o código do projeto:
```
python screenshot_para_texto.py
```

### Caso queira criar um executável
Rode
```
python setup.py build
```
O executável estará na pasta build criada no mesmo repositório. Para executar o arquivo executável:
```
build\<pasta-criada-dentro-de-build-com-exe>\screenshot_para_texto.exe
```

### Funcionando
<img src="https://github.com/brunatoloti/data-science-projects/blob/main/projeto-screenshot-para-texto/img/captura.gif" />