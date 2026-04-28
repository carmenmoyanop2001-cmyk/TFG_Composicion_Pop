import numpy as np
import random
from scipy.io import wavfile
import Exportador_MIDI  # Importamos el nuevo script de exportación

# Importamos tus módulos de instrumentos
import Bombo
import Caja_Pop
import Hi_Hat_abierto
import Hi_Hat_cerrado

SR = 44100

def generar_compas_bateria(bpm, metrica, seccion):
    seg_por_beat = 60 / bpm
    
    # 1. AJUSTE DE MÉTRICA Y PASOS
    if metrica in ["6/8", "3/4"]:
        pasos = 12 
        dur_compas = seg_por_beat * 3 
    elif metrica == "2/4":
        pasos = 8
        dur_compas = seg_por_beat * 2
    else: # 4/4
        pasos = 16
        dur_compas = seg_por_beat * 4

    dur_paso = dur_compas / pasos
    audio_compas = np.zeros(int(SR * dur_compas))
    
    # Lista para guardar eventos: (Nota_MIDI, Tiempo_Beat, Duracion)
    eventos_midi_compas = [] 

    # 2. CARGAR SONIDOS
    kick = Bombo.generar_bombo()
    snare = Caja_Pop.generar_caja_con_cuerpo()
    hh_c = Hi_Hat_cerrado.generar_hihat_cerrado_nota(0.1)
    hh_a = Hi_Hat_abierto.generar_hihat_abierto(0.25)

    # 3. PROBABILIDADES SEGÚN SECCIÓN
    prob_kick = 0.9 if seccion == "ESTRIBILLO" else 0.6
    prob_snare = 0.95 if seccion == "ESTRIBILLO" else 0.4
    prob_hh = 0.9 if seccion == "ESTRIBILLO" else 0.6
    
    if seccion in ["INTRO", "FINAL"]:
        prob_kick, prob_snare, prob_hh = 0.3, 0.0, 0.3

    def insertar_seguro(lienzo, sonido, inicio):
        fin_deseado = inicio + len(sonido)
        if fin_deseado > len(lienzo):
            sonido_recortado = sonido[:len(lienzo) - inicio]
            if len(sonido_recortado) > 0:
                lienzo[inicio:] += sonido_recortado
        else:
            lienzo[inicio:fin_deseado] += sonido

    # 4. CONSTRUCCIÓN ALEATORIA DEL COMPÁS
    for i in range(pasos):
        pos = int(i * dur_paso * SR)
        hum = random.uniform(0.85, 1.0) 
        pos_beat = (i * dur_paso) / seg_por_beat
        dur_estandar = 0.1 # Duración corta para disparos de percusión

        # --- LÓGICA DE BOMBO ---
        es_tiempo_fuerte = (i == 0) or (metrica == "4/4" and i == 8) or (metrica == "6/8" and i == 6) or (metrica == "3/4" and i == 0)
        if es_tiempo_fuerte:
            if random.random() < prob_kick:
                insertar_seguro(audio_compas, kick * hum, pos)
                eventos_midi_compas.append((36, pos_beat, dur_estandar)) 

        # --- LÓGICA DE CAJA ---
        es_tiempo_snare = False
        if metrica == "4/4" and i in [4, 12]: es_tiempo_snare = True
        elif metrica == "2/4" and i == 4: es_tiempo_snare = True
        elif metrica == "6/8" and i == 6: es_tiempo_snare = True 
        elif metrica == "3/4" and i in [4, 8]: es_tiempo_snare = True

        if es_tiempo_snare and random.random() < prob_snare:
            insertar_seguro(audio_compas, snare * 0.7 * hum, pos)
            eventos_midi_compas.append((38, pos_beat, dur_estandar))

        # --- LÓGICA DE HI-HAT ---
        if random.random() < prob_hh:
            if seccion == "ESTRIBILLO" and i % 4 == 0 and random.random() > 0.8:
                insertar_seguro(audio_compas, hh_a * 0.2 * hum, pos)
                eventos_midi_compas.append((46, pos_beat, dur_estandar))
            else:
                insertar_seguro(audio_compas, hh_c * 0.3 * hum, pos)
                eventos_midi_compas.append((42, pos_beat, dur_estandar))

    return audio_compas, eventos_midi_compas

def generar_pista_percusion_completa(bpm, metrica, duracion_deseada_seg, mapa_secciones=None):
    seg_por_beat = 60 / bpm
    if metrica in ["6/8", "3/4"]: 
        pulsos_por_compas = 3
    elif metrica == "2/4": 
        pulsos_por_compas = 2
    else: 
        pulsos_por_compas = 4
    
    dur_compas = seg_por_beat * pulsos_por_compas
    num_compases = int(np.ceil(duracion_deseada_seg / dur_compas))
    if mapa_secciones is None: mapa_secciones = ['VERSO'] * num_compases

    muestras_totales = int(num_compases * dur_compas * SR)
    pista_audio = np.zeros(muestras_totales)
    eventos_midi_totales = []

    print(f"\n> Batería IA: Generando {num_compases} compases en {metrica}")

    for c in range(num_compases):
        seccion_actual = mapa_secciones[c] if c < len(mapa_secciones) else mapa_secciones[-1]
        
        compas_audio, midi_compas = generar_compas_bateria(bpm, metrica, seccion_actual)
        
        offset_beat = c * pulsos_por_compas
        for nota, t_beat, dur in midi_compas:
            eventos_midi_totales.append((nota, t_beat + offset_beat, dur))

        inicio_muestras = int(c * dur_compas * SR)
        fin_compas = min(inicio_muestras + len(compas_audio), muestras_totales)
        pista_audio[inicio_muestras:fin_compas] += compas_audio[:fin_compas-inicio_muestras]

    pista_audio = np.tanh(pista_audio * 1.1)
    if np.max(np.abs(pista_audio)) > 0:
        pista_audio = (pista_audio / np.max(np.abs(pista_audio))) * 0.85
        
    return pista_audio, eventos_midi_totales

# --- BLOQUE DE EJECUCIÓN INDEPENDIENTE ---
if __name__ == "__main__":
    bpm_test = 120
    metrica_test = "4/4"
    duracion_test = 12 
    mapa_test = ["INTRO", "VERSO", "ESTRIBILLO", "FINAL"]
    
    audio, midi_data = generar_pista_percusion_completa(bpm_test, metrica_test, duracion_test, mapa_test)
    
    # Exportar Audio
    wavfile.write("Bateria_Solo.wav", SR, (audio * 32767).astype(np.int16))
    
    # Exportar MIDI (usando el canal de percusión)
    Exportador_MIDI.guardar_midi(midi_data, bpm_test, "Bateria_Solo", es_percusion=True)