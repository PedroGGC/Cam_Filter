# ASCIICamera 📸💻

Um software de renderização em tempo real construído localmente em Python (`Pygame` e `OpenCV`) que captura a alimentação da sua webcam nativa e a converte de forma incrivelmente rápida para Matrizes de caracteres ASCII.

Além do modo ASCII clássico (preto e branco em densidade configurável), o projeto conta com um **Painel Retrátil Dinâmico** que disponibiliza 5 filtros de imagem que usam acelerações do Numpy e convoluções reais via OpenCV.

![ASCIICamera - Real-time Preview]((Imagem de Exemplo Omitida))

---

## 🌟 Funcionalidades

- **Mapeamento Vetorizado de Caracteres**: A imagem capturada não passa por lentos loops em Python; ao invés disso, uma densidade de escala de 12 níveis de luz é mapeada imediatamente em processamento nativo via Numpy C-arrays.
- **Painel Lateral Toggleable**: Na borda direita da tela, um botão em forma de seta (`◀`/`▶`) exibe ou recolhe um menu cheio de propriedades de processamento de imagem sem interferir no FPS ou causar esticamentos de aspect-ratio.
- **Modo Tela Cheia Borderless**: Usa 100% da resolução do seu monitor preservando funções importantes de janelas como Alt-Tab e PrintScreen integradas pelo SO (eliminando travamentos de _exclusive fullscreens_ clássicos).
- **Inversão Rápida**: Pressione a tecla `I` durante o modo de visualização puramente ASCII para inverter as paletas de cores e gerar um fundo branco sólido para leitura distinta no escuro.

---

## 🎨 Filtros Embutidos (Painel Lateral)

O projeto possui dois pipelines paralelos completamente diferentes que não entram em conflito e você pode chavear livremente clicando neles no painel direito:

1. **Modo ASCII Puro (Inativo)**: Pipeline que lê os pixels de brilho, quantiza as matrizes, e desenha fontes pré-armazenadas (_font pre-rendering cache_) via o draw engine de `.blits()` do pygame. É o estado inicial.
2. **Grayscale**: Exibe a imagem direta combinando a força de saturação entre imagem colorida padrão e preto-e-branco.
3. **Deep Dive**: Sub-quantiza todos os canais de cor da cena (R,G,B). Em intensidade `0.5`, gera imagens pesadamente posterizadas muito parecidas com fotografias pixel-arts ou jogos retro (sem dithering).
4. **Noise**: Injúria de sinal estático. Somam-se níveis controlados de pixels aleatórios ao frame.
5. **Embossed**: Roda um filtro com _Kernel Espacial_ `2D` para calcular os gradientes e revelar as bordas ressaltadas/côncavas da alimentação como se estivessem engravadas no cimento.
6. **Style**: Usa uma rede neural ultra-rápida implementada pelo OpenCV (`cv2.stylization`) executada em meia resolução. Esse filtro dá um forte caráter de pintura à base de água colorida para qualquer ambiente.

> _Dica:_ Ao habilitar qualquer filtro, você tem um **Slider de Intensidade (%)** respectivo abaixo do nome dele para ter o total controle do blend entre frame original <=> frame modificado.

---

## 🚀 Instalação e Execução

Você precisará de Python `>=3.7` instalado em sua máquina.

1. **Clone da pasta**
   Acesse a pasta correspondente no seu explorador e instale todas as dependências na sua linha de comando:

   ```bash
   pip install opencv-python numpy pygame
   ```

2. **Inicie o script**

   ```bash
   python main.py
   ```

3. **Uso de Teclas**:
   - **Aperte `Q`** ou **`ESC`** a qualquer instante para fechar o programa e desativar sua webcam.
   - **Aperte `I`** para alternar a inversão de cores (válido somente no painel original invisível para ASCII).
   - **Clique no seletor de canto direito:** Para expor ou puxar de volta o painel cinza de filtros.

---

## 🛠️ Modificando as Cores

As cores podem ser facilmente ajustadas alterando as constantes localizadas nas primeiras 10 linhas do arquivo `main.py`:

```python
FONT_SIZE = 14
FG_COLOR = (255, 255, 255)  # Branco - Cor principal da fonte ASCII
BG_COLOR = (0, 0, 0)        # Preto - Fundo
ASCII_CHARS = " .':-=+*#%@$"  # Do mais escuro para o mais claro
```

_Experimente mudar o `FG_COLOR` para `(0, 255, 65)` para voltar à clássica paleta Verde tipo Matrix!_
