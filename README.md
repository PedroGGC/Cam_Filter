# Filters_cam

Um software de renderização em tempo real construído localmente em Python (Pygame e OpenCV) que captura a alimentação da sua webcam nativa e a converte de forma incrivelmente rápida.

Além do modo ASCII clássico (preto e branco em densidade configurável), o projeto conta com um Painel Retrátil Dinâmico que disponibiliza filtros criativos de imagem que usam aceleração em arrays nativos.

---

## Funcionalidades

- Mapeamento Vetorizado de Caracteres: A imagem capturada em ASCII não passa por lentos loops. Uma densidade de escala é mapeada de imediato via processamento nativo numpy.
- Painel Lateral Oculto: Na borda direita da tela, um clique simples expande um menu com propriedades de processamento e sliders sem interferir no framerate.
- Modo Tela Cheia Borderless: Usa 100% da resolução do seu monitor preservando funções importantes integradas ao OS, dispensando engasgos clássicos.
- Inversão Rápida: Pressionando a tecla I durante o uso puramente em letras, ocorre a reversão focal da malha.

---

## Filtros de Lente

Há pipelines paralelos de processamento que podem ser selecionados livremente no grid cinza:

1. Modo de Letras (Inativo): Leitura quantizada do brilho natural transposto via fontes cache mode quantificadas pelo pygame array pointer.
2. Deep Dive: Reduz agressivamente e quantiza paletas gerando visuais parecidos com fotografias desativadas retro antigas das maquinas de bits antigos.
3. Style: Um algoritmo vetor e stylization que emula traços artísticos diluindo o ruído a favor de massas de cores de agua mais cheias.
4. Neon Edges: Contrai e detecta bordas injetando dilatadores radioativos fluorescentes.
5. Glitch RGB: Interrompe e empurra frames RGB causando dissincronia virtual vermelha e azul (Efeito TV com sinal fraco).
6. Pixelate TV: Força uma interpolação por proximidade bruta transformando você em blocos massivos quadrados.
7. Pencil Sketch: Gera inversões blur sobre a paleta cinza desenhando o ambiente como obra em papel.
8. Cyberpunk: Mapa que desloca tonalidades pra rosa escuro contra branco e ciano usando LUTs em C++.

Através dos Sliders de Intensidade, há campos dinâmicos integrados para se digitar porcentagens de 0-100 para regular com precisão do teclado a mistura visual.

---

## Requisitos de Maquina e Instalacao

Para executar esse projeto voce precisa ter o **Python** instalado em sua maquina. Caso nao tenha, siga os passos abaixo para garantir que o ambiente seja configurado corretamente e comandos funcionem sem erros:

1. **Baixe o Python Oficial**: Acesse o site oficial atraves do link [https://www.python.org/downloads/](https://www.python.org/downloads/) e faca o download da versao mais recente para o Windows.
2. **Adicione o Python ao PATH**: Abra o executavel do instalador. Na primeira tela (antes de clicar em "Install Now"), marque obrigatoriamente a caixa de selecao que diz **"Add Python to PATH"** (ou "Add python.exe to PATH") no rodape da janela. Isso e critico para o proximo passo funcionar.

Se o seu Python ja estiver instalado e configurado, basta abrir o Prompt de Comando (CMD) ou PowerShell na pasta do projeto e executar a construcao final:

```bash
pip install opencv-python numpy pygame
```

---

## Como Comecar

Com tudo pronto, apenas ative a ferramenta utilizando:

python main.py

Para uso de atalhos e utilidades ao longo da utilizacao:

- Tecla Q ou ESC: Interrompe o processo finalizando com segurança a ocupação da sua webcam nativa.
- Tecla I: Inverte cores (Restrito ao modo padrao de teclado).


---

## Customizacoes Base

As cores do modo em letras podem ser modificadas logo no topo do arquivo main.py:

```python
FONT_SIZE = 14
FG_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
ASCII_CHARS = " .':-=+*#%@$"
```


