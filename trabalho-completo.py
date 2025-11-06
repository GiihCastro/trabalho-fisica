from vpython import *
import numpy as np

running = False
E_vetor = vector(0,0,0)
B_vetor = vector(0,0,0)
grid_B = []

def toggle_run(b):
    """Pausa ou inicia a simulação."""
    global running
    running = not running
    b.text = "Pause" if running else "Play"
    b.background = color.red if running else color.gray(0.25)

def reset_sim(b):
    # Globals
    global r_particula, v_particula, velocidade, particula, trajetoria, tempo, B_vetor, E_vetor, q, m, V_ajustado, B_ajustado, label_b, label_v, curva_K, curva_Vx, curva_Vy, curva_Vz, grid_B, texto_resultados
    
    try:
        # Lendo TODOS os campos
        new_Bx = float(BX_input.text)
        new_By = float(BY_input.text)
        new_Bz = float(BZ_input.text)
        new_Ex = float(EX_input.text)
        new_Ey = float(EY_input.text)
        new_Ez = float(EZ_input.text)
        new_q = float(Q_input.text)
        new_m = float(M_input.text)
        new_vx = float(VX_input.text)
        new_vy = float(VY_input.text)
        new_vz = float(VZ_input.text)
    except ValueError:
        print("Erro: Verifique se todos os campos de entrada contêm números válidos.")
        return
        
    q = new_q
    m = new_m
    B_vetor = vector(new_Bx, new_By, new_Bz)
    E_vetor = vector(new_Ex, new_Ey, new_Ez)

    # Lógica da Grelha 3D
    if mag(B_vetor) > 0:
        axis_grelha = hat(B_vetor) * 0.02 
        visivel = True
    else:
        axis_grelha = vector(0,0,0)
        visivel = False
    
    for seta in grid_B:
        seta.axis = axis_grelha
        seta.visible = visivel 

    r_particula = vector(0, 0, 0)
    v_particula = vector(new_vx, new_vy, new_vz)

    # Lógica do Cálculo Teórico (Missão 1)
    B_mag = mag(B_vetor)
    E_mag = mag(E_vetor)

    # Só calcula R e T se E=0, pois a fórmula só vale para campo B puro.
    if E_mag > 0:
        texto_resultados.text = "Cálculo de R/T não aplicável (E != 0)"
    elif B_mag == 0 or q == 0:
        texto_resultados.text = "R (Raio): Infinito (B ou q = 0)\nT (Período): Infinito (B ou q = 0)"
    else:
        B_hat = hat(B_vetor)
        v_para_mag = dot(v_particula, B_hat)
        v_para_vec = v_para_mag * B_hat
        v_perp_vec = v_particula - v_para_vec
        v_perp_mag = mag(v_perp_vec)

        if v_perp_mag == 0:
            R_teorico_str = "0 (v_perp = 0)"
        else:
            R_teorico = (m * v_perp_mag) / (abs(q) * B_mag)
            R_teorico_str = f"{R_teorico:.4e} m"

        T_teorico = (2 * pi * m) / (abs(q) * B_mag)
        T_teorico_str = f"{T_teorico:.4e} s"
        texto_resultados.text = f"R (Raio): {R_teorico_str}\nT (Período): {T_teorico_str}"


    # Reset dos Objetos 3D
    if mag(v_particula) > 0:
        V_ajustado = hat(v_particula) * 0.05
    else:
        V_ajustado = vector(0,0,0)

    if mag(B_vetor) > 0:
        B_ajustado = hat(B_vetor) * 0.05
    else:
        B_ajustado = vector(0,0,0)

    particula.pos = r_particula
    velocidade.pos = r_particula
    campo_b.pos = r_particula - B_ajustado/2
    trajetoria.clear()
    trajetoria.append(pos=r_particula)
    tempo = 0
    campo_b.axis = B_ajustado
    velocidade.axis = V_ajustado
    label_b.pos = campo_b.pos + campo_b.axis
    label_v.pos = velocidade.pos + velocidade.axis
    
    # Reset dos Gráficos (Missão 4)
    curva_K.delete()
    K_inicial = 0.5 * m * mag2(v_particula)
    curva_K.plot(0, K_inicial) 
    
    curva_Vx.delete()
    curva_Vy.delete()
    curva_Vz.delete()
    curva_Vx.plot(0, v_particula.x)
    curva_Vy.plot(0, v_particula.y)
    curva_Vz.plot(0, v_particula.z)

# ----------------- 1. CONFIGURAÇÃO DA CENA E CSS -----------------
scene.title = "<b>Trajetória de Partícula em Campo Eletromagnético</b>"
scene.width = 650
scene.height = 550
scene.autoscale = True
scene.range = 0.05

