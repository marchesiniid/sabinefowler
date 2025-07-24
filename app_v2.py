import streamlit as st

# Tabla Fowler‑Sabine (ANSI 1971): umbral dB → % pérdida por freq
tabla = {
    10: {500:0.2,1000:0.3,2000:0.4,4000:0.1},
    15: {500:0.5,1000:0.9,2000:1.3,4000:0.3},
    20: {500:1.1,1000:2.1,2000:2.9,4000:0.9},
    25: {500:1.8,1000:3.6,2000:4.9,4000:1.7},
    30: {500:3.6,1000:5.4,2000:7.3,4000:2.7},
    35: {500:3.7,1000:7.7,2000:9.8,4000:3.8},
    40: {500:4.9,1000:10.2,2000:12.9,4000:5.0},
    45: {500:6.3,1000:13.0,2000:17.3,4000:6.4},
    50: {500:7.9,1000:15.7,2000:22.4,4000:8.0},
    55: {500:9.5,1000:19.0,2000:25.7,4000:9.7},
    60: {500:11.3,1000:21.5,2000:28.0,4000:11.2},
    65: {500:12.8,1000:23.5,2000:30.2,4000:13.5},
    70: {500:13.8,1000:25.5,2000:32.2,4000:13.5},
    75: {500:14.6,1000:27.2,2000:34.0,4000:14.2},
    80: {500:14.9,1000:28.8,2000:37.5,4000:14.8},
    85: {500:14.9,1000:28.8,2000:37.5,4000:14.8},
    90: {500:15.0,1000:29.9,2000:39.2,4000:14.9},
}

def lookup(umbral, freq):
    claves = sorted(tabla.keys())
    cercano = min(claves, key=lambda k: abs(k-umbral))
    return tabla[cercano][freq]

def porc_mono(umbral_dict):
    return sum(lookup(umbral_dict[f], f) for f in (500,1000,2000,4000))

def clasificar(pt_prom):
    if pt_prom <= 25: return "Normal"
    if pt_prom <= 40: return "Leve"
    if pt_prom <= 55: return "Moderada"
    if pt_prom <= 70: return "Mod‑Severa"
    if pt_prom <= 90: return "Severa"
    return "Profunda"

st.title("Calculadora Audiometría Tonal (Med. Laboral)")

with st.form("form"):
    incluir6k = st.checkbox("Incluir 6000 Hz para HFA y asimetría", value=False)
    st.write("Ingresá los umbrales en dB:")
    cols = st.columns(2)
    with cols[0]:
        st.subheader("Oído Derecho")
        od = {
            f: st.number_input(f"{f} Hz", 0, 120, key=f"od{f}") for f in (500,1000,2000,4000)}
        if incluir6k:
            od[6000] = st.number_input("6000 Hz", 0, 120, key="od6000")
        
    with cols[1]:
        st.subheader("Oído Izquierdo")
        oi = {
            f: st.number_input(f"{f} Hz", 0, 120, key=f"oi{f}") for f in (500,1000,2000,4000)}
        if incluir6k:
            oi[6000] = st.number_input("6000 Hz", 0, 120, key="oi6000")

    if st.form_submit_button("Calcular"):
        # cálculos básicos
        suma_od    = sum(od.values())
        perdida_od = suma_od/4
        pm_od      = porc_mono(od)
        to_od      = pm_od*0.42
        pt_od      = (od[500]+od[1000]+od[2000])/3
        if incluir6k:
            hfa_od = (od[2000]+od[4000]+od[6000])/3

        suma_oi    = sum(oi.values())
        perdida_oi = suma_oi/4
        pm_oi      = porc_mono(oi)
        to_oi      = pm_oi*0.42
        pt_oi      = (oi[500]+oi[1000]+oi[2000])/3
        if incluir6k:
            hfa_oi = (oi[2000]+oi[4000]+oi[6000])/3

        # asimetría sólo sobre las freq disponibles
        freqs = (500,1000,2000,4000) + ((6000,) if incluir6k else ())
        asim = any(abs(od.get(f,0)-oi.get(f,0))>15 for f in freqs)
        obs_asim = "Sí" if asim else "No"

        # diagnóstico por oído
        diag_od = clasificar(perdida_od) + (" + Asimetría" if asim else "")
        diag_oi = clasificar(perdida_oi) + (" + Asimetría" if asim else "")

        # diagnóstico global
        peor = max(perdida_od, perdida_oi)
        diag_glob = f"Peor oído: {clasificar(peor)}" + ("; Asimetría" if asim else "")

        # — Subtítulos coloreados sólo aquí —
        st.markdown("### <span style='color:red'>Oído Derecho</span>", unsafe_allow_html=True)
        st.write(f"Suma de Umbrales: {suma_od}")
        st.write(f"Pérdida en dB: {perdida_od:.1f}")
        st.write(f"% PAB: {pm_od:.1f}%")
        st.write(f"T.O.: {to_od:.1f}")
        st.write(f"PTT - Promedio Tonos Puros  (500‑1k‑2k): {pt_od:.1f} dB")
        if incluir6k:
            st.write(f"HFA - Promedio Altas frecuencias (2k‑4k‑6k): {hfa_od:.1f} dB")
        st.write(f"Asimetría interaural: {obs_asim}")
        st.write(f"Diagnóstico sugerido: {diag_od}")

        st.markdown("### <span style='color:blue'>Oído Izquierdo</span>", unsafe_allow_html=True)
        st.write(f"Suma de Umbrales: {suma_oi}")
        st.write(f"Pérdida en dB: {perdida_oi:.1f}")
        st.write(f"% PAB: {pm_oi:.1f}%")
        st.write(f"T.O.: {to_oi:.1f}")
        st.write(f"PTT - Promedio Tonos Puros (500‑1k‑2k): {pt_oi:.1f} dB")
        if incluir6k:
            st.write(f"HFA - Promedio Altas Frecuencias (2k‑4k‑6k): {hfa_oi:.1f} dB")
        st.write(f"Asimetría interaural: {obs_asim}")
        st.write(f"Diagnóstico sugerido: {diag_oi}")

        st.markdown("## Diagnóstico Global")
        st.write(f"Asimetría interaural: {obs_asim}")
        st.write(diag_glob)
