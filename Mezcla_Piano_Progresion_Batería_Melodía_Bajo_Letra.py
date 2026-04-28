import numpy as np
from scipy.io import wavfile
from midiutil import MIDIFile
import Piano_Acorde_Completa
import Progresión_Batería
import Melodia_Completa
import Bajo_Electrico
import Exportador_MIDI
import Generador_de_Letras

SR = 44100

def definir_estructura(bpm, metrica, segundos):
    if bpm <= 0: raise ValueError("BPM inválido")
    seg_por_beat = 60 / bpm
    
    if metrica in ["6/8", "3/4"]: pulsos_compas = 3
    elif metrica == "2/4": pulsos_compas = 2
    else: pulsos_compas = 4

    dur_compas = seg_por_beat * pulsos_compas
    num_compases = int(np.ceil(segundos / dur_compas))
    mapa = []

    if segundos < 60:
        for i in range(num_compases):
            if i < num_compases // 3: mapa.append("VERSO")
            elif i < (2 * num_compases) // 3: mapa.append("ESTRIBILLO")
            else: mapa.append("VERSO")
    elif 60 <= segundos <= 120:
        for i in range(num_compases):
            if i < 2: mapa.append("INTRO")
            elif i < num_compases // 3: mapa.append("VERSO")
            elif i < (2 * num_compases) // 3: mapa.append("ESTRIBILLO")
            elif i < num_compases - 2: mapa.append("VERSO")
            else: mapa.append("FINAL")
    else:
        for i in range(num_compases):
            if i < 2: mapa.append("INTRO")
            elif i < num_compases // 6: mapa.append("VERSO")
            elif i < 2 * (num_compases // 6): mapa.append("ESTRIBILLO")
            elif i < 3 * (num_compases // 6): mapa.append("VERSO")
            elif i < 4 * (num_compases // 6): mapa.append("ESTRIBILLO")
            elif i < 5 * (num_compases // 6): mapa.append("PUENTE")
            elif i < num_compases - 2: mapa.append("ESTRIBILLO")
            else: mapa.append("FINAL")

    return mapa, pulsos_compas, num_compases

# --- LA FUNCIÓN AHORA RECIBE LOS DATOS DE STREAMLIT ---
def produccion_final_maestra(bpm_in=120, segundos_in=20, metrica_in="4/4", 
                             shift_in=0, modo_in="mayor", animo_in="alegre", 
                             usa_bat=True, usa_baj=True, usa_pia=True, usa_mel=True):
    
    # IMPORTANTE: Eliminamos los input() para que Streamlit pueda enviar sus variables
    print(f"\nGenerando: {bpm_in} BPM, {segundos_in}s, Modo {modo_in}, Ánimo {animo_in}")

    mapa_secciones, pulsos_p_compas, num_compases = definir_estructura(bpm_in, metrica_in, segundos_in)
    largo_objetivo = int(segundos_in * SR)

    letra_final = Generador_de_Letras.generar_letra_completa(mapa_secciones, animo_in)

    midi_maestro = MIDIFile(4)
    for i in range(4): midi_maestro.addTempo(i, 0, bpm_in)

    def forzar_largo(audio, largo):
        if len(audio) >= largo: return audio[:largo]
        return np.pad(audio, (0, max(0, largo - len(audio))), 'constant')

    try:
        # 2. GENERACIÓN DE CAPAS
        p_raw, bpm_real, prog_elegida, midi_p = Piano_Acorde_Completa.generar_progresion_inteligente(
            bpm_in, animo_in, modo_in, shift_in, segundos_in, metrica_in, mapa_secciones
        )
        
        if usa_pia:
            for acorde, inicio, dur in midi_p:
                for f in acorde:
                    n = Exportador_MIDI.hz_a_midi(f)
                    if n: midi_maestro.addNote(0, 0, n, inicio, dur, 60)
        else: p_raw = np.zeros(largo_objetivo)

        if usa_bat:
            b_raw, midi_b = Progresión_Batería.generar_pista_percusion_completa(
                bpm_real, metrica_in, segundos_in, mapa_secciones
            )
            for n_bat, inicio, dur in midi_b:
                midi_maestro.addNote(3, 9, n_bat, inicio, dur, 90)
        else: b_raw = np.zeros(largo_objetivo)
        
        if usa_baj:
            ba_raw, midi_ba = Bajo_Electrico.generar_pista_bajo_completa(
                bpm_real, shift_in, modo_in, metrica_in, segundos_in, mapa_secciones
            )
            for n_baj, inicio, dur in midi_ba:
                if n_baj: midi_maestro.addNote(1, 0, n_baj, inicio, dur, 80)
        else: ba_raw = np.zeros(largo_objetivo)
        
        if usa_mel:
            m_raw, midi_m = Melodia_Completa.generar_melodia_completa(
                prog_elegida, bpm_real, shift_in, metrica_in, segundos_in, mapa_secciones
            )
            
            pulsos_totales = num_compases * pulsos_p_compas
            pulsos_por_frase = pulsos_totales / len(letra_final) if letra_final else 1

            for n_mel, inicio, dur in midi_m:
                if n_mel: midi_maestro.addNote(2, 0, n_mel, inicio, dur, 75)

            for i, linea in enumerate(letra_final):
                texto_canto = linea.split("] ")[1] if "] " in linea else linea
                tiempo_lyric = i * pulsos_por_frase
                midi_maestro.addText(2, tiempo_lyric, texto_canto)
        else: 
            m_raw = np.zeros(largo_objetivo)

        # 3. MEZCLA
        mezcla = (forzar_largo(m_raw, largo_objetivo) * 0.45) + \
                 (forzar_largo(b_raw, largo_objetivo) * 0.35) + \
                 (forzar_largo(p_raw, largo_objetivo) * 0.25) + \
                 (forzar_largo(ba_raw, largo_objetivo) * 0.40)

        fade_samples = int(SR * 3)
        if len(mezcla) > fade_samples:
            mezcla[-fade_samples:] *= np.linspace(1.0, 0.0, fade_samples)

        final_audio = np.tanh(mezcla * 1.1)
        max_val = np.max(np.abs(final_audio))
        if max_val > 0: final_audio = (final_audio / max_val) * 0.9

        return final_audio, bpm_real, animo_in, midi_maestro, letra_final

    except Exception as e:
        print(f"\n[ERROR]: {e}")
        return None, None, None, None, None

# El bloque if __name__ == "__main__" queda solo para tus pruebas locales en PC
if __name__ == "__main__":
    # Aquí puedes dejar inputs si quieres probarlo a mano en VS Code
    print("Iniciando prueba local...")
    resultado, bpm, emo, midi_final, letra_cancion = produccion_final_maestra()
    
