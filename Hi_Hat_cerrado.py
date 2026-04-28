import numpy as np
from scipy import signal
from scipy.io import wavfile

# --- CONFIGURACIÓN ---
SR = 44100

def generar_hihat_cerrado_nota(duracion_nota=0.3):
    """
    SÍNTESIS DE HI-HAT CERRADO:
    Mantiene tu lógica de ruido blanco con filtro HP a 2500Hz para tener más cuerpo.
    """
    t = np.linspace(0, duracion_nota, int(SR * duracion_nota), False)
    
    # 1. GENERAR RUIDO BLANCO
    ruido = np.random.uniform(-1, 1, len(t))
    
    # 2. FILTRO PASO-ALTO CON CORTE BAJO (2500Hz según tu petición)
    # Esto le da un sonido menos estridente y con más "madera".
    sos = signal.butter(4, 2500, 'hp', fs=SR, output='sos')
    platillo_filtrado = signal.sosfilt(sos, ruido)
    
    # 3. ENVOLVENTE (Factor -8 para que tenga algo de cola)
    envolvente = np.exp(-8 * t) 
    
    # Evitar clic digital al inicio
    fade_in = int(SR * 0.002)
    envolvente[:fade_in] *= np.linspace(0, 1, fade_in)
    
    resultado = platillo_filtrado * envolvente
    
    if np.max(np.abs(resultado)) > 0:
        resultado /= np.max(np.abs(resultado))
        
    return resultado * 0.4  # Volumen moderado para no tapar la caja

def generar_pista_hihat_cerrado_completa(bpm, metrica, duracion_deseada_seg):
    seg_por_beat = 60 / bpm
    
    # --- AJUSTE DE MÉTRICA DINÁMICO ---
    if metrica == "4/4":
        pulsos_por_compas = 4
    elif metrica == "2/4":
        pulsos_por_compas = 2
    elif metrica in ["3/4", "6/8"]:
        pulsos_por_compas = 3
    else:
        pulsos_por_compas = 4

    seg_por_compas = seg_por_beat * pulsos_por_compas
    num_compases = int(np.ceil(duracion_deseada_seg / seg_por_compas))
    muestras_totales = int(num_compases * seg_por_compas * SR)
    pista_audio = np.zeros(muestras_totales)
    
    # Sonido base más corto (0.15s es ideal para cerrado)
    sonido_hh = generar_hihat_cerrado_nota(0.15)
    len_hh = len(sonido_hh)
    
    for c in range(num_compases):
        inicio_compas = int(c * seg_por_compas * SR)
        
        # En 6/8 las corcheas son la unidad de pulso, en 4/4 son medio pulso
        paso = 0.5
        puntos_insercion = np.arange(0, pulsos_por_compas, paso)
            
        for p in puntos_insercion:
            idx = inicio_compas + int(p * seg_por_beat * SR)
            
            # Verificación de límites del array para evitar errores de índice
            if idx + len_hh < muestras_totales:
                pista_audio[idx : idx + len_hh] += sonido_hh

    # Normalización moderada para el acompañamiento rítmico
    if np.max(np.abs(pista_audio)) > 0:
        pista_audio = (pista_audio / np.max(np.abs(pista_audio))) * 0.5
        
    return pista_audio

# ==========================================
# EJECUCIÓN DE PRUEBA
# ==========================================
if __name__ == "__main__":
    # Parámetros de prueba
    bpm_test = 120
    metrica_test = "4/4"
    duracion_test = 10  # segundos
    
    audio_final = generar_pista_hihat_cerrado_completa(bpm_test, metrica_test, duracion_test)
    
    # Guardado
    wavfile.write("Pista_HH_Cerrado_Sincronizada.wav", SR, (audio_final * 32767).astype(np.int16))
    print(f"Pista de Hi-Hat Cerrado de {duracion_test}s generada.")