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
2. Gameboy Camera: Espreme as cores da sua camera forçando os 4 tons clássicos em blocos de pixels estilo Nintendo.
3. Blueprint Plan: Converte tudo em um papel azul fosco arquitetônico e detecta profundidade com derivados de matriz para giz branco e ciano.
4. CRT Monitor: Entorta as bordas simulando um tubo analógico antigo de TV convexa com scanlines horizontais escuras.
5. Halftone Art: Arte estilo jornal antigo. Troca a luz natural por uma ilusão de óptica com bolinhas de tinta espaçadas/largas em tons pretos e cinzas.
6. Ghost Trails: Fricciona todos os quadros passados segurando movimentos fantasma das bordas.
7. Neon Edges: Contrai e detecta bordas injetando dilatadores radioativos fluorescentes.
8. Pixelate TV: Força uma interpolação por proximidade bruta transformando você em blocos massivos quadrados.
9. Pencil Sketch: Gera inversões blur sobre a paleta cinza desenhando o ambiente como obra em papel.
10. Glitch RGB: Interrompe e empurra frames RGB causando dissincronia virtual vermelha e azul simulando falha.
11. Deep Dive: Reduz agressivamente e quantiza paletas gerando visuais retro.

Através dos Sliders de Intensidade, há campos dinâmicos integrados para se digitar porcentagens de 0-100 para regular com precisão do teclado a mistura visual.

---

## Requisitos de Maquina e Instalacao

Para executar esse projeto voce precisa ter o **Python** instalado em sua maquina. Caso nao tenha, siga os passos abaixo para garantir que o ambiente seja configurado corretamente e comandos funcionem sem erros:

1. **Baixe o Python Oficial**: Acesse o site oficial atraves do link [https://www.python.org/downloads/](https://www.python.org/downloads/) e faca o download da versao mais recente para o Windows.
2. **Adicione o Python ao PATH**: marque obrigatoriamente a caixa de selecao que diz **"Add Python to PATH"** (ou "Add python.exe to PATH") no rodape da janela.
Se o seu Python ja estiver instalado e configurado, basta abrir o Prompt de Comando (CMD) ou PowerShell na pasta do projeto e executar a construcao final:

```bash
pip install opencv-python numpy pygame pyvirtualcam
```

---

## Como Comecar o Projeto

O software se baseia em duas abordagens separadas de execução, depedendo da sua necessidade:

### 1. Uso Local Padrão (Full Screen)

Exibe a interface e roda a câmera visualmente grande no seu monitor para uso privado ou de teste fechado em tela cheia com atalhos de mouse.

No seu terminal, digite:

```bash
python main.py
```

### 2. Uso de Transmissão (Discord, OBS, etc.)

Esse método reduz a interface rodando localmente para uma janela fina estilo "Painel de Controle Remoto". Ele oculta o vídeo da sua tela primária, e passa a entregar a força total dos filtros silenciosamente num formato Universal de Webcam em plano de fundo pela sua placa de vídeo.

No terminal, digite:

```bash
python virtual_cam.py

---

## Atalhos do Sistema

- Tecla Q ou ESC: Interrompe o processo finalizando com segurança a ocupação da tela e do terminal.
- Tecla I: Inverte cores (Restrito ao modo nativo de letras ASCII).
```
