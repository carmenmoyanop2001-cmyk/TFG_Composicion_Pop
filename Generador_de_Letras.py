
import random

# Estructura: (Palabra, Tónica, Género [0:M, 1:F], Número [0:S, 1:P])
biblioteca_lexica = {
    "alegre": {
        "sustantivos": [
            ("sol", 0, 0, 0), ("fiesta", 1, 1, 0), ("camino", 1, 0, 0), ("luz", 0, 1, 0), 
            ("disco", 1, 0, 0), ("noche", 1, 1, 0), ("día", 0, 0, 0), ("control", 0, 0, 0), 
            ("ojos", 1, 0, 1), ("error", 0, 0, 0), ("nombre", 1, 0, 0), ("libertad", 0, 1, 0), ("amor", 0, 0, 0)
        ],
        "verbos": [
            ("brillar", 1, None, None), ("cantar", 1, None, None), ("sentir", 1, None, None), 
            ("sonreir", 1, None, None), ("mirar", 0, None, None), ("mentir", 0, None, None), 
            ("enamorar", 0, None, None), ("reír", 0, None, None), ("celebrar", 0, None, None), 
            ("ganar", 0, None, None), ("construir", 0, None, None)
        ],
        "adjetivos": [
            ("fuerte", 0, 0, 0), ("dorado", 1, 0, 0), ("libre", 0, 0, 0), ("loco", 1, 0, 0), 
            ("encantadora", 1, 1, 0), ("desastre", 1, 0, 0), ("enamorado", 1, 0, 0), 
            ("feliz", 0, 0, 0), ("brillante", 0, 0, 0), ("alegre", 0, 0, 0), ("rápido", 0, 0, 0)
        ]
    },
    "triste": {
        "sustantivos": [
            ("noche", 1, 1, 0), ("camino", 1, 0, 0), ("luz", 0, 1, 0), ("disco", 1, 0, 0), 
            ("ojos", 1, 0, 1), ("error", 0, 0, 0), ("lluvia", 1, 1, 0), ("niebla", 1, 1, 0), 
            ("invierno", 1, 0, 0), ("sombra", 1, 1, 0), ("silencio", 1, 0, 0), ("olvido", 1, 0, 0), 
            ("tren", 0, 0, 0), ("lágrima", 2, 1, 0)
        ],
        "verbos": [
            ("llorar", 0, None, None), ("suspirar", 0, None, None), ("recordar", 0, None, None), 
            ("perder", 0, None, None), ("extrañar", 0, None, None), ("abandonar", 0, None, None), 
            ("olvidar", 0, None, None), ("caminar", 0, None, None), ("mirar", 0, None, None), 
            ("callar", 0, None, None), ("esperar", 0, None, None), ("caer", 0, None, None), 
            ("temblar", 0, None, None), ("romper", 0, None, None), ("escribir", 0, None, None), ("correr", 0, None, None)
        ],
        "adjetivos": [
            ("triste", 1, 0, 0), ("solo", 1, 0, 0), ("vacío", 1, 0, 0), ("gris", 0, 0, 0), 
            ("oscuro", 1, 0, 0), ("frío", 1, 0, 0), ("lejano", 1, 0, 0), ("marchito", 1, 0, 0), 
            ("perdido", 1, 0, 0), ("roto", 1, 0, 0), ("callado", 1, 0, 0), ("apagado", 1, 0, 0), 
            ("nostálgico", 2, 0, 0), ("sombrío", 1, 0, 0), ("abandonado", 1, 0, 0)
        ]
    },
    "nostálgico": {
        "sustantivos": [
            ("recuerdo", 1, 0, 0), ("infancia", 1, 1, 0), ("otoño", 1, 0, 0), ("tarde", 1, 1, 0), 
            ("hogar", 0, 0, 0), ("viaje", 1, 0, 0), ("fotografía", 2, 1, 0), ("canción", 0, 1, 0), 
            ("tiempo", 1, 0, 0), ("ayer", 1, 0, 0), ("memoria", 1, 1, 0), ("historia", 1, 1, 0), 
            ("nostalgia", 1, 1, 0), ("verano", 1, 0, 0), ("amigo", 1, 0, 0)
        ],
        "verbos": [
            ("recordar", 0, None, None), ("volver", 0, None, None), ("mirar", 0, None, None), 
            ("soñar", 0, None, None), ("pensar", 0, None, None), ("extrañar", 0, None, None), 
            ("caminar", 0, None, None), ("sentir", 0, None, None), ("escuchar", 0, None, None), 
            ("vivir", 0, None, None), ("imaginar", 0, None, None), ("evocar", 0, None, None), 
            ("añorar", 0, None, None), ("buscar", 0, None, None), ("guardar", 0, None, None)
        ],
        "adjetivos": [
            ("antiguo", 1, 0, 0), ("lejano", 1, 0, 0), ("pasado", 1, 0, 0), ("viejo", 1, 0, 0), 
            ("perdido", 1, 0, 0), ("olvidado", 1, 0, 0), ("melancólico", 2, 0, 0), 
            ("nostálgico", 2, 0, 0), ("remoto", 1, 0, 0), ("eterno", 1, 0, 0), ("fugaz", 0, 0, 0), 
            ("cálido", 2, 0, 0), ("suave", 1, 0, 0), ("apagado", 1, 0, 0), ("dorado", 1, 0, 0)
        ]
    },
    "decidido": {
        "sustantivos": [
            ("meta", 1, 1, 0), ("decisión", 0, 1, 0), ("camino", 1, 0, 0), ("objetivo", 2, 0, 0), 
            ("logro", 1, 0, 0), ("plan", 0, 0, 0), ("destino", 1, 0, 0), ("reto", 1, 0, 0), 
            ("avance", 1, 0, 0), ("triunfo", 1, 0, 0)
        ],
        "verbos": [
            ("decidir", 0, None, None), ("avanzar", 0, None, None), ("lograr", 0, None, None), 
            ("superar", 0, None, None), ("alcanzar", 0, None, None), ("actuar", 0, None, None), 
            ("persistir", 0, None, None), ("intentar", 0, None, None), ("conseguir", 0, None, None), ("luchar", 0, None, None)
        ],
        "adjetivos": [
            ("firme", 1, 0, 0), ("seguro", 1, 0, 0), ("claro", 1, 0, 0), ("decidido", 1, 0, 0), 
            ("valiente", 1, 0, 0), ("constante", 1, 0, 0), ("directo", 1, 0, 0), ("resuelto", 1, 0, 0), 
            ("tenaz", 0, 0, 0), ("capaz", 0, 0, 0)
        ]
    },
    "esperanzador": {
        "sustantivos": [
            ("esperanza", 1, 1, 0), ("futuro", 1, 0, 0), ("luz", 0, 1, 0), ("sueño", 1, 0, 0), 
            ("oportunidad", 2, 1, 0), ("cambio", 1, 0, 0), ("mañana", 1, 1, 0), ("ilusión", 0, 1, 0), 
            ("camino", 1, 0, 0), ("meta", 1, 1, 0)
        ],
        "verbos": [
            ("esperar", 0, None, None), ("soñar", 0, None, None), ("crecer", 0, None, None), 
            ("avanzar", 0, None, None), ("mejorar", 0, None, None), ("confiar", 0, None, None), 
            ("lograr", 0, None, None), ("imaginar", 0, None, None), ("alcanzar", 0, None, None), ("renacer", 0, None, None)
        ],
        "adjetivos": [
            ("brillante", 1, 0, 0), ("posible", 1, 0, 0), ("nuevo", 1, 0, 0), ("futuro", 1, 0, 0), 
            ("esperanzador", 0, 0, 0), ("luminoso", 1, 0, 0), ("positivo", 2, 0, 0), 
            ("claro", 1, 0, 0), ("radiante", 1, 0, 0), ("optimista", 2, 0, 0)
        ]
    },
    "tenso": {
        "sustantivos": [
            ("silencio", 1, 0, 0), ("espera", 1, 1, 0), ("nervio", 1, 0, 0), ("riesgo", 1, 0, 0), 
            ("conflicto", 2, 0, 0), ("miedo", 1, 0, 0), ("presión", 0, 1, 0), ("momento", 1, 0, 0), 
            ("crisis", 1, 1, 0), ("peligro", 1, 0, 0)
        ],
        "verbos": [
            ("tensar", 0, None, None), ("esperar", 0, None, None), ("temblar", 0, None, None), 
            ("dudar", 0, None, None), ("contener", 0, None, None), ("vigilar", 0, None, None), 
            ("enfrentar", 0, None, None), ("resistir", 0, None, None), ("presionar", 0, None, None), ("aguantar", 0, None, None)
        ],
        "adjetivos": [
            ("tenso", 1, 0, 0), ("nervioso", 1, 0, 0), ("inquieto", 1, 0, 0), ("rígido", 2, 0, 0), 
            ("crítico", 2, 0, 0), ("inestable", 1, 0, 0), ("urgente", 1, 0, 0), ("delicado", 1, 0, 0), 
            ("peligroso", 1, 0, 0), ("intenso", 1, 0, 0)
        ]
    }
}


