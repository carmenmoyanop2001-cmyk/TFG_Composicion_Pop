import numpy as np
from scipy.io import wavfile
from midiutil import MIDIFile
import Piano_Acorde_Completa
import Progresión_Batería
import Melodia_Completa
import Bajo_Electrico
import Exportador_MIDI
import Generador_de_Letras  # <--- IMPORTACIÓN DEL NUEVO MÓDULO

SR = 44100

def definir_estructura(bpm, metrica, segundos):
    if bpm <= 0: raise ValueError("BPM inválido")
    seg_por_beat = 60 / bpm
    
    # Determinamos pulsos por compás según métrica
    if metrica in ["6/8", "3/4"]: pulsos_compas = 3
    elif metrica == "2/4": pulsos_compas = 2
    else: pulsos_compas = 4

    dur_compas = seg_por_beat * pulsos_compas
    num_compases = int(np.ceil(segundos / dur_compas))
    mapa = []

    # REGLA 1: Menos de 60 segundos (Verso - Estribillo - Verso)
    if segundos < 60:
        for i in range(num_compases):
            if i < num_compases // 3: mapa.append("VERSO")
            elif i < (2 * num_compases) // 3: mapa.append("ESTRIBILLO")
            else: mapa.append("VERSO")

    # REGLA 2: Entre 60 y 120 segundos (Intro - Verso - Estribillo - Verso - Final)
    elif 60 <= segundos <= 120:
        for i in range(num_compases):
            if i < 2: mapa.append("INTRO")
            elif i < num_compases // 3: mapa.append("VERSO")
            elif i < (2 * num_compases) // 3: mapa.append("ESTRIBILLO")
            elif i < num_compases - 2: mapa.append("VERSO")
            else: mapa.append("FINAL")

    # REGLA 3: Más de 120 segundos (Intro - Verso - Estribillo - Verso - Estribillo - Puente - Estribillo - Final)
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

def produccion_final_maestra(bpm_in=120, segundos_in=20, metrica_in="4/4", 
                             shift_in=0, modo_in="mayor", animo_in="alegre", 
                             usa_bat=True, usa_baj=True, usa_pia=True, usa_mel=True):
    print("\n" + "="*60)
    print("   SISTEMA DE PRODUCCIÓN: MEZCLA Y EXPORTACIÓN MIDI")
    print("="*60)
    
    # 1. ENTRADA DE DATOS
    try:
        bpm_in = int(input("1. Tempo (BPM) [120]: ") or 120)
        segundos_in = int(input("2. Duración (segundos) [20]: ") or 20)
        metrica_in = input("3. Métrica (4/4, 2/4, 6/8, 3/4) [4/4]: ").strip() or "4/4"
        shift_in = int(input("4. Transposición (0=Do) [0]: ") or 0)
        modo_in = input("5. ¿Modo Mayor o Menor? [mayor]: ").lower().strip() or "mayor"
        animo_in = input("6. ¿Ánimo? [alegre]: ").lower() or "alegre"

        print("\n--- Selección de Instrumentos (s/n) ---")
        usa_bat = input("¿Batería? [s]: ").lower() != 'n'
        usa_baj = input("¿Bajo? [s]: ").lower() != 'n'
        usa_pia = input("¿Piano? [s]: ").lower() != 'n'
        usa_mel = input("¿Melodía? [s]: ").lower() != 'n'
    except:
        bpm_in, segundos_in, metrica_in, shift_in, modo_in, animo_in = 120, 20, "4/4", 0, "mayor", "alegre"
        usa_bat = usa_baj = usa_pia = usa_mel = True

    mapa_secciones, pulsos_p_compas, num_compases = definir_estructura(bpm_in, metrica_in, segundos_in)
    largo_objetivo = int(segundos_in * SR)

    # --- GENERACIÓN DE LETRA (Sincronizada con la duración) ---
    # Llamamos al generador usando el mapa de secciones real y el ánimo
    letra_final = Generador_de_Letras.generar_letra_completa(mapa_secciones, animo_in)

    midi_maestro = MIDIFile(4)
    for i in range(4): midi_maestro.addTempo(i, 0, bpm_in)

    def forzar_largo(audio, largo):
        if len(audio) >= largo: return audio[:largo]
        return np.pad(audio, (0, max(0, largo - len(audio))), 'constant')

    try:
        print(f"\n[Procesando {num_compases} compases...]")

        # 2. GENERACIÓN DE CAPAS Y DATOS MIDI
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
            
            # --- LÓGICA CORREGIDA PARA SYNTHESIZER V ---
            pulsos_totales = num_compases * pulsos_p_compas
            # Evitamos división por cero si la letra fallara
            pulsos_por_frase = pulsos_totales / len(letra_final) if letra_final else 1

            # 1. Añadimos las Notas
            for n_mel, inicio, dur in midi_m:
                if n_mel: 
                    midi_maestro.addNote(2, 0, n_mel, inicio, dur, 75)

            # 2. Añadimos la Letra (Usando addText con tipo 5)
            for i, linea in enumerate(letra_final):
                # Limpiamos el texto: [VERSO] Hola -> Hola
                texto_canto = linea.split("] ")[1] if "] " in linea else linea
                tiempo_lyric = i * pulsos_por_frase
                
                # addText(track, time, text) -> Por defecto añade Text Event
                # Para Synthesizer V, esto suele ser suficiente para que lo reconozca
                midi_maestro.addText(2, tiempo_lyric, texto_canto)
            # -------------------------------------------
        else: 
            m_raw = np.zeros(largo_objetivo)

        # 3. ALINEACIÓN Y MEZCLA
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

        # DEVOLVEMOS TAMBIÉN LA LETRA
        return final_audio, bpm_real, animo_in, midi_maestro, letra_final

    except Exception as e:
        print(f"\n[ERROR]: {e}")
        return None, None, None, None, None

if __name__ == "__main__":
    # Recogemos el nuevo parámetro letra_final
    resultado, bpm, emo, midi_final, letra_cancion = produccion_final_maestra()
    
    if resultado is not None:
        base_name = f"Resultado_{emo}_{bpm}BPM"
        
        wavfile.write(f"{base_name}.wav", SR, (resultado * 32767).astype(np.int16))
        
        with open(f"{base_name}.mid", "wb") as f_mid:
            midi_final.writeFile(f_mid)
        
        # --- GUARDAR LETRA EN ARCHIVO DE TEXTO ---
        with open(f"{base_name}_LETRA.txt", "w", encoding="utf-8") as f_txt:
            f_txt.write(f"LETRA GENERADA - MOOD: {emo.upper()}\n")
            f_txt.write("="*30 + "\n")
            for linea in letra_cancion:
                f_txt.write(linea + "\n")

        print("\n" + "="*60)
        print(f" ÉXITO: Generados '{base_name}.wav', '.mid' y '_LETRA.txt'")
        print("="*60)
