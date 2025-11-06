# 📌 Simulação da Trajetória de uma Partícula em Campos Elétricos e Magnéticos

Este projeto é uma **simulação interativa** desenvolvida em **VPython**,
permitindo visualizar em 3D o movimento de uma partícula carregada sob a
ação dos campos **E (elétrico)** e **B (magnético)**, incluindo também
gráficos de energia e componentes da velocidade.

A interface possui controles completos para ajustar parâmetros físicos e
acompanhar o comportamento da partícula em tempo real.

------------------------------------------------------------------------

## ✅ Funcionalidades

-   Visualização **3D** da partícula, vetor velocidade e vetor campo
    magnético.\
-   Ajuste de:
    -   Campo magnético **B (T)**\
    -   Campo elétrico **E (V/m)**\
    -   Carga **q (C)**\
    -   Massa **m (kg)**\
    -   Velocidade inicial **V (m/s)**\
-   Grelha tridimensional mostrando a direção do campo magnético.\
-   Cálculo automático do **raio da trajetória (R)** e **período (T)**
    quando ( `\vec{E}`{=tex} = 0 ).\
-   Gráficos em tempo real:
    -   Energia cinética ✅\
    -   Componentes de velocidade ✅\
-   Botões de **Play** e **Reset** para controle da simulação.\
-   Tema **dark**, estilizado com CSS diretamente no VPython.

------------------------------------------------------------------------

## 🧰 Tecnologias utilizadas

-   **Python**
-   **VPython**
-   **NumPy**
-   Renderização gráfica 3D integrada ao navegador via WebVPython

------------------------------------------------------------------------

## ▶️ Como executar

1.  Instale o VPython:

``` bash
pip install vpython numpy
```

2.  Execute o arquivo:

``` bash
python trabalho\ completo.py
```

3.  A simulação abrirá automaticamente no navegador.

------------------------------------------------------------------------

## 📂 Estrutura principal

-   **Simulação 3D:** partícula, vetores, grelha do campo B\
-   **Inputs:** campos para parâmetros físicos\
-   **Lógica física:** força de Lorentz, método de Euler melhorado\
-   **Gráficos:** energia cinética e componentes da velocidade\
-   **Estilização:** tema dark embutido via HTML/CSS

------------------------------------------------------------------------

## 🎯 Objetivo do projeto

Este código foi criado para fins didáticos, permitindo visualizar e
compreender o movimento de partículas carregadas em campos
eletromagnéticos. É ideal para estudos de Física, Eletromagnetismo ou
demonstrações em sala de aula.

------------------------------------------------------------------------

## 📜 Licença

Este projeto é de uso livre para fins acadêmicos. Adicione aqui sua
licença se desejar (MIT, GPL, etc).
