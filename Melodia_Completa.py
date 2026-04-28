import numpy as np
import random
from scipy.io import wavfile
import Exportador_MIDI

# --- CONFIGURACIÓN GLOBAL ---
SR = 44100 

def generar_onda_nota(freq, duracion_seg,intensidad=0.30):
    """
    SÍNTESIS ADITIVA + ADSR:
    Mantiene tu estructura de armónicos y decaimiento exponencial.
    """
    if freq <= 0: return np.zeros(int(SR * duracion_seg))
    
    t = np.linspace(0, duracion_seg, int(SR * duracion_seg), endpoint=False)
    
    # Timbre: Fundamental + 3 armónicos
    onda = (1.0 * np.sin(2 * np.pi * freq * t) + 
            0.5 * np.sin(2 * np.pi * freq * 2 * t) + 
            0.2 * np.sin(2 * np.pi * freq * 3 * t) +
            0.1 * np.sin(2 * np.pi * freq * 4 * t))

    # Envolvente: Decay para simular pulsación
    decay = np.exp(-3.5 * t) 
    ataque_muestras = int(SR * 0.01)
    fade_in = np.ones(len(t))
    fade_in[:ataque_muestras] = np.linspace(0, 1, ataque_muestras) 
    
    return onda * decay * fade_in * 0.30

def calcular_notas_acorde_actual(grado, semitonos_desplazamiento):
    """
    MOTOR TONAL BASADO EN ACORDES:
    Calcula las notas de la tríada (1ª, 3ª, 5ª) basándose en tus frecuencias 
    base y aplicando la escala temperada f = f0 * 2^(n/12).
    """
    # Tus frecuencias base exactas (en Do / 0 semitonos)
    frecuencias_base = {
        'I': 261.63,   # Do (C4)
        'ii': 293.66,  # Re m (D4)
        'IV': 349.23,  # Fa (F4)
        'V': 196.00,   # Sol (G3) - Octava abajo
        'vi': 220.00   # La m (A3)
    }
    
    # 1. Calculamos la Tónica (Raíz) del acorde ajustada a la tonalidad
    f_raiz = frecuencias_base[grado] * (2**(semitonos_desplazamiento/12))
    
    # 2. Definimos si el acorde es menor o mayor para la 3ª nota
    # Según tu esquema: ii y vi son menores, I, IV y V son mayores.
    es_menor = grado in ['ii', 'vi']
    semitonos_tercera = 3 if es_menor else 4
    
    # 3. Construimos la tríada (Escala temperada)
    n1 = f_raiz                         # Tónica
    n2 = f_raiz * (2**(semitonos_tercera/12)) # Tercera (Mayor o Menor)
    n3 = f_raiz * (2**(7/12))           # Quinta Justa
    
    # Retornamos el set de notas en 2 octavas para dar variedad a la melodía
    return [n1, n2, n3, n1*2, n2*2, n3*2]

def generar_ritmo_compas(pulsos_totales, seccion, metrica):
    """ 
    MOTOR RÍTMICO: Ajuste preciso para métricas binarias y ternarias.
    """
    ritmo = []
    restante = pulsos_totales
    
    # Definición de figuras según el tipo de métrica
    if metrica in ["6/8", "3/4"]:
        # En 3/4 o 6/8, los pulsos se dividen en tercios o mitades de 3
        figuras = [1.0, 0.5, 1.5] # Negra, Corchea, Negra con punto
    else:
        figuras = [1.0, 0.5, 0.25] # Negra, Corchea, Semicorchea

    # Aumento de actividad en el Estribillo (notas más cortas)
    if seccion == "ESTRIBILLO":
        figuras = [0.5, 0.25] if metrica not in ["6/8", "3/4"] else [0.5, 0.75]

    while restante > 0.05:
        figura = random.choice(figuras)
        if figura <= restante:
            ritmo.append(figura)
            restante -= figura
        else:
            ritmo.append(restante)
            restante = 0
    return ritmo

