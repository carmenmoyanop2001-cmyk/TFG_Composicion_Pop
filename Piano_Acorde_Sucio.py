import numpy as np
from scipy import signal
from scipy.io import wavfile

# --- CONFIGURACIÓN ---
SR = 44100

# 1. DICCIONARIO DE FRECUENCIAS BASE (Tonalidad Do)
FREQS_BASE = {
    'I': 261.63,   # Do
    'ii': 293.66,  # Re m
    'IV': 349.23,  # Fa
    'V': 196.00,   # Sol (octava abajo)
    'vi': 220.00   # La m
}

# 2. DICCIONARIO DE PROGRESIONES: Todas resuelven en I
PROGRESIONES_MOOD = {
    "alegre": ["I", "V", "vi", "IV", "I"],
    "triste": ["vi", "IV", "I", "V", "I"],
    "nostalgico": ["I", "vi", "IV", "V", "I"],
    "decidido": ["ii", "V", "I", "IV", "I"],
    "esperanzador": ["I", "IV", "V", "IV", "I"],
    "tenso": ["ii", "V", "vi", "ii", "I"]
}

def obtener_frecuencias_por_grado(grado, transpo_semitonos):
    f_raiz = FREQS_BASE[grado] * (2 ** (transpo_semitonos / 12))
    es_menor = grado in ['ii', 'vi']
    tercera = f_raiz * (2 ** (3/12)) if es_menor else f_raiz * (2 ** (4/12))
    quinta = f_raiz * (2 ** (7/12))
    return [f_raiz, tercera, quinta]

def generar_piano_nota(freq, duracion):
    if freq <= 0: return np.zeros(int(SR * duracion))
    t = np.linspace(0, duracion, int(SR * duracion), False)
    cuerpo = (1.0 * np.sin(2 * np.pi * freq * t) +
              0.6 * np.sin(2 * np.pi * 2 * freq * t) +
              0.3 * np.sin(2 * np.pi * 3 * freq * t) +
              0.1 * np.sin(2 * np.pi * 4 * freq * t))
    envolvente = np.exp(-2.5 * t)
    ataque = (np.random.uniform(-1, 1, len(t))) * np.exp(-100 * t) * 0.1
    return (cuerpo + ataque) * envolvente

# --- FUNCIÓN MODIFICADA PARA COMPATIBILIDAD TOTAL ---
def generar_progresion_inteligente(bpm_usuario, animo, modo_usuario, transponer, duracion_seg):
    """
    Argumentos sincronizados con el script de Mezcla Final.
    Selecciona UNA progresión y la repite hasta el final.
    """
    animo = animo.lower().strip()
    # Buscamos la progresión en el diccionario; si no existe, usamos la 'alegre'
    progresion = PROGRESIONES_MOOD.get(animo, PROGRESIONES_MOOD["alegre"])
    
    seg_por_beat = 60 / bpm_usuario
    # Forzamos métrica 4/4 para el acompañamiento de piano estándar
    dur_compas = seg_por_beat * 4 
    
    num_compases = int(np.ceil(duracion_seg / dur_compas))
    muestras_totales = int(num_compases * dur_compas * SR)
    pista_audio = np.zeros(muestras_totales)

    print(f"\n> Piano IA: Mood '{animo.upper()}' -> Progresión: {progresion}")

    for i in range(num_compases):
        # Repetición circular de la lista que termina en I
        grado = progresion[i % len(progresion)]
        notas = obtener_frecuencias_por_grado(grado, transponer)
        
        inicio_compas = int(i * dur_compas * SR)
        
        for f in notas:
            sonido_nota = generar_piano_nota(f, dur_compas)

            fin = inicio_compas + len(sonido_nota)

            pista_audio[inicio_compas:fin] += sonido_nota * 0.25

        if fin > len(pista_audio):
            sonido_nota = sonido_nota[:len(pista_audio) - inicio_compas]
            fin = len(pista_audio)

        pista_audio[inicio_compas:fin] += sonido_nota * 0.25


    # Post-procesado (Filtros EQ)
    sos_l = signal.butter(4, 500, 'lp', fs=SR, output='sos')
    sos_h = signal.butter(4, 4000, 'hp', fs=SR, output='sos')
    pista_audio = signal.sosfilt(sos_l, pista_audio)*1.5 + signal.sosfilt(sos_h, pista_audio)*1.2

    # Normalización final
    if np.max(np.abs(pista_audio)) > 0:
        pista_audio /= np.max(np.abs(pista_audio))
        
    # Devolvemos audio, bpm y progresión (exactamente lo que pide la producción final)
    return pista_audio, bpm_usuario, progresion

# --- EJECUCIÓN PARA TEST INDEPENDIENTE ---
if __name__ == "__main__":
    print("Test de Piano independiente")
    mood_user = input("Ánimo (alegre, triste, nostalgico, decidido, esperanzador, tenso): ")
    
    audio, bpm, prog_usada = generar_progresion_inteligente(
        bpm_usuario=120, 
        animo=mood_user, 
        modo_usuario="mayor", 
        transponer=0, 
        duracion_seg=10
    )
    
    nombre_salida = f"Piano_Test_{mood_user}.wav"
    wavfile.write(nombre_salida, SR, (audio * 32767).astype(np.int16))
    print(f"Archivo '{nombre_salida}' generado. Finaliza en: {prog_usada[-1]}")