import numpy as np
from scipy import signal
from scipy.io import wavfile
from midiutil import MIDIFile 

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


#--- GENERADOR DE COMPÁS INDIVIDUAL ---

def generar_compas_piano(grado, transponer, dur_compas,seccion, metrica):

    "Genera el audio de un único compás adaptándose al momento de la canción"

    notas = obtener_frecuencias_por_grado(grado,transponer)
    audio_compas = np.zeros(int(SR*dur_compas))

    #Definir ganancia e intención según sección
    es_suave = seccion in ['INTRO', 'VERSO', 'FINAL']
    ganancia = 0.2 if es_suave else 0.4

    for i, f in enumerate(notas):
        sonido_nota = generar_piano_nota(f, dur_compas)

        #Efecto de arpegio humano: en los versos las notas no entran exactamente a la vez 
        delay = int(i* 0.02 * SR) if es_suave else 0

        inicio = delay
        fin = min(inicio + len(sonido_nota), len(audio_compas))
        audio_compas[inicio:fin] += sonido_nota[:fin-inicio] * ganancia

    return audio_compas



# --- FUNCIÓN MODIFICADA PARA COMPATIBILIDAD TOTAL ---
# ... (tus funciones de síntesis se mantienen igual) ...

def generar_progresion_inteligente(bpm_usuario, animo, modo_usuario, transponer, duracion_seg, metrica="4/4", mapa_secciones=None):
    animo = animo.lower().strip()
    progresion = PROGRESIONES_MOOD.get(animo, PROGRESIONES_MOOD["alegre"])
    
    seg_por_beat = 60 / bpm_usuario
    
    # --- CÁLCULO DE MÉTRICA ---
    if metrica in ["6/8", "3/4"]:
        pulsos_por_compas = 3
    elif metrica == "2/4":
        pulsos_por_compas = 2
    else:
        pulsos_por_compas = 4
        
    dur_compas = seg_por_beat * pulsos_por_compas 
    num_compases = int(np.ceil(duracion_seg / dur_compas))
    
    if mapa_secciones is None:
        mapa_secciones = ['VERSO'] * num_compases

    muestras_totales = int(num_compases * dur_compas * SR)
    pista_audio = np.zeros(muestras_totales)
    
    # --- NUEVA LISTA PARA EL MIDI ---
    eventos_midi_piano = [] 

    for i in range(num_compases):
        grado = progresion[i % len(progresion)]
        seccion_actual = mapa_secciones[i] if i < len(mapa_secciones) else mapa_secciones[-1]
        
        # Obtenemos las notas (frecuencias) de este compás
        notas_frecuencias = obtener_frecuencias_por_grado(grado, transponer)
        
        # Guardamos para el MIDI: (Lista de frecuencias, pulso de inicio, duración en pulsos)
        eventos_midi_piano.append((notas_frecuencias, i * pulsos_por_compas, pulsos_por_compas))
        
        audio_compas = generar_compas_piano(grado, transponer, dur_compas, seccion_actual, metrica)
        
        inicio_compas = int(i * dur_compas * SR)
        fin = min(inicio_compas + len(audio_compas), muestras_totales)
        pista_audio[inicio_compas:fin] += audio_compas[:fin-inicio_compas]

    # Post-procesado y Normalización (Tu código original)
    sos_l = signal.butter(4, 500, 'lp', fs=SR, output='sos')
    sos_h = signal.butter(4, 4000, 'hp', fs=SR, output='sos')
    pista_audio = signal.sosfilt(sos_l, pista_audio)*1.5 + signal.sosfilt(sos_h, pista_audio)*1.2

    if np.max(np.abs(pista_audio)) > 0:
        pista_audio /= np.max(np.abs(pista_audio))
        
    # DEVOLVEMOS 4 VALORES: audio, bpm, progresion y LOS EVENTOS MIDI
    return pista_audio, bpm_usuario, progresion, eventos_midi_piano

# --- EJECUCIÓN PARA TEST INDEPENDIENTE ---
if __name__ == "__main__":

    import Exportador_MIDI
    audio, bpm, prog, eventos_acordes = generar_progresion_inteligente(120, "alegre", "mayor", 0, 10)
        
    midi_plano = []
    for acorde, inicio, duracion in eventos_acordes:
        for f in acorde:
            midi_plano.append((Exportador_MIDI.hz_a_midi(f), inicio, duracion))
                
    Exportador_MIDI.guardar_midi(midi_plano, bpm, "Piano_Solo")