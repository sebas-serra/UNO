import streamlit as st
import Mazo 
import Jugador

st.set_page_config(page_title="UNO", layout="wide")

COLORES = {
    "Azul": "#1e90ff",
    "Rojo": "#e63946",
    "Verde": "#2dc653",
    "Amarillo": "#ffd166",
    "negro": "#352e48"
}

def color_texto(color):
    return "white" if color in ["Azul", "Rojo", "Verde", "negro"] else "black"

def carta_html(numero, color):
    bg = COLORES.get(color, "#ccc")
    txt = color_texto(color)
    return f"""
        <div style='display:inline-block; background:{bg}; color:{txt};
        border-radius:10px; padding:10px 18px; margin:5px;
        font-size:28px; font-weight:bold; border: 3px solid white;
        min-width:55px; text-align:center;'>
        {numero}
        </div>
    """

if "juego_iniciado" not in st.session_state:
    st.session_state.juego_iniciado = False
if "jugadores" not in st.session_state:
    st.session_state.jugadores = []
if "coso" not in st.session_state:
    st.session_state.coso = None
if "partida" not in st.session_state:
    st.session_state.partida = None
if "turno" not in st.session_state:
    st.session_state.turno = 0
if "mensaje" not in st.session_state:
    st.session_state.mensaje = ""
if "eligiendo_color" not in st.session_state:
    st.session_state.eligiendo_color = False
if "ganador" not in st.session_state:
    st.session_state.ganador = None



def iniciar_juego():
    mazo = Mazo.Baraja()
    mazo.crearmazo()
    jugadores = []
    for _ in range(4):
        p = Jugador.Player()
        p.iniciar(mazo)
        jugadores.append(p)
    st.session_state.coso = mazo
    st.session_state.jugadores = jugadores
    st.session_state.partida = mazo.tomarcarta()
    st.session_state.turno = 0
    st.session_state.juego_iniciado = True
    st.session_state.mensaje = "Juego iniciado Turno del Jugador 1"
    st.session_state.ganador = None





def jugador_actual():
    return st.session_state.jugadores[st.session_state.turno]



def avanzar_turno(saltar=False):
    for i, jugador in enumerate(st.session_state.jugadores):
        if len(jugador.mano) == 0:
            st.session_state.ganador = i + 1
            return
    salto = 2 if saltar else 1
    st.session_state.turno = (st.session_state.turno + salto) % len(st.session_state.jugadores)
    st.session_state.mensaje = f"Turno del Jugador {st.session_state.turno + 1}"



def jugar_carta(id):
    jugador = jugador_actual()
    carta = jugador.mano[id]
    if not carta.comprobar(st.session_state.partida):
        st.session_state.mensaje = "Carta no válida"
        return

    jugador.mano.pop(id)
    st.session_state.partida = carta

    if carta.numero == "+2":
        siguiente = st.session_state.jugadores[(st.session_state.turno + 1) % len(st.session_state.jugadores)]
        siguiente.robar(st.session_state.coso)
        siguiente.robar(st.session_state.coso)
        avanzar_turno()


    elif carta.numero == "+4":
        siguiente = st.session_state.jugadores[(st.session_state.turno + 1) % len(st.session_state.jugadores)]
        for _ in range(4):
            siguiente.robar(st.session_state.coso)
        st.session_state.eligiendo_color = True
        avanzar_turno()


    elif carta.numero == "@":
        st.session_state.eligiendo_color = True
        avanzar_turno()

    elif carta.numero == "*":
        avanzar_turno(saltar=True)

    else:
        avanzar_turno()

def elegir_color(color):
    st.session_state.partida.color = color
    st.session_state.eligiendo_color = False
    avanzar_turno()

def pasar_turno():
    jugador_actual().robar(st.session_state.coso)
    avanzar_turno()





st.title("Juego UNO")

if not st.session_state.juego_iniciado:
    st.markdown("### Bienvenido al UNO")
    if st.button("Iniciar juego", type="primary"):
        iniciar_juego()
        st.rerun()

else:
    if st.session_state.ganador:
        st.success(f"🏆 ¡El Jugador {st.session_state.ganador} ha ganado!")
        if st.button("Jugar de nuevo"):
            iniciar_juego()
            st.rerun()
        st.stop()

    st.markdown("### Carta en la pila")
    p = st.session_state.partida
    st.markdown(carta_html(p.numero, p.color), unsafe_allow_html=True)

    st.divider()


    if st.session_state.eligiendo_color:
        st.markdown("### 🎨 Elige un color")
        cols = st.columns(4)
        for col, (nombre, hex_color) in zip(cols, [("Rojo","Rojo"),("Azul","Azul"),("Verde","Verde"),("Amarillo","Amarillo")]):
            with col:
                if st.button(nombre, key=f"color_{nombre}"):
                    elegir_color(nombre)
                    st.rerun()
        st.stop()

    # Turno actual
    turno = st.session_state.turno
    st.markdown(f"### 👤 Turno: Jugador {turno + 1}")
    if st.session_state.mensaje:
        st.info(st.session_state.mensaje)



    st.markdown("#### Tu mano:")
    jugador = jugador_actual()
    cols = st.columns(max(len(jugador.mano), 1))
    for i, carta in enumerate(jugador.mano):
        with cols[i]:
            st.markdown(carta_html(carta.numero, carta.color), unsafe_allow_html=True)
            if st.button("Jugar", key=f"carta_{i}"):
                jugar_carta(i)
                st.rerun()


    st.divider()
    st.markdown("#### Otros jugadores:")
    otros_cols = st.columns(3)
    for i, jugador_otro in enumerate(st.session_state.jugadores):
        if i == turno:
            continue
        with otros_cols[i % 3]:
            st.markdown(f"**Jugador {i+1}:** {len(jugador_otro.mano)} cartas")

    # Pasar turno
    st.divider()
    if st.button("Pasar turno (robar carta)", type="secondary"):
        pasar_turno()
        st.rerun()