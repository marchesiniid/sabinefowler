# app.py
import streamlit as st

# Tabla Fowler‑Sabine (ANSI 1971): umbral dB → % pérdida por freq
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
    55: {500:9.5, 1000:19.0,2000:25.7,4000:9.7},
    60: {500:11.3,1000:21.5,2000:28.0,4000:11.2},
    65: {500:12.8,1000:23.5,2000:30.2,4000:13.5},
    70: {500:13.8,1000:25.5,2000:32.2,4000:13.5},
    75: {500:14.6,1000:27.2,2000:34.0,4000:14.2},
    80: {500:14.9,1000:28.8,2000:37.5,4000:14.8},
    85: {500:14.9,1000:28.8,2000:37.5,4000:14.8},
    90: {500:15.0,1000:29.9,2000:39.2,4000:14.9}
}

def lookup(umbral, freq):
    claves = sorted(tabla.keys())
    cercano = min(claves, key=lambda k: abs(k - umbral))
    return tabla[cercano][freq]

def porc_mono(umbral_dict):
    return sum(lookup(umbral_dict[f], f) for f in (500, 1000, 2000, 4000))

st.title("Calculadora % PAB, T.O. y Suma de Umbrales")
with st.form("form"):
    st.subheader("Oído Derecho")
    od = {f: st.number_input(f"{f} Hz (dB)", 0, 120, key=f"od{f}") for f in (500, 1000, 2000, 4000)}
    st.subheader("Oído Izquierdo")
    oi = {f: st.number_input(f"{f} Hz (dB)", 0, 120, key=f"oi{f}") for f in (500, 1000, 2000, 4000)}
    if st.form_submit_button("Calcular"):
        # Cálculos oído derecho
        suma_od = sum(od.values())
        pm_od = porc_mono(od)
        to_od = pm_od * 0.42
        # Cálculos oído izquierdo
        suma_oi = sum(oi.values())
        pm_oi = porc_mono(oi)
        to_oi = pm_oi * 0.42

        st.write(f"**Oído Derecho**")
        st.write(f"- Suma de Umbrales: {suma_od}")
        st.write(f"- % PAB: {pm_od:.1f}%")
        st.write(f"- T.O.: {to_od:.1f}")

        st.write(f"**Oído Izquierdo**")
        st.write(f"- Suma de Umbrales: {suma_oi}")
        st.write(f"- % PAB: {pm_oi:.1f}%")
        st.write(f"- T.O.: {to_oi:.1f}")
