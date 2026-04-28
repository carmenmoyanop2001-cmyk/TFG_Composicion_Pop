import numpy as np
from scipy.io import wavfile

# --- CONFIGURACIÓN GLOBAL ---
SR = 44100 

def generar_bombo():
    """
    SÍNTESIS ANALÓGICA DE BOMBO:
    Cuerpo (barrido de frecuencia) + Impacto (ruido filtrado).
    """
    duracion = 0.4  # Un golpe de bombo no necesita 0.5s, con 0.4s es más seco
    t = np.linspace(0, duracion, int(SR * duracion), False)
    
    # 1. CUERPO: Barrido de 150Hz a 40Hz
    # f(t) es la frecuencia instantánea
    f_t = 150 * (40 / 150)**(t / duracion)
    fase = 2 * np.pi * np.cumsum(f_t) / SR
    cuerpo = np.sin(fase) * np.exp(-12 * t) # Caída rápida para que sea "punchy"
    
    # 2. IMPACTO: El "click" del pedal
    ruido = (np.random.random(len(t)) * 2 - 1)
    impacto = ruido * np.exp(-100 * t) * 0.2 
    
    # 3. MEZCLA Y SATURACIÓN
    bombo_final = np.tanh((cuerpo + impacto) * 2.0)
    
    return bombo_final

def generar_pista_percusion(bpm, metrica, duracion_deseada_seg):
    seg_por_beat = 60 / bpm
    
    # --- AJUSTE DE MÉTRICA DINÁMICO ---
    if metrica == "4/4":
        pulsos_por_compas = 4
        puntos_pulso = [0, 2] # Bombo en 1 y 3
    elif metrica == "2/4":
        pulsos_por_compas = 2
        puntos_pulso = [0]    # Bombo en 1
    elif metrica in ["3/4", "6/8"]:
        pulsos_por_compas = 3
        puntos_pulso = [0]    # En 3/4 el bombo suele ir solo al principio (tierra)
    else:
        pulsos_por_compas = 4
        puntos_pulso = [0, 2]

    seg_por_compas = seg_por_beat * pulsos_por_compas
    num_compases = int(np.ceil(duracion_deseada_seg / seg_por_compas))
    muestras_totales = int(num_compases * seg_por_compas * SR)
    
    pista_audio = np.zeros(muestras_totales)
    sonido_bombo = generar_bombo()
    len_bombo = len(sonido_bombo)
    
    for c in range(num_compases):
        inicio_compas = int(c * seg_por_compas * SR)
        
        for p in puntos_pulso:
            idx_insercion = inicio_compas + int(p * seg_por_beat * SR)
            
            # Suma de señales para evitar clipping y permitir capas futuras (hi-hats, caja)
            # Solo insertamos si hay espacio suficiente en el array
            fin_insercion = idx_insercion + len_bombo
            if fin_insercion <= muestras_totales:
                pista_audio[idx_insercion : fin_insercion] += sonido_bombo

    # Normalización con margen de seguridad (Headroom)
    if np.max(np.abs(pista_audio)) > 0:
        pista_audio = (pista_audio / np.max(np.abs(pista_audio))) * 0.85
        
    return pista_audio

if __name__ == "__main__":
    # --- PRUEBA DE SISTEMA ---
    bpm_test = 120
    metrica_test = "4/4"
    duracion_test = 10 # 10 segundos
    
    audio_percusion = generar_pista_percusion(bpm_test, metrica_test, duracion_test)
    
    wavfile.write("Percusion_Sincronizada.wav", SR, (audio_percusion * 32767).astype(np.int16))
    print(f"Pista de percusión generada: {len(audio_percusion)/SR:.2f} segundos.")