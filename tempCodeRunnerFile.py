import numpy as np
import random
from scipy import signal
from scipy.io import wavfile

# --- CONFIGURACIÓN GLOBAL ---
SR = 44100 

def generar_bajo_electrico(freq, duracion_seg, seccion="VERSO"):
    """
    SÍNTESIS DE BAJO: Ajusta el timbre según la sección.
    En el ESTRIBILLO tiene un poco más de brillo (cuerda).
    """
    if freq <= 0: return np.zeros(int(SR * duracion_seg))
    
    n_muestras = int(SR * duracion_seg)
    t = np.linspace(0, duracion_seg, n_muestras, endpoint=False)
    
    # CUERPO: Fundamental senoidal
    sub = np.sin(2 * np.pi * freq * t)
    
    # TIMBRE: Diente de sierra. Más presente en Estribillo para "cortar" en la mezcla.
    factor_brillo = 0.15 if seccion == "ESTRIBILLO" else 0.08
    cuerda = signal.sawtooth(2 * np.pi * freq * t, 0.5) * factor_brillo
    
    audio = np.tanh((sub + cuerda) * 1.2)
    
    # ENVOLVENTE: Decay más largo en INTRO (notas etéreas), corto en ESTRIBILLO (punch)
    decay_val = 1.5 if seccion in ["INTRO", "FINAL"] else 3.5
    decay = np.exp(-decay_val * t)
    
    return audio * decay

def obtener_frecuencia_bajo(grado, semitonos):
    """
    MAPEO TONAL: Frecuencias base en octavas bajas (C1-C2).
    Sincronizado con las fundamentales del piano/melodía.
    """
    frecuencias_base = {
        'I': 32.70,   'ii': 36.71, 'iii': 41.20, 'IV': 43.65, 
        'V': 49.00,  'vi': 55.00, 'vii': 61.74
    }
    f_raiz = frecuencias_base.get(grado, 32.70) * (2**(semitonos/12))
    return f_raiz

def generar_ritmo_bajo_coordinado(pulsos_totales, seccion, metrica):
    """
    LÓGICA RÍTMICA: Sigue la energía de la melodía.
    """
    ritmo = []
    restante = pulsos_totales
    
    if seccion == "ESTRIBILLO":
        # Ritmo activo: Negras y corcheas (1.0, 0.5)
        opciones = [1.0, 0.5, 0.5] 
    elif seccion == "VERSO":
        # Ritmo estable: Blancas y negras (2.0, 1.0)
        opciones = [2.0, 1.0]
    else: # INTRO / FINAL
        # Notas muy largas
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
    """
    MOTOR PRINCIPAL: Construye el bajo siguiendo la estructura de la canción.
    """
    seg_por_beat = 60 / bpm
    if metrica == "6/8": dur_compas = seg_por_beat * 3
    elif metrica == "2/4": dur_compas = seg_por_beat * 2
    else: dur_compas = seg_por_beat * 4
    
    num_compases = int(np.ceil(duracion_deseada_seg / dur_compas))
    
    if mapa_secciones is None:
        mapa_secciones = ["VERSO"] * num_compases

    # Progresión lógica (debe ser la misma que en la Melodía/Piano)
    progresion = ["I", "V", "vi", "IV"] if modo == "mayor" else ["I", "vi", "iii", "V"]

    pista_final = []
    print(f"> Bajo IA: Sincronizando {num_compases} compases con la melodía...")

    for i in range(num_compases):
        grado_actual = progresion[i % len(progresion)]
        seccion_actual = mapa_secciones[i] if i < len(mapa_secciones) else mapa_secciones[-1]
        
        f_fundamental = obtener_frecuencia_bajo(grado_actual, semitonos)
        esquema_ritmico = generar_ritmo_bajo_coordinado(dur_compas/seg_por_beat, seccion_actual, metrica)
        
        for dur_pulso in esquema_ritmico:
            # El bajo sigue la raíz, pero en el estribillo puede saltar a la quinta (como la melodía)
            f_nota = f_fundamental
            if seccion_actual == "ESTRIBILLO" and random.random() < 0.3:
                f_nota *= 1.5 # Salto a la quinta justa
            
            nota_audio = generar_bajo_electrico(f_nota, dur_pulso * seg_por_beat, seccion_actual)
            pista_final.append(nota_audio)

    audio_final = np.concatenate(pista_final)
    
    # Normalización suave
    if np.max(np.abs(audio_final)) > 0:
        audio_final = (audio_final / np.max(np.abs(audio_final))) * 0.7
        
    return audio_final

# --- EJECUCIÓN INDEPENDIENTE (TEST) ---
if __name__ == "__main__":
    # Valores de prueba para generar solo el bajo
    bpm_test = 120
    shift_test = 0
    modo_test = "mayor"
    metrica_test = "4/4"
    duracion_test = 16 
    mapa_test = ["INTRO", "VERSO", "VERSO", "ESTRIBILLO"] # El bajo cambiará en cada una
    
    print("Iniciando generación de Bajo Independiente...")
    bajo_solo = generar_pista_bajo_completa(bpm_test, shift_test, modo_test, metrica_test, duracion_test, mapa_test)
    
    nombre_archivo = "Bajo_Evolutivo_Independiente.wav"
    wavfile.write(nombre_archivo, SR, (bajo_solo * 32767).astype(np.int16))
    print(f"¡Éxito! Archivo '{nombre_archivo}' generado correctamente.")