plantillas = {

    "INTRO": [
        "Suena [art:un:s:0] [s:0] en [art:el:s:1] [s:1]",
        "Todo empieza con [art:un:s:0] [s:0]",
        "Siento [art:el:s:0] [s:0] al [v:1]",
        "Bajo [art:el:s:1] [s:1] voy a [v:1]",
        "[art:tu:s:0] [s:0] se acerca al [v:1]"
    ],
    "VERSO": [
        "En [art:mi:s:0] [s:0] veo [art:un:s:1] [s:1]",
        "No quiero [v:1] [art:este:s:0] [s:0] [a:0]",
        "Buscando [art:un:s:1] [s:1] para [v:1]",
        "Desde [art:aquel:s:0] [s:0] no dejo de [v:1]",
        "Guardo [art:este:s:1] [s:1] en [art:mi:s:0] [s:0]",
        "[art:tu:s:0] [s:0] me hace [v:1] sin pensar",
        "Entre [art:el:s:1] [s:1] y [art:el:s:0] [s:0] te vi",
        "No queda [s:1] para [v:1]",
        "Sigo [art:tu:s:0] [s:0] aunque duela [v:1]",
        "En cada [s:1] vuelvo a [v:1]",
        "[art:tu:s:0] [s:0] rompió [art:mi:s:0] [s:0]",
        "Busco [art:una:s:1] [s:1] para no [v:1]",
        "Dejé [art:el:s:0] [s:0] atrás para [v:1]"
    ],
    "ESTRIBILLO": [
        "Siento [art:el:s:0] [s:0] al [v:1]",
        "Eres [art:mi:s:0] [s:0] [a:0]",
        "Vamos a [v:1] bajo [art:el:s:0] [s:0]",
        "Bailo con [art:tu:s:0] [s:0] hasta [v:1]",
        "Eres [art:mi:s:0] [s:0] más [a:0]",
        "Quiero [v:1] sin miedo [art:al:s:0] [s:0]",
        "[art:tu:s:0] [s:0] me hace [v:1]",
        "Vamos a [v:1] sin mirar [art:el:s:0] [s:0]",
        "Eres ese [s:0] tan [a:0]",
        "No voy a [v:1] [art:este:s:0] [s:0]",
        "Siento [art:tu:s:0] [s:0] al [v:1]",
        "Bajo [art:el:s:1] [s:1] te vi [v:1]",
        "[art:tu:s:0] [s:0] suena tan [a:0]"
    ],
    "PUENTE": [
        "Y ahora no sé si [v:1]",
        "Dime si vas a [v:1]",
        "Todo empezó con [art:un:s:0] [s:0]",
        "Quiero [v:1] aunque duela [art:el:s:0] [s:0]",
        "Entre [art:el:s:0] [s:0] y tú, me perdí",
        "Déjame [v:1] [art:una:s:1] [s:1] vez más"
    ],
    "FINAL": [
        "Se apaga [art:el:s:0] [s:0] sin [v:1]",
        "Solo queda [s:1] en mí",
        "Vuelvo a [art:ese:s:0] [s:0] para [v:1]",
        "[art:tu:s:0] [s:0] se va, dejo de [v:1]",
        "Y [art:el:s:0] [s:0] se vuelve [a:0]"
    ]
}

