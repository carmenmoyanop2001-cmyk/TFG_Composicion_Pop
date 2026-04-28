import streamlit as st
import numpy as np
from scipy.io import wavfile
import tempfile
import os

# IMPORTA TU SISTEMA TAL CUAL
import Piano_Acorde_Completa
import Progresión_Batería
import Melodia_Completa
import Bajo_Electrico
import Exportador_MIDI
import Generador_de_Letras
import Mezcla_Piano_Progresion_Batería_Melodía_Bajo_Letra  # <- el archivo donde tienes produccion_final_maestra()

st.set_page_config(page_title="Generador Musical", layout="wide")

st.title("🎵 Sistema Generador de Música Pop")

# -------------------------
# INPUTS
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    bpm = st.number_input("BPM", value=120, min_value=40, max_value=200)

with col2:
    duracion = st.number_input("Duración (segundos)", value=20, min_value=5, max_value=300)

with col3:
    metrica = st.selectbox("Métrica", ["4/4", "2/4", "3/4", "6/8"])

transposicion = st.slider("Transposición", -12, 12, 0)

modo = st.selectbox("Modo", ["mayor", "menor"])

animo = st.selectbox("Ánimo", [
    "alegre", "triste", "nostalgico",
    "decidido", "esperanzador", "tenso"
])

st.markdown("---")

# -------------------------
# INSTRUMENTOS
# -------------------------
st.subheader("Instrumentos")

c1, c2, c3, c4 = st.columns(4)

with c1:
    piano = st.checkbox("Piano", value=True)

with c2:
    bajo = st.checkbox("Bajo", value=True)

with c3:
    bateria = st.checkbox("Batería", value=True)

with c4:
    melodia = st.checkbox("Melodía", value=True)

st.markdown("---")

# -------------------------
# BOTÓN PRINCIPAL
# -------------------------
if st.button("🚀 Generar Canción"):

    with st.spinner("Generando música... esto puede tardar unos segundos"):

        audio, bpm_real, emo, midi, letra = Mezcla_Piano_Progresion_Batería_Melodía_Bajo_Letra.produccion_final_maestra(
            bpm_in=bpm,
            segundos_in=duracion,
            metrica_in=metrica,
            shift_in=transposicion,
            modo_in=modo,
            animo_in=animo,
            usa_bat=bateria,
            usa_baj=bajo,
            usa_pia=piano,
            usa_mel=melodia
        )

        # -------------------------
        # AUDIO OUTPUT
        # -------------------------
        if audio is not None:

            st.success("¡Canción generada!")

            audio_int16 = (audio * 32767).astype(np.int16)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                wavfile.write(tmpfile.name, 44100, audio_int16)

                st.audio(tmpfile.name, format="audio/wav")

            # -------------------------
            # LETRA
            # -------------------------
            st.subheader("📝 Letra generada")

            for linea in letra:
                st.write(linea)

            # -------------------------
            # DESCARGA
            # -------------------------
            st.download_button(
                "Descargar WAV",
                data=open(tmpfile.name, "rb"),
                file_name="cancion_generada.wav"
            )

            with open("temp.mid", "wb") as f:
                midi.writeFile(f)

            st.download_button(
                "Descargar MIDI",
                data=open("temp.mid", "rb"),
                file_name="cancion_generada.mid"
            )

        else:
            st.error("Error generando la canción")
