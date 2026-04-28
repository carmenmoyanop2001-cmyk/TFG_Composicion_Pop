import numpy as np
from scipy import signal
from scipy.io import wavfile

# --- CONFIGURACIÓN ---
SR = 44100

def generar_caja_con_cuerpo():
    """
    SÍNTESIS DE CAJA: 
    Mantiene tu lógica de Punch + Bordón + Reverb.
    """
    duracion_nota = 0.8 
    t = np.linspace(0, duracion_nota, int(SR * duracion_nota), False)
    
    # 1. EL "PUNCH" (Ataque del parche)
    f_inicio, f_fin = 210, 140
    freq_sweep = np.linspace(f_inicio, f_fin, len(t))
    fase = 2 * np.pi * np.cumsum(freq_sweep) / SR
    cuerpo = (np.sin(fase) + 0.3 * np.sin(2 * fase)) * np.exp(-25 * t)
    
    # 2. EL BORDÓN (Textura de la caja)
    ruido_base = np.random.uniform(-1, 1, len(t))
    sos_bordon = signal.butter(4, [600, 5000], 'bandpass', fs=SR, output='sos')
    bordon = signal.sosfilt(sos_bordon, ruido_base)
    bordon_final = bordon * np.exp(-10 * t) * 0.4
    
    # 3. REVERB DE SALA
    cola_ruido = np.random.uniform(-1, 1, len(t))
    sos_reverb = signal.butter(2, 1200, 'low', fs=SR, output='sos')
    reverb = signal.sosfilt(sos_reverb, cola_ruido)
    reverb_final = reverb * np.exp(-8 * t) * 0.2
    
    # 4. SUMA Y PROCESADO
    snare = np.tanh((cuerpo + bordon_final + reverb_final) * 2.0) 
    return snare

def generar_pista_caja_completa(bpm, metrica, duracion_deseada_seg):
    seg_por_beat = 60 / bpm
    
    # --- AJUSTE DE BACKBEAT SEGÚN MÉTRICA ---
    if metrica == "4/4":
        pulsos_por_compas = 4
        pulsos_caja = [1, 3] # Pulsos 2 y 4 (índice 0)
    elif metrica == "2/4":
        pulsos_por_compas = 2
        pulsos_caja = [1]    # Pulso 2
    elif metrica == "3/4":
        pulsos_por_compas = 3
        pulsos_caja = [1, 2] # Pulsos 2 y 3 (típico de pop-vals)
    elif metrica == "6/8":
        pulsos_por_compas = 3 # Un 6/8 se siente como 2 grupos de 3 (negra con punto)
        pulsos_caja = [1.5]  # Pulso 4 (mitad del compás)
    else:
        pulsos_por_compas = 4
        pulsos_caja = [1, 3]

    seg_por_compas = seg_por_beat * pulsos_por_compas
    num_compases = int(np.ceil(duracion_deseada_seg / seg_por_compas))
    muestras_totales = int(num_compases * seg_por_compas * SR)
    
    pista_audio = np.zeros(muestras_totales)
    sonido_caja = generar_caja_con_cuerpo()
    len_caja = len(sonido_caja)
    
    for c in range(num_compases):
        inicio_compas = int(c * seg_por_compas * SR)
        
        for p in pulsos_caja:
            idx_insercion = inicio_compas + int(p * seg_por_beat * SR)
            
            # Verificación de límites del lienzo de audio
            fin_insercion = idx_insercion + len_caja
            if fin_insercion <= muestras_totales:
                pista_audio[idx_insercion : fin_insercion] += sonido_caja

    # Normalización con margen de pico para evitar clipping digital
    if np.max(np.abs(pista_audio)) > 0:
        pista_audio = (pista_audio / np.max(np.abs(pista_audio))) * 0.8
        
    return pista_audio

# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Parámetros de prueba
    bpm_test = 120
    metrica_test = "4/4"
    duracion_test = 15 # segundos
    
    audio_final = generar_pista_caja_completa(bpm_test, metrica_test, duracion_test)
    
    # Guardar resultado
    wavfile.write("Pista_Caja_Sincronizada.wav", SR, (audio_final * 32767).astype(np.int16))
    print(f"Pista de caja de {duracion_test}s generada correctamente.")