def concordancia(palabra_base, genero, numero, tipo):
    """Ajusta artículos y adjetivos al sustantivo (Género: 0=M, 1=F | Número: 0=S, 1=P)"""
    
    # Manejo de Artículos
    articulos = {
        "un":  ["un", "una", "unos", "unas"],
        "el":  ["el", "la", "los", "las"],
        "este": ["este", "esta", "estos", "estas"],
        "mi":   ["mi", "mi", "mis", "mis"],
        "tu":   ["tu", "tu", "tus", "tus"]
    }

    if tipo == "articulo":
        idx = (genero + (2 * numero)) # Lógica: 0=MS, 1=FS, 2=MP, 3=FP
        return articulos.get(palabra_base, [palabra_base]*4)[idx]

    if tipo == "adjetivo":
        # Si el adjetivo termina en 'o', cambiamos género y número
        if palabra_base.endswith("o"):
            base = palabra_base[:-1]
            gen = "o" if genero == 0 else "a"
            num = "" if numero == 0 else "s"
            return base + gen + num
        # Si termina en 'e' o consonante, solo añadimos plural
        elif numero == 1:
            return palabra_base + "s" if palabra_base[-1] in "aeiou" else palabra_base + "es"
            
    return palabra_base

def obtener_palabra(animo, tipo_tag, acento):
    """Selecciona palabra y devuelve la tupla completa (texto, tonica, gen, num)"""
    mapeo = {"s": "sustantivos", "v": "verbos", "a": "adjetivos"}
    cat = mapeo[tipo_tag]
    candidatas = [p for p in biblioteca_lexica[animo][cat] if p[1] == acento]
    
    if not candidatas:
        return random.choice(biblioteca_lexica[animo][cat])
    return random.choice(candidatas)