# --- Definições do Tema Escuro ---
BG_COLOR_SCENE = color.gray(0.1)
BG_COLOR_HTML = '#1e1e1e'
TEXT_COLOR_HTML = '#d4d4d4'
TEXT_COLOR_VPYTHON = color.gray(0.9)
ACCENT_COLOR_1 = '#9cdcfe'
ACCENT_COLOR_2 = '#4ec9b0'
INPUT_BG = '#3c3c3c'
INPUT_BORDER = '#555'

scene.background = BG_COLOR_SCENE 

# --- Estilização CSS ---
dark_style = f"""
<style>
    body {{
        background-color: {BG_COLOR_HTML};
        color: {TEXT_COLOR_HTML};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}
    canvas {{
        display: block !important;
        margin: 0 auto 20px auto !important;
        border-radius: 8px;
    }}
    /* Centraliza todo o conteúdo da legenda (inputs, botões, gráficos) */
    .jupwidgets {{
        width: 650px !important;
        margin: 0 auto !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }}
    /* Corrige labels do wtext */
    .jupwidgets > span[style*="width: 100%"] {{
        display: inline-block !important;
        width: auto !important;
        vertical-align: middle !important;
        margin-right: 5px !important;
        padding: 5px 0 !important;
    }}
    .jupwidgets input[type="text"] {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_COLOR_HTML} !important;
        border: 1px solid {INPUT_BORDER} !important;
        border-radius: 4px;
        padding: 6px;
        vertical-align: middle !important;
        box-sizing: border-box;
    }}
    .jupwidgets button {{
        background-color: #0e639c !important;
        color: white !important;
        border: none !important;
        border-radius: 4px;
        padding: 10px 25px;
        font-weight: bold;
        font-size: 1em;
        cursor: pointer;
        transition: background-color 0.2s;
        margin: 0 5px !important;
    }}
    .jupwidgets button:hover {{
        background-color: #1177bb !important;
    }}
    .graphs-container {{
        width: 650px;
        margin: 20px auto 0 auto;
    }}
</style>
"""
scene.append_to_caption(dark_style)

# --- LAYOUT DOS PARÂMETROS ---
wtext(text=f'<h3 style="color:{ACCENT_COLOR_2}; border-bottom: 2px solid #444; padding-bottom: 5px; margin-bottom: 15px;">Parâmetros da Simulação:</h3>')

wtext(text=f'<span style="color:{ACCENT_COLOR_1}; font-weight:bold;">Campo B (T):</span>')
wtext(text="<b>X:</b> ")
BX_input = winput(text='0', width=70, bind=None)
wtext(text=" <b>Y:</b> ")
BY_input = winput(text='0', width=70, bind=None)
wtext(text=" <b>Z:</b> ")
BZ_input = winput(text='0.5', width=70, bind=None)
wtext(text='\n')

wtext(text=f'<span style="color:{ACCENT_COLOR_1}; font-weight:bold;">Campo E (V/m):</span>')
wtext(text="<b>X:</b> ")
EX_input = winput(text='0', width=70, bind=None)
wtext(text=" <b>Y:</b> ")
EY_input = winput(text='0', width=70, bind=None)
wtext(text=" <b>Z:</b> ")
EZ_input = winput(text='0', width=70, bind=None)
wtext(text='\n')

wtext(text=f'<span style="color:{ACCENT_COLOR_1}; font-weight:bold;">Carga q (C):</span>')
Q_input = winput(text='1.602e-19', width=250, bind=None)
wtext(text='\n')

wtext(text=f'<span style="color:{ACCENT_COLOR_1}; font-weight:bold;">Massa m (kg):</span>')
M_input = winput(text='1.672e-27', width=250, bind=None)
wtext(text='\n')

wtext(text=f'<span style="color:{ACCENT_COLOR_1}; font-weight:bold;">Velocidade V (m/s):</span>')
wtext(text="<b>X:</b> ")
VX_input = winput(text='1e6', width=70, bind=None)
wtext(text=" <b>Y:</b> ")
VY_input = winput(text='0', width=70, bind=None)
wtext(text=" <b>Z:</b> ")
VZ_input = winput(text='0', width=70, bind=None)
wtext(text='\n\n')

# Botões
wtext(text='<div style="text-align: center; margin: 20px 0;">')
btn_play = button(text="Play", background=color.gray(0.25), bind=toggle_run)
btn_reset = button(text="Reset", bind=reset_sim)
wtext(text='</div>')

# Resultados Teóricos (Missão 1)
wtext(text=f'<h4 style="color:{ACCENT_COLOR_2}; margin-top: 15px;">Resultados Teóricos (para E=0):</h4>')
texto_resultados = wtext(text='R (Raio): -- m\nT (Período): -- s\n')

