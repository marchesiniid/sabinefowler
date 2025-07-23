import streamlit as st

# Tabla de Sabine-Fowler (ANSI 1971)
tabla = {
    10: {500:0.2, 1000:0.3, 2000:0.4, 4000:0.1},
    15: {500:0.5, 1000:0.9, 2000:1.3, 4000:0.3},
    20: {500:1.1, 1000:2.1, 2000:2.9, 4000:0.9},
    25: {500:1.8, 1000:3.6, 2000:4.9, 4000:1.7},
    30: {500:3.6, 1000:5.4, 2000:7.3, 4000:2.7},
    35: {500:3.7, 1000:7.7, 2000:9.8, 4000:3.8},
    40: {500:4.9, 1000:10.2,2000:12.9,4000:5.0},
    45: {500:6.3, 1000:13.0,2000:17.3,4000:6.4},
    50: {500:7.9, 1000:15.7,2000:22.4,4000:8.0},
    55: {500:9.5, 1000:19.0, 2000:25.7, 4000:9.7},
    60: {500:11.3, 1000:21.5, 2000:28.0, 4000:11.2},
    65: {500:12.8, 1000:23.5, 2000:30.2, 4000:13.5},
    70: {500:13.8, 1000:25.5, 2000:32.2, 4000:13.5},
    75: {500:14.6, 1000:27.2, 2000:34.0, 4000:14.2},
    80: {500:14.9, 1000:28.8, 2000:37.5, 4000:14.8},
    85: {500:14.9, 1000:28.8, 2000:37.5, 4000:14.8},
    90: {500:15.0, 1000:29.9, 2000:39.2, 4000:14.9}
}


def lookup(valor, freq):
    """Redondea el umbral al múltiplo de 5 más cercano y devuelve el % de pérdida."""
    ks = sorted(tabla.keys())
    nearest = min(ks, key=lambda x: abs(x - valor))
    return tabla[nearest][freq]


def porc_mono(umbral):
    """Calcula el % de pérdida monaural sumando las frecuencias clave."""
    return sum(lookup(umbral[f], f) for f in (500, 1000, 2000, 4000))


def calcular_pab(od, oi):
    """Calcula el % PAB según Fowler‑Sabine."""
    pm_od = porc_mono(od)
    pm_oi = porc_mono(oi)
    mejor, peor = min(pm_od, pm_oi), max(pm_od, pm_oi)
    return (mejor * 5 + peor) / 6


st.title("Calculadora % PAB (Sabine-Fowler)")
st.write("Ingresa los umbrales tonales (dB) para cada frecuencia:")

with st.form("form"):    
    st.subheader("Oído Derecho")
    od = {f: st.number_input(f" - {f} Hz", 0, 120, key=f"od{f}") for f in (500, 1000, 2000, 4000)}
    st.subheader("Oído Izquierdo")
    oi = {f: st.number_input(f" - {f} Hz", 0, 120, key=f"oi{f}") for f in (500, 1000, 2000, 4000)}
    if st.form_submit_button("Calcular % PAB"):        
        pab = calcular_pab(od, oi)
        st.success(f"**% PAB:** {pab:.1f}%")