def procesar_plantilla(animo, plantilla):
    """
    Procesador con concordancia gramatical múltiple.
    Gestiona género y número para cada sustantivo de forma independiente.
    """
    items = plantilla.split()
    resultado = []
    
    # Diccionario para recordar cada sustantivo por su ID (0 o 1)
    # Guardamos la tupla entera: (palabra, tonica, genero, numero)
    memoria_sustantivos = {}

    # --- PRIMERA PASADA: Identificar y generar todos los sustantivos ---
    for item in items:
        if "[s:" in item:
            idx_abre, idx_cierra = item.find("["), item.find("]")
            tag = item[idx_abre+1 : idx_cierra].split(":")
            id_s = int(tag[1])
            # Guardamos la tupla de 4 elementos en la memoria usando su ID
            memoria_sustantivos[id_s] = obtener_palabra(animo, "s", id_s)

    # --- SEGUNDA PASADA: Construir la frase con concordancia ---
    for item in items:
        if "[" in item and ":" in item and "]" in item:
            idx_abre, idx_cierra = item.find("["), item.find("]")
            tag = item[idx_abre+1 : idx_cierra].split(":")
            
            # Recuperamos texto antes y después del corchete (ej: puntuación)
            antes, despues = item[:idx_abre], item[idx_cierra+1:]
            palabra_final = ""

            # Caso A: Artículos inteligentes [art:base:tipo_ref:id_ref]
            # Ejemplo: [art:el:s:0]
            if tag[0] == "art":
                base_art = tag[1]
                ref_id = int(tag[3]) # El ID del sustantivo al que se refiere
                # Sacamos género (gen) y número (num) del sustantivo guardado
                _, _, gen, num = memoria_sustantivos[ref_id]
                palabra_final = concordancia(base_art, gen, num, "articulo")

            # Caso B: Sustantivos [s:ID]
            elif tag[0] == "s":
                ref_id = int(tag[1])
                palabra_final = memoria_sustantivos[ref_id][0] # Solo el texto

            # Caso C: Adjetivos [a:acento]
            elif tag[0] == "a":
                # Obtenemos un adjetivo al azar
                adj_tupla = obtener_palabra(animo, "a", int(tag[1]))
                # Concordamos con el sustantivo principal (el ID 0)
                _, _, gen, num = memoria_sustantivos.get(0, ("cosa", 0, 0, 0))
                palabra_final = concordancia(adj_tupla[0], gen, num, "adjetivo")

            # Caso D: Verbos [v:acento]
            elif tag[0] == "v":
                verbo_tupla = obtener_palabra(animo, "v", int(tag[1]))
                palabra_final = verbo_tupla[0]

            resultado.append(antes + palabra_final + despues)
        else:
            # Palabras normales (en, de, con...)
            resultado.append(item)

    return " ".join(resultado)


