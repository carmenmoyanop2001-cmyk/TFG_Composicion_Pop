from midiutil import MIDIFile

def guardar_midi(eventos, bpm, nombre_archivo, es_percusion=False):
    """
    Transforma una lista de eventos en un archivo .mid
    eventos: lista de tuplas (nota_midi, inicio_beat, duracion_beat)
    """
    #1. Crear el objeto MIDI con una sola pista (Track 0)

    midi_obj = MIDIFile(1)
    track = 0
    tiempo_inicial = 0
    # 2. Establecer el Tempo del archivo
    # Esto define la velocidad de reproducción y cómo se interpretan los pulsos (beats)
    midi_obj.addTempo(track, tiempo_inicial, bpm)
    
    # Canal 9 para percusión, Canal 0 para melódicos
    canal = 9 if es_percusion else 0

    # 4. Iterar sobre la lista de eventos musicales
    for nota, inicio, duracion in eventos:
        if nota is not None:
            # addNote(track, canal, pitch, time, duration, volume/velocity)
            # El valor 100 define la 'velocidad' (fuerza del ataque de la nota)
            midi_obj.addNote(track, canal, int(nota), inicio, duracion, 100)

    # 5. Escritura del flujo binario en disco
    with open(f"{nombre_archivo}.mid", "wb") as output_file:
        midi_obj.writeFile(output_file)
    print(f"[MIDI] Generado: {nombre_archivo}.mid")

def hz_a_midi(f):
    """Conversión universal de frecuencia a nota MIDI"""
    import numpy as np
    if f <= 0: return None
    return int(12 * np.log2(f / 440.0) + 69)