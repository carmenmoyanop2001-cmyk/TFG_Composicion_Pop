import numpy as np
import random
from scipy import signal
from scipy.io import wavfile
import Exportador_MIDI

# --- CONFIGURACIÓN GLOBAL ---
SR = 44100 

def generar_bajo_electrico(freq, duracion_seg, seccion="VERSO"):
    if freq <= 0: return np.zeros(int(SR * duracion_seg))
    
    n_muestras = int(SR * duracion_seg)
    t = np.linspace(0, duracion_seg, n_muestras, endpoint=False)
    
    sub = np.sin(2 * np.pi * freq * t)
    factor_brillo = 0.15 if seccion == "ESTRIBILLO" else 0.08
    cuerda = signal.sawtooth(2 * np.pi * freq * t, 0.5) * factor_brillo
    
    audio = np.tanh((sub + cuerda) * 1.2)
    
    decay_val = 1.5 if seccion in ["INTRO", "FINAL"] else 3.5
    envolvente = np.exp(-decay_val * t)
    
    ms_suavizado = int(SR * 0.005) 
    puerta_suavizado = np.ones(n_muestras)
    
    puerta_suavizado[:ms_suavizado] = np.linspace(0, 1, ms_suavizado)
    puerta_suavizado[-ms_suavizado:] = np.linspace(1, 0, ms_suavizado)
    
    return audio * envolvente * puerta_suavizado

def obtener_frecuencia_bajo(grado, semitonos):
    frecuencias_base = {
        'I': 32.70,   'ii': 36.71, 'iii': 41.20, 'IV': 43.65, 
        'V': 49.00,  'vi': 55.00, 'vii': 61.74
    }
    f_raiz = frecuencias_base.get(grado, 32.70) * (2**(semitonos/12))
    return f_raiz

def generar_ritmo_bajo_coordinado(pulsos_totales, seccion, metrica):
    ritmo = []
    restante = pulsos_totales
    
    if metrica in ["3/4", "6/8"]:
        if seccion == "ESTRIBILLO":
            opciones = [1.0, 0.5, 0.5]
        elif seccion == "VERSO":
            opciones = [3.0, 1.5, 1.0]
        else:
            opciones = [3.0]
    else:
        if seccion == "ESTRIBILLO":
            opciones = [1.0, 0.5, 0.5] 
        elif seccion == "VERSO":
            opciones = [2.0, 1.0]
        else:
            opciones = [pulsos_totales]

    while restante > 0.01:
        figura = random.choice(opciones)
        if figura <= restante:
            ritmo.append(figura)
            restante -= figura
        else:
            ritmo.append(restante)
            restante = 0
    return ritmo

def generar_pista_bajo_completa(bpm, semitonos, modo, metrica, duracion_deseada_seg, mapa_secciones=None):
    seg_por_beat = 60 / bpm
    
    # Definimos pulsos_compas según métrica para el cálculo MIDI y rítmico
    if metrica in ["6/8", "3/4"]: pulsos_compas = 3.0
    elif metrica == "2/4": pulsos_compas = 2.0
    else: pulsos_compas = 4.0
    
    dur_compas = seg_por_beat * pulsos_compas
    num_compases = int(np.ceil(duracion_deseada_seg / dur_compas))
    
    if mapa_secciones is None:
        mapa_secciones = ["VERSO"] * num_compases

    progresion = ["I", "V", "vi", "IV"] if modo == "mayor" else ["I", "vi", "iii", "V"]

    pista_final = []
    eventos_midi = []
    print(f"> Bajo IA: Sincronizando {num_compases} compases con la melodía...")

    # Corrección de indentación en el bucle principal
    for i in range(num_compases):
        grado_actual = progresion[i % len(progresion)]
        seccion_actual = mapa_secciones[i] if i < len(mapa_secciones) else mapa_secciones[-1]
        f_fundamental = obtener_frecuencia_bajo(grado_actual, semitonos)
        
        # Usamos la variable pulsos_compas recién definida
        esquema_ritmico = generar_ritmo_bajo_coordinado(pulsos_compas, seccion_actual, metrica)
        
        tiempo_acumulado = i * pulsos_compas
        for dur_pulso in esquema_ritmico:
            f_nota = f_fundamental
            if seccion_actual == "ESTRIBILLO" and random.random() < 0.3: 
                f_nota *= 1.5
            
            pista_final.append(generar_bajo_electrico(f_nota, dur_pulso * seg_por_beat, seccion_actual))
            
            nota_midi = Exportador_MIDI.hz_a_midi(f_nota)
            if nota_midi:
                eventos_midi.append((nota_midi, tiempo_acumulado, dur_pulso))
            
            tiempo_acumulado += dur_pulso

    # Corrección de indentación en el retorno de la función
    audio_final = np.concatenate(pista_final)

    if np.max(np.abs(audio_final)) > 0: 
        audio_final = (audio_final / np.max(np.abs(audio_final))) * 0.7
        
    return audio_final, eventos_midi

# --- EJECUCIÓN INDEPENDIENTE (TEST) ---
if __name__ == "__main__":
    bpm_test = 120
    shift_test = 0
    modo_test = "mayor"
    metrica_test = "4/4"
    duracion_test = 16 
    mapa_test = ["INTRO", "VERSO", "VERSO", "ESTRIBILLO"]
    
    print("Iniciando generación de Bajo Independiente...")
    bajo_solo, midi_data = generar_pista_bajo_completa(bpm_test, shift_test, modo_test, metrica_test, duracion_test, mapa_test)
    
    nombre_archivo = "Bajo_Evolutivo_Independiente.wav"
    wavfile.write(nombre_archivo, SR, (bajo_solo * 32767).astype(np.int16))
    Exportador_MIDI.guardar_midi(midi_data, 120, "Bajo_Solo")
    print(f"¡Éxito! Archivo '{nombre_archivo}' generado correctamente.")