# Contêiner dos Gráficos
scene.append_to_caption('<div class="graphs-container">')

# ----------------- 2. OBJETOS GRÁFICOS -----------------
q = 1.602e-19 
m = 1.672e-27 
dt = 1e-9      

r_particula = vector(0, 0, 0)
v_particula = vector(1e6, 0, 0)
V_ajustado = hat(v_particula) * 0.05
B_ajustado = vector(0,0,0.05) # Placeholder

raio_esfera = 0.005
particula = sphere(pos=r_particula, radius=raio_esfera, color=color.yellow, make_trail=False)
campo_b = arrow(pos=vector(0, 0, 0) - B_ajustado/2, axis=B_ajustado, color=color.cyan, shaftwidth=raio_esfera/4)
label_b = label(pos=campo_b.pos + campo_b.axis, text='B', color=color.cyan, 
                xoffset=20, yoffset=10, background=BG_COLOR_SCENE, box=False, opacity=0.8)
velocidade = arrow(pos=r_particula, axis=V_ajustado, color=color.green, shaftwidth=raio_esfera/4)
label_v = label(pos=velocidade.pos + velocidade.axis, text='V', color=color.green, 
                xoffset=20, yoffset=10, background=BG_COLOR_SCENE, box=False, opacity=0.8)
trajetoria = curve(color=color.orange, radius=raio_esfera/10)

# Grelha 3D (Missão 3)
grid_range = 0.08 
grid_steps = 3    
posicoes = np.linspace(-grid_range, grid_range, grid_steps)
initial_axis = vector(0, 0, 0.02) # Placeholder, reset_sim corrige

for x in posicoes:
    for y in posicoes:
        for z in posicoes:
            if x == 0 and y == 0 and z == 0: # Não desenha na origem
                continue 
            
            seta_campo = arrow(
                pos=vector(x, y, z),
                axis=initial_axis,
                color=color.cyan, 
                opacity=0.3,       
                shaftwidth=raio_esfera / 6,
                visible=True
            )
            grid_B.append(seta_campo)

# Gráficos (Missão 4)
graph_K = graph(width=650, height=200, 
                   title="<b>Energia Cinética (K) vs. Tempo</b>", 
                   xtitle="Tempo (s)", ytitle="Energia (J)",
                   foreground=TEXT_COLOR_VPYTHON, background=BG_COLOR_SCENE)
curva_K = gcurve(color=color.cyan, label="K (simulado)")

graph_V = graph(width=650, height=200, 
                   title="<b>Componentes da Velocidade (V) vs. Tempo</b>", 
                   xtitle="Tempo (s)", ytitle="Velocidade (m/s)",
                   foreground=TEXT_COLOR_VPYTHON, background=BG_COLOR_SCENE)
curva_Vx = gcurve(color=color.red, label="Vx")
curva_Vy = gcurve(color=color.green, label="Vy")
curva_Vz = gcurve(color=color.magenta, label="Vz")

scene.append_to_caption('</div>') # Fecha o contêiner dos gráficos

# ----------------- 3. LOOP DE SIMULAÇÃO -----------------
tempo = 0
N_frames = 0
reset_sim(None) # Chama o reset_sim para carregar tudo

while True:
    rate(100) 
    if running:
        # --- Cálculo da Força de Lorentz (Método de Euler Melhorado) ---
        produto_vetorial_i = cross(v_particula, B_vetor)
        F_i = q * (E_vetor + produto_vetorial_i)
        a_i = F_i / m
        
        v_trial = v_particula + a_i * dt
        
        produto_vetorial_trial = cross(v_trial, B_vetor)
        F_trial = q * (E_vetor + produto_vetorial_trial)
        a_trial = F_trial / m
        
        a_media = 0.5 * (a_i + a_trial)
        v_particula = v_particula + a_media * dt
        r_particula = r_particula + v_particula * dt 

        # --- Atualização 3D ---
        particula.pos = r_particula
        velocidade.pos = r_particula
        
        if mag(v_particula) > 0: 
            V_ajustado = hat(v_particula) * 0.05
            velocidade.axis = V_ajustado
            label_v.pos = velocidade.pos + velocidade.axis
        else:
            velocidade.axis = vector(0,0,0)
            label_v.pos = r_particula
            
        trajetoria.append(pos=r_particula)

        # --- Plotagem dos Gráficos ---
        K = 0.5 * m * mag2(v_particula)
        curva_K.plot(tempo, K)
        
        curva_Vx.plot(tempo, v_particula.x)
        curva_Vy.plot(tempo, v_particula.y)
        curva_Vz.plot(tempo, v_particula.z)
        
        tempo += dt
        N_frames += 1