def generar_letra_completa(mapa_secciones, animo):
    """
    Genera la lírica completa asegurando que INTRO y FINAL 
    también tengan contenido basado en sus plantillas.
    """
    # 1. Pre-generamos bloques fijos para mantener coherencia en la canción
    # El Estribillo y el Puente deben repetirse igual para ser memorables
    coro_fijo = [procesar_plantilla(animo, random.choice(plantillas["ESTRIBILLO"])) for _ in range(2)]
    
    # Solo generamos puente si la canción es larga y existe en las plantillas
    puente_fijo = []
    if "PUENTE" in plantillas:
        puente_fijo = [procesar_plantilla(animo, random.choice(plantillas["PUENTE"])) for _ in range(2)]
    
    letra_final = []

    # 2. Recorremos el mapa de secciones (Intro -> Verso -> Estribillo...)
    for i, seccion in enumerate(mapa_secciones):
        
        # Caso A: Secciones con contenido dinámico (Verso)
        if seccion == "VERSO":
            linea = procesar_plantilla(animo, random.choice(plantillas["VERSO"]))
            letra_final.append(f"[{seccion}] {linea}")
            
        # Caso B: Secciones con contenido fijo/repetitivo (Estribillo/Puente)
        elif seccion == "ESTRIBILLO":
            linea = coro_fijo[i % len(coro_fijo)]
            letra_final.append(f"[{seccion}] {linea}")
            
        elif seccion == "PUENTE":
            if puente_fijo:
                linea = puente_fijo[i % len(puente_fijo)]
                letra_final.append(f"[{seccion}] {linea}")
        
        # Caso C: INTRO y FINAL (Ahora con generación de letra)
        elif seccion in ["INTRO", "FINAL"]:
            # Buscamos una plantilla específica para Intro o Final
            if seccion in plantillas and plantillas[seccion]:
                linea = procesar_plantilla(animo, random.choice(plantillas[seccion]))
                letra_final.append(f"[{seccion}] {linea}")
            else:
                # Si por algún motivo no hay plantillas, evitamos que quede vacío
                letra_final.append(f"[{seccion}] ...")
                
    return letra_final

# --- PRUEBA DE EJECUCIÓN ---
if __name__ == "__main__":
    # Simulación de un mapa de canción real
    mapa_ejemplo = ["INTRO", "VERSO", "VERSO", "ESTRIBILLO", "ESTRIBILLO", "FINAL"]
    
    # Generamos la letra para un ánimo "alegre"
    resultado = generar_letra_completa(mapa_ejemplo, "alegre")
    
    # Mostramos el resultado por consola
    for linea in resultado:
        print(linea)