def crear_compas_melodico(grado, bpm, semitonos, seccion, metrica):
    """
    Une el ritmo con las notas del acorde, aplicando lógica de SECCIÓN.
    """
    seg_por_beat = 60 / bpm
    
    # Determinamos pulsos por compás para el ritmo
    if metrica == "6/8" or metrica == "3/4": pulsos_compas = 3.0
    elif metrica == "2/4": pulsos_compas = 2.0
    else: pulsos_compas = 4.0

    notas_disponibles = calcular_notas_acorde_actual(grado, semitonos)
    
    # --- LÓGICA DE SECCIÓN ---
    if seccion == "ESTRIBILLO":
        # Usamos las notas más agudas del array (índices altos) y más volumen
        notas_finales = notas_disponibles[3:] 
        prob_silencio = 0.05
        vol = 0.40
    elif seccion == "VERSO":
        # Notas medias y más silencios
        notas_finales = notas_disponibles[1:5]
        prob_silencio = 0.25
        vol = 0.25
    else: # INTRO / FINAL
        # Notas graves y etéreas
        notas_finales = notas_disponibles[:3]
        prob_silencio = 0.40
        vol = 0.15

    esquema_ritmico = generar_ritmo_compas(pulsos_compas, seccion, metrica)
    
    audio_compas = []
    for duracion_pulso in esquema_ritmico:
        f = random.choice(notas_finales)
        if random.random() < prob_silencio: f = 0 
        
        duracion_seg = duracion_pulso * seg_por_beat
        audio_compas.append(generar_onda_nota(f, duracion_seg, intensidad=vol))
    
    return np.concatenate(audio_compas)

def generar_melodia_completa(progresion, bpm, semitonos, metrica, duracion_deseada_seg, mapa_secciones=None):
    seg_por_beat = 60 / bpm
    
    if metrica in ["6/8", "3/4"]:
        pulsos_compas = 3.0
    elif metrica == "2/4":
        pulsos_compas = 2.0
    else:
        pulsos_compas = 4.0

    dur_compas = seg_por_beat * pulsos_compas

    if mapa_secciones is None:
        num_compases = int(np.ceil(duracion_deseada_seg / dur_compas))
        mapa_secciones = ['VERSO'] * num_compases
    else:
        num_compases = len(mapa_secciones)

    print(f"> Melodía IA: Componiendo {num_compases} compases con dinámica de sección...")
    
    melodia_final = []
    eventos_midi = []

    for i in range(num_compases):
        grado = progresion[i % len(progresion)]
        seccion = mapa_secciones[i]
        notas_finales = calcular_notas_acorde_actual(grado, semitonos)
        esquema_ritmico = generar_ritmo_compas(pulsos_compas, seccion, metrica)
        
        tiempo_acumulado = i * pulsos_compas
        for dur_pulso in esquema_ritmico:
            f = random.choice(notas_finales) if random.random() > 0.2 else 0
            melodia_final.append(generar_onda_nota(f, dur_pulso * seg_por_beat))
            if f > 0:
                eventos_midi.append((Exportador_MIDI.hz_a_midi(f), tiempo_acumulado, dur_pulso))
            tiempo_acumulado += dur_pulso

    return np.concatenate(melodia_final), eventos_midi

# --- EJECUCIÓN ---

if __name__ == "__main__":
    mapa_ejemplo = ["VERSO", "VERSO", "ESTRIBILLO", "ESTRIBILLO"]
    audio, midi_data = generar_melodia_completa(["I", "V", "vi", "IV"], 120, 0, "4/4", 15, mapa_ejemplo)
    
    if np.max(np.abs(audio)) > 0:
        audio /= np.max(np.abs(audio))
    wavfile.write("Melodia_Evolutiva_Test.wav", SR, (audio * 32767).astype(np.int16))
    Exportador_MIDI.guardar_midi(midi_data, 120, "Melodia_Solo")