import numpy as np
from scipy import signal
from scipy.io import wavfile

# --- CONFIGURACIÓN GLOBAL ---
SR = 44100

def generar_hihat_abierto(duracion_nota=0.5):
    """
    SÍNTESIS DE HI-HAT ABIERTO:
    Base de ruido blanco con filtro paso-alto (HP) por encima de 8000Hz.
    """
    t = np.linspace(0, duracion_nota, int(SR * duracion_nota), False)
    
    # 1. GENERAR RUIDO BLANCO (Frecuencias aleatorias)
    ruido = np.random.uniform(-1, 1, len(t))
    
    # 2. FILTRO PASO-ALTO (Brillo metálico)
    # Cortamos todo lo que no sea brillo extremo
    sos = signal.butter(10, 8000, 'hp', fs=SR, output='sos')
    platillo_filtrado = signal.sosfilt(sos, ruido)
    
    # 3. ENVOLVENTE (Decaimiento largo para el 'tssshhh')
    envolvente = np.exp(-5 * t)
    
    # Suavizado inicial para evitar clic digital
    fade_in = int(SR * 0.002)
    envolvente[:fade_in] *= np.linspace(0, 1, fade_in)
    
    return platillo_filtrado * envolvente * 0.3

def generar_pista_hihat_completa(bpm, metrica, duracion_deseada_seg):
    seg_por_beat = 60 / bpm
    
    # --- AJUSTE DE CONTRATIEMPOS SEGÚN MÉTRICA ---
    if metrica == "4/4":
        pulsos_por_compas = 4
        puntos_insercion = [0.5, 1.5, 2.5, 3.5] # El "y" de cada negra
    elif metrica == "2/4":
        pulsos_por_compas = 2
        puntos_insercion = [0.5, 1.5]
    elif metrica == "3/4":
        pulsos_por_compas = 3
        puntos_insercion = [0.5, 1.5, 2.5]      # Contrarios en el pulso 1, 2 y 3
    elif metrica == "6/8":
        pulsos_por_compas = 3                   # Sentido ternario (2 pulsos de negra con punto)
        puntos_insercion = [0.25, 0.75, 1.25, 1.75, 2.25, 2.75] # Síncopas rápidas
    else:
        pulsos_por_compas = 4
        puntos_insercion = [0.5, 1.5, 2.5, 3.5]

    seg_por_compas = seg_por_beat * pulsos_por_compas
    num_compases = int(np.ceil(duracion_deseada_seg / seg_por_compas))
    muestras_totales = int(num_compases * seg_por_compas * SR)
    
    pista_audio = np.zeros(muestras_totales)
    sonido_hh = generar_hihat_abierto(0.5)
    len_hh = len(sonido_hh)
    
    for c in range(num_compases):
        inicio_compas = int(c * seg_por_compas * SR)
        
        for p in puntos_insercion:
            idx = inicio_compas + int(p * seg_por_beat * SR)
            
            # Verificación de límites del array
            if idx + len_hh < muestras_totales:
                pista_audio[idx : idx + len_hh] += sonido_hh

    # Normalización con margen de seguridad para la mezcla final
    if np.max(np.abs(pista_audio)) > 0:
        pista_audio = (pista_audio / np.max(np.abs(pista_audio))) * 0.65
        
    return pista_audio

# ==========================================
# EJECUCIÓN DE PRUEBA
# ==========================================
if __name__ == "__main__":
    # Parámetros configurables
    bpm_test = 120
    metrica_test = "4/4"
    duracion_test = 12  # segundos
    
    audio_final = generar_pista_hihat_completa(bpm_test, metrica_test, duracion_test)
    
    # Guardado
    wavfile.write("Pista_HiHat_Sincronizada.wav", SR, (audio_final * 32767).astype(np.int16))
    print(f"Pista de Hi-Hat de {duracion_test}s generada correctamente.")