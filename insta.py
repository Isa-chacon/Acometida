# Librerias a utilizar
import streamlit as st
import pandas as pd
import numpy as np
import math
import copy

# Configuración de la página
st.set_page_config(page_title="Cálculo de Acometida", layout="wide")

# Personalización de estilo 
st.markdown("""
    <style>
    .css-18e3th9, .css-1y4v4l9, .css-1v0mbdj {background-color: lavenderblush; color: blue;}
    .css-1l0l5lz {color: white;}
    .title {text-align: center; font-size: 40px; font-weight: bold; color: blue;}  
    [data-testid="stSidebar"] {background-color: mistyrose;}
    .subheader {text-align: center; font-size: 20px; font-weight: bold; color: cadetblue;}
    .p {text-align: left; font-size: 10px; font-weight: bold; color: black;}
    .error-message {color: red; font-size: 18px; font-weight: bold;}
    
    /* Estilo personalizado para el botón */
    div.stButton > button {
        background-color: #008B8B;  /* Color azul */
        color: white;  /* Color del texto */
        font-size: 18px;  /* Tamaño de la fuente */
        border-radius: 5px;  /* Bordes redondeados */
        padding: 10px 20px;  /* Tamaño del botón */
        width: 200px;  /* Ancho del botón */
        text-align: center;  /* Centrado del texto */
        border: none;  /* Quitar borde */
        cursor: pointer;  /* Cambiar el cursor al pasar el mouse */
        display: block;  /* Para centrarlo */
        margin: 0 auto;  /* Margen automático para centrar */
    }

    div.stButton > button:hover {
        background-color: #008B8B;  /* Color azul más oscuro al pasar el mouse */
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

############################### MATRICES ###########################

#PARA 60°C SE USA TERMOPLASTICO TW, PARA 75°C THW Y PARA 90THHW
#   SI ES SUPERFICIAL BANDEJA, SI ES EMPOTRADA EMT Y SI ES SUBTERRANEA DUCTO

# TABLA 315(B).16 UBICADA EN LA PAG 192 DE LA NTC 2050

aluminio = [
    ['Calibre', 'T_cable', 'Imax', 'R'],
    ['6 AWG', 60, 40, 2.168],
    ['6 AWG', 75, 50, 2.168],
    ['6 AWG', 90, 60, 2.168],
    ['4 AWG', 60, 55, 1.363],
    ['4 AWG', 75, 65, 1.363],
    ['4 AWG', 90, 75, 1.363],
    ['2 AWG', 60, 75, 0.8573],
    ['2 AWG', 75, 90, 0.8573],
    ['2 AWG', 90, 135, 0.8573],
    ['1/0 AWG', 60, 120, 0.4275],
    ['1/0 AWG', 75, 120, 0.4275],
    ['1/0 AWG', 90, 135, 0.4275],
    ['2/0 AWG', 60, 135, 0.3389],
    ['2/0 AWG', 75, 155, 0.3389],
    ['2/0 AWG', 90, 175, 0.3389],
    ['3/0 AWG', 60, 155, 0.269],
    ['3/0 AWG', 75, 180, 0.269],
    ['3/0 AWG', 90, 205, 0.269],
    ['4/0 AWG', 60, 180, 0.2272],
    ['4/0 AWG', 75, 205, 0.2272],
    ['4/0 AWG', 90, 230, 0.2272],
    ['250 kcmil', 60, 205, 0.1624],
    ['250 kcmil', 75, 205, 0.1624],
    ['250 kcmil', 90, 230, 0.1624],
    ['350 kcmil', 60, 250, 0.1297],
    ['350 kcmil', 75, 250, 0.1297],
    ['350 kcmil', 90, 270, 0.1297],
    ['500 kcmil', 60, 310, 0.1139],
    ['500 kcmil', 75, 310, 0.1139],
    ['500 kcmil', 90, 350, 0.1139],
    ['600 kcmil', 60, 340, 0.0941],
    ['600 kcmil', 75, 375, 0.0941],
    ['600 kcmil', 90, 420, 0.0941],
    ['700 kcmil', 60, 375, 0.0808],
    ['700 kcmil', 75, 415, 0.0808],
    ['700 kcmil', 90, 460, 0.0808],
    ['750 kcmil', 60, 385, 0.0745],
    ['750 kcmil', 75, 435, 0.0745],
    ['750 kcmil', 90, 475, 0.0745],
    ['800 kcmil', 60, 395, 0.0707],
    ['800 kcmil', 75, 445, 0.0707],
    ['800 kcmil', 90, 490, 0.0707],
    ['900 kcmil', 60, 425, 0.0639],
    ['900 kcmil', 75, 480, 0.0639],
    ['900 kcmil', 90, 530, 0.0639],
    ['1000 kcmil', 60, 445, 0.0584],
    ['1000 kcmil', 75, 500, 0.0584],
    ['1000 kcmil', 90, 545, 0.0584],
]

cobre = [
    ['Calibre', 'T_cable', 'Imax', 'R'],
    ['14 AWG', 60, 15, 8.28],
    ['14 AWG', 75, 20, 8.28],
    ['14 AWG', 90, 25, 8.28],
    ['12 AWG', 60, 20, 5.21],
    ['12 AWG', 75, 25, 5.21],
    ['12 AWG', 90, 30, 5.21],
    ['10 AWG', 60, 30, 3.35],
    ['10 AWG', 75, 35, 3.35],
    ['10 AWG', 90, 40, 3.35],
    ['8 AWG', 60, 40, 2.1],
    ['8 AWG', 75, 50, 2.1],
    ['8 AWG', 90, 55, 2.1],
    ['6 AWG', 60, 55, 1.32],
    ['6 AWG', 75, 65, 1.32],
    ['6 AWG', 90, 75, 1.32],
    ['4 AWG', 60, 70, 0.83],
    ['4 AWG', 75, 85, 0.83],
    ['4 AWG', 90, 95, 0.83],
    ['2 AWG', 60, 95, 0.659],
    ['2 AWG', 75, 115, 0.659],
    ['2 AWG', 90, 130, 0.659],
    ['1/0 AWG', 60, 150, 0.261],
    ['1/0 AWG', 75, 150, 0.261],
    ['1/0 AWG', 90, 170, 0.261],
    ['2/0 AWG', 60, 175, 0.207],
    ['2/0 AWG', 75, 175, 0.207],
    ['2/0 AWG', 90, 195, 0.207],
    ['3/0 AWG', 60, 200, 0.164],
    ['3/0 AWG', 75, 200, 0.164],
    ['3/0 AWG', 90, 225, 0.164],
    ['4/0 AWG', 60, 230, 0.139],
    ['4/0 AWG', 75, 230, 0.139],
    ['4/0 AWG', 90, 260, 0.139],
    ['250 kcmil', 60, 255, 0.0991],
    ['250 kcmil', 75, 255, 0.0991],
    ['250 kcmil', 90, 290, 0.0991],
    ['350 kcmil', 60, 310, 0.0777],
    ['350 kcmil', 75, 310, 0.0777],
    ['350 kcmil', 90, 350, 0.0777],
    ['500 kcmil', 60, 380, 0.0695],
    ['500 kcmil', 75, 380, 0.0695],
    ['500 kcmil', 90, 430, 0.0695],
    ['600 kcmil', 60, 420, 0.0575],
    ['600 kcmil', 75, 455, 0.0575],
    ['600 kcmil', 90, 505, 0.0575],
    ['700 kcmil', 60, 460, 0.0494],
    ['700 kcmil', 75, 510, 0.0494],
    ['700 kcmil', 90, 560, 0.0494],
    ['750 kcmil', 60, 475, 0.0465],
    ['750 kcmil', 75, 535, 0.0465],
    ['750 kcmil', 90, 585, 0.0465],
    ['800 kcmil', 60, 490, 0.0432],
    ['800 kcmil', 75, 555, 0.0432],
    ['800 kcmil', 90, 600, 0.0432],
    ['900 kcmil', 60, 520, 0.0390],
    ['900 kcmil', 75, 585, 0.0390],
    ['900 kcmil', 90, 645, 0.0390],
    ['1000 kcmil', 60, 545, 0.0357],
    ['1000 kcmil', 75, 615, 0.0357],
    ['1000 kcmil', 90,675,0.0357],
]


# TABLA C.1 PAG 983 NTC2050
# Factor de llenado máximo: 53% para un solo conductor xfase  y 31% 2 conductores x fase y 40% para mas de 2 conductores 
# según la tabla 1 CAPITULO 9 de la NTC2050. PAG 954

canalizacion = [
    ["Calibre", '½"', '¾"', '1"', '1¼"', '1½"', '2"', '2½"', '3"', '3½"', '4"'],
    ['14 AWG', 7, 12, 20, 34, 44, 70, 104, 157, 201, 261],
    ['12 AWG', 6, 10, 16, 27, 35, 56, 84, 126, 163, 211],
    ['10 AWG', 4, 8, 12, 18, 28, 44, 66, 99, 128, 166],
    ['8 AWG', 2, 4, 8, 12, 16, 26, 39, 59, 77, 99],
    ['6 AWG', 1, 3, 6, 9, 13, 20, 30, 45, 58, 76],
    ['4 AWG', 1, 2, 4, 5, 7, 11, 22, 24, 36, 46],
    ['2 AWG', 1, 1, 3, 5, 7, 11, 17, 17, 28, 36],
    ['1 AWG', 1, 1, 3, 5, 6, 10, 14, 14, 24, 31],
    ["1/0 AWG", 0, 1, 1, 3, 5, 6, 10, 10, 18, 23],
    ["2/0 AWG", 0, 1, 1, 2, 3, 4, 7, 7, 15, 19],
    ["3/0 AWG", 0, 1, 1, 2, 3, 4, 6, 6, 13, 16],
    ["4/0 AWG", 0, 1, 1, 1, 2, 2, 4, 6, 11, 14],
    ["250 kcmil", 1, 1, 1, 1, 3, 5, 7, 10, 12, 15],
    ["300 kcmil", 1, 1, 1, 1, 2, 4, 6, 8, 10, 13],
    ["350 kcmil", 1, 1, 1, 1, 2, 3, 5, 7, 9, 11],
    ["400 kcmil", 1, 1, 1, 1, 2, 3, 5, 6, 8, 10],
    ["500 kcmil", 1, 1, 1, 1, 2, 3, 4, 5, 7, 9],
    ["600 kcmil", 0, 0, 1, 1, 1, 2, 3, 4, 6, 7],
    ["700 kcmil", 0, 0, 1, 1, 1, 1, 3, 4, 5, 6],
    ["750 kcmil", 0, 0, 1, 1, 1, 1, 2, 3, 5, 6],
    ["800 kcmil", 0, 0, 0, 1, 1, 1, 2, 3, 4, 5],
    ["900 kcmil", 0, 0, 0, 1, 1, 1, 2, 3, 4, 5],
    ["1000 kcmil", 0, 0, 0, 1, 1, 1, 1, 2, 3, 4],
]

# Tabla para bandejas portacables según NTC 2050 (Artículo 318)
# Factor de llenado máximo: 40% para un solo conductor y 30% para múltiples conductores
# Estas dimensiones son basadas en la tabla 318-9 de la NTC 2050

bandeja = [
    ["Calibre", '50mm', '100mm', '150mm', '225mm', '300mm', '450mm', '600mm', '900mm'],
    # AWG/kcmil, cantidad máxima de conductores permitidos
    ['14 AWG', 30, 64, 96, 142, 190, 285, 380, 570],
    ['12 AWG', 24, 51, 76, 113, 151, 226, 301, 452],
    ['10 AWG', 15, 32, 48, 71, 95, 143, 191, 286],
    ['8 AWG', 8, 18, 27, 40, 53, 80, 107, 161],
    ['6 AWG', 6, 12, 19, 28, 38, 57, 76, 114],
    ['4 AWG', 3, 7, 11, 17, 23, 34, 46, 69],
    ['2 AWG', 2, 4, 7, 10, 14, 21, 28, 42],
    ['1 AWG', 1, 3, 5, 8, 11, 16, 21, 32],
    ["1/0 AWG", 1, 3, 4, 7, 9, 14, 18, 27],
    ["2/0 AWG", 1, 2, 3, 5, 7, 11, 15, 23],
    ["3/0 AWG", 1, 1, 3, 4, 6, 9, 12, 18],
    ["4/0 AWG", 1, 1, 2, 3, 5, 7, 10, 15],
    ["250 kcmil", 0, 1, 1, 3, 4, 6, 8, 12],
    ["300 kcmil", 0, 1, 1, 2, 3, 5, 7, 10],
    ["350 kcmil", 0, 1, 1, 2, 3, 4, 6, 9],
    ["400 kcmil", 0, 1, 1, 1, 3, 4, 5, 8],
    ["500 kcmil", 0, 0, 1, 1, 2, 3, 4, 6],
    ["600 kcmil", 0, 0, 1, 1, 1, 2, 3, 5],
    ["750 kcmil", 0, 0, 1, 1, 1, 2, 3, 4],
    ["1000 kcmil", 0, 0, 0, 1, 1, 1, 2, 3]
]

# Tabla para ductos subterráneos según NTC 2050 (Artículo 346)
# Basado en tabla 1 del capítulo 9 de la NTC 2050 (factor de llenado máximo: 53% para un conductor,
# 31% para dos conductores, 40% para tres o más conductores)

ducto = [
    ["Calibre", '16mm', '21mm', '27mm', '35mm', '41mm', '53mm', '63mm', '78mm', '91mm', '103mm'],
    # AWG/kcmil, cantidad máxima de conductores permitidos según diámetro del ducto
    ['14 AWG', 6, 10, 16, 28, 40, 68, 95, 150, 201, 257],
    ['12 AWG', 4, 7, 12, 21, 30, 52, 72, 114, 153, 195],
    ['10 AWG', 3, 6, 10, 17, 24, 41, 58, 91, 122, 156],
    ['8 AWG', 1, 3, 5, 9, 12, 22, 30, 48, 64, 82],
    ['6 AWG', 1, 1, 3, 5, 8, 14, 19, 31, 41, 53],
    ['4 AWG', 0, 1, 2, 4, 6, 10, 14, 22, 30, 38],
    ['2 AWG', 0, 1, 1, 3, 4, 7, 10, 16, 21, 27],
    ['1 AWG', 0, 0, 1, 2, 3, 6, 8, 13, 17, 22],
    ["1/0 AWG", 0, 0, 1, 1, 3, 5, 7, 11, 15, 19],
    ["2/0 AWG", 0, 0, 1, 1, 2, 4, 6, 9, 12, 16],
    ["3/0 AWG", 0, 0, 1, 1, 1, 3, 5, 8, 10, 13],
    ["4/0 AWG", 0, 0, 0, 1, 1, 3, 4, 6, 8, 11],
    ["250 kcmil", 0, 0, 0, 1, 1, 2, 3, 5, 7, 9],
    ["300 kcmil", 0, 0, 0, 1, 1, 1, 3, 4, 6, 8],
    ["350 kcmil", 0, 0, 0, 0, 1, 1, 2, 4, 5, 7],
    ["400 kcmil", 0, 0, 0, 0, 1, 1, 2, 3, 5, 6],
    ["500 kcmil", 0, 0, 0, 0, 1, 1, 1, 3, 4, 5],
    ["600 kcmil", 0, 0, 0, 0, 0, 1, 1, 2, 3, 4],
    ["750 kcmil", 0, 0, 0, 0, 0, 1, 1, 1, 3, 3],
    ["1000 kcmil", 0, 0, 0, 0, 0, 0, 1, 1, 2, 2]
]

############################### FUNCIONES ###########################

# La función de cálculos basicos calcula las variables necesarios para poder dimensionar la acometida

def calculos_basicos (potencia,tipo_sistema,voltaje, ambiente,fp,tipofp):
    
    if fp == 1:        
        u = 0
        if tipo_sistema == "Monofásico":
          corriente = (potencia * np.cos(u) ) / voltaje
        elif tipo_sistema == "Trifásico":
          corriente = (potencia * np.cos(u) ) / (np.sqrt(3) * voltaje)
    else:
        
        #No hay diferencia entre inductivo y capacitivo en la magnitud de la corriente porque el coseno se come el negativo
        if tipofp == 'Inductivo':
            if tipo_sistema == "Monofásico":
                corriente = (potencia * fp ) / voltaje
            elif tipo_sistema == "Trifásico":
                corriente = (potencia * fp) / (np.sqrt(3) * voltaje)

        elif tipofp == 'Capacitivo':
            if tipo_sistema == "Monofásico":
                corriente = (potencia * fp ) / voltaje
            elif tipo_sistema == "Trifásico":
                corriente = (potencia * fp ) / (np.sqrt(3) * voltaje)

    if tipo_sistema == "Monofásico":
        cant_conductores = 3  # Fase, neutro y tierra
        fase = 1
    elif tipo_sistema == "Trifásico":
        cant_conductores = 4  # L1, L2, L3 y tierra
        fase =3

    I_acometida = corriente * 1.25

    if I_acometida < 100:
        T_cable = 60
    else:
        if ambiente == 'Seco':
            T_cable = 75
        elif ambiente == 'Seco/Humedo':
            T_cable = 90

    return cant_conductores, I_acometida, T_cable, fase

# La función de corrección de temperatura toma las matrices de los cables de cobre y aluminio 
#y les modifica la capacidad de corriente de acuerdo con la corrección por temperatura 

def T_correccion(tambiente, toperacion, matriz):
    factores = {(21, 25): {60: 1.08, 75: 1.05, 90: 1.04},
                (26, 30): {60: 1.00, 75: 1.00, 90: 1.00},
                (31, 35): {60: 0.91, 75: 0.94, 90: 0.96},
                (36, 40): {60: 0.82, 75: 0.88, 90: 0.91}}

    fcorreccion = 1.00
    for rango, valores in factores.items():
        if rango[0] <= tambiente <= rango[1]:
            fcorreccion = valores.get(toperacion, 1.00)
            break

    nueva_matriz = copy.deepcopy(matriz)
    nueva_matriz = np.array(nueva_matriz, dtype=object)
    nueva_matriz[1:, 2] = nueva_matriz[1:, 2].astype(float) * fcorreccion

    return nueva_matriz.tolist()

# Esta función selecciona el cablibre del cable de acuerdo con la corriente maxima y cersiorandose de que no se supere el 3% en la regulación de voltaje, 
#si no encuentra un calibre que sirva devuelve un NA

def seleccionar_calibre(matriz, T_cable, I_max, fases, longitud, voltaje, conductores_por_fase=1):
    matriz_filtrada = sorted(
        [fila for fila in matriz[1:] if fila[1] == T_cable and fila[2] >= I_max / conductores_por_fase],
        key=lambda x: x[2]
    )

    if not matriz_filtrada:
        return ["NA", T_cable, 0, 0, 0]  # Retornar NA si no se encuentran conductores adecuados

    divisor = np.sqrt(3) * 1000 if fases == 3 else 1000

    # Encontrar el primer conductor que cumpla con la regulación de voltaje
    for conductor in matriz_filtrada:
        caida_tension = (conductor[3] * longitud * I_max / divisor) * 100 / voltaje / conductores_por_fase
        if caida_tension <= 3:
            return conductor + [round(caida_tension, 3)]

    # Si ningún conductor cumple con la regulación de voltaje
    return ["NA", T_cable, 0, 0, 0]

#Esta función calcula la canalización a utilizar según los criterios de entrada dados por el usuario y el calibre seleccionado
#basado en tablas de la NTC2050 que especifican la capacidad maxima de la canalización por calibre utilizado para no superar los porcentajes de ocupación requeridos
#Si es superficial usa bandeja
#si es empodtrada usa conduit
#si es subterranea usa ducto

def buscar_canalizacion(calibre, n, tipo_canalizacion, ubicacion):
    # Seleccionar la tabla adecuada según la ubicación
    if ubicacion == "Superficial":
        tabla = bandeja
    elif ubicacion == "Empotrada":
        tabla = canalizacion  # Esta es tu tabla original de conduit
    elif ubicacion == "Subterránea":
        tabla = ducto
    else:
        return "Ubicación no válida"

    # Nombre del tipo de canalización
    if ubicacion == "Superficial":
        tipo = "Bandeja"
    elif ubicacion == "Empotrada":
        tipo = "Conduit"
    elif ubicacion == "Subterránea":
        tipo = "Ducto"

    # Buscar la fila correspondiente al calibre
    for fila in tabla[1:]:  # Ignorar la primera fila (encabezados)
        if fila[0] == calibre:
            # Recorrer la fila para encontrar el primer valor >= n
            for i in range(1, len(fila)):
                if fila[i] >= n:
                    return tipo, tabla[0][i]  # Retornar el tipo y la dimensión

    return tipo, "No encontrado"  # En caso de que no haya coincidencias

# esta función es para seleccionar el aislante del cable según la temperatura del cable, como se menciona en el codigo este cable es sólo para '''

def insulating (T_cable):
  if T_cable == 60:
    aislante = 'TW'
  elif T_cable == 75:
    aislante = 'THW'
  elif T_cable == 90:
    aislante = 'THHW'
  return aislante

############################### INTERFAZ ###########################

st.markdown("<h1 class='title'>Cálculo de Acometida</h1>", unsafe_allow_html=True)

st.markdown("<h1 class='p'> Consideraciones para el cálculo de su acometida eléctrica: </h1>", unsafe_allow_html=True)
st.markdown("""
- Con esta aplicación obtendrá 4 opciones para su acometida con cable de cobre y aluminio, y con 1 y 2 conductores por fase.
- Los termoplásticos considerados son TW, THW y THHW.
- Este cálculo admite temperaturas ambiente entre 21 y 40°C.
- Si el sistema no encuentra un cálibre adecuado para su acometida en el valor del cálibre se evidenciará "NA".
- El calibre indicado se recomienda para las fases, el neutro y la tierra.
""")

st.link_button("Ver tutorial", "https://uninorte-my.sharepoint.com/:f:/g/personal/imchacon_uninorte_edu_co/EteS2J884clCjUExmLOj07ABexGOt-7pBWxJq2kaeuPFzQ?e=Xp4z6I")

st.markdown("<h2 class='subheader'>Datos de entrada: </h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    potencia = st.number_input('Digite la demanda (VA):', min_value=1)
    longitud = st.number_input('Distancia de recorrido (m):', min_value=1)
    fp = st.number_input('Digite el factor de potencia:', min_value=0.0, max_value=1.0,value=1.0)
    

with col2:
    tipo_sistema = st.selectbox("Seleccione el número de fases:", ["Monofásico", "Trifásico"])        
    tension = st.number_input('Digite el nivel de tensión (V):', min_value=1)
    if fp == 1:
        tipofp = st.selectbox("Seleccione el tipo de factor de potencia:", ['Resistivo']) 
    else:
        tipofp = st.selectbox("Seleccione el tipo de factor de potencia:", ["Inductivo", "Capacitivo"]) 
        
with col3:
    T_ambiente = st.number_input('Digite la temperatura ambiente (°C):', min_value=21, max_value=40)
    ambiente = st.selectbox("Seleccione el tipo de ambiente: ", ["Seco", "Seco/Humedo"])
    ubicacion = st.selectbox("Seleccione la ubicación de la acometida: ", ["Superficial", "Empotrada",'Subterránea'])

if st.button("Calcular Acometida"):
    
    # Verificar si alguna variable está vacía
    if not all([potencia, longitud, tipo_sistema, tension, T_ambiente, ambiente]):
        st.markdown('<p class="error-message">Información de entrada incompleta. Por favor, complete todos los campos.</p>', unsafe_allow_html=True)
    else:
        n_conductores, imax, T_cable, fase = calculos_basicos(potencia, tipo_sistema, tension, ambiente, fp, tipofp)  

        cobre_corregida = T_correccion(T_ambiente, T_cable, cobre)
        aluminio_corregida = T_correccion(T_ambiente, T_cable, aluminio)
        
        aluminio_uno = seleccionar_calibre(aluminio_corregida, T_cable, imax, fase, longitud, tension, conductores_por_fase=1)
        cobre_uno = seleccionar_calibre(cobre_corregida, T_cable, imax, fase, longitud, tension, conductores_por_fase=1)

        aluminio_dos = seleccionar_calibre(aluminio_corregida, T_cable, imax, fase, longitud, tension, conductores_por_fase=2)
        cobre_dos = seleccionar_calibre(cobre_corregida, T_cable, imax, fase, longitud, tension, conductores_por_fase=2)

        # Número total de conductores (considerando fase, neutro y tierra)
        total_conductores_1c = n_conductores
        total_conductores_2c = n_conductores * 2  # Doble para el caso de 2 conductores por fase
        
        # Buscar canalización adecuada
        tipo_canal_1c_cu, dim_canal_1c_cu = buscar_canalizacion(cobre_uno[0], total_conductores_1c, canalizacion, ubicacion) if cobre_uno[0] != "NA" else ("NA", "NA")
        tipo_canal_1c_al, dim_canal_1c_al = buscar_canalizacion(aluminio_uno[0], total_conductores_1c, canalizacion, ubicacion) if aluminio_uno[0] != "NA" else ("NA", "NA")
        tipo_canal_2c_cu, dim_canal_2c_cu = buscar_canalizacion(cobre_dos[0], total_conductores_2c, canalizacion, ubicacion) if cobre_dos[0] != "NA" else ("NA", "NA")
        tipo_canal_2c_al, dim_canal_2c_al = buscar_canalizacion(aluminio_dos[0], total_conductores_2c, canalizacion, ubicacion) if aluminio_dos[0] != "NA" else ("NA", "NA")

        aislante = insulating(T_cable)
        
        # Crear la tabla de diseño con los valores calculados
        diseño = [
            ['Calibre', 'Material', 'Aislante', 'I_acometida [A]', 'Imax_conductor [A]', 'T_cable [°C]', 'Conductores x fase', 'Tipo Canalización', 'Dimensión', '%RV'],
            [cobre_uno[0], 'Cobre', aislante, imax, cobre_uno[2] if cobre_uno[0] != "NA" else 0, T_cable, 1, tipo_canal_1c_cu, dim_canal_1c_cu, cobre_uno[4] if len(cobre_uno) > 4 else 0],
            [aluminio_uno[0], 'Aluminio', aislante, imax, aluminio_uno[2] if aluminio_uno[0] != "NA" else 0, T_cable, 1, tipo_canal_1c_al, dim_canal_1c_al, aluminio_uno[4] if len(aluminio_uno) > 4 else 0],
            [cobre_dos[0], 'Cobre', aislante, imax, 2*cobre_dos[2] if cobre_dos[0] != "NA" else 0, T_cable, 2, tipo_canal_2c_cu, dim_canal_2c_cu, cobre_dos[4] if len(cobre_dos) > 4 else 0],
            [aluminio_dos[0], 'Aluminio', aislante, imax, 2*aluminio_dos[2] if aluminio_dos[0] != "NA" else 0, T_cable, 2, tipo_canal_2c_al, dim_canal_2c_al, aluminio_dos[4] if len(aluminio_dos) > 4 else 0],
        ]
        
        st.write('')
        
        tabla_diseño = pd.DataFrame(diseño[1:], columns=diseño[0])
        
        st.dataframe(tabla_diseño, use_container_width=True)


