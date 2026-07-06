import streamlit as st
import datetime

st.set_page_config(page_title="Treino Futevôlei", layout="centered")

st.title("🏖️ Treino do Dia")

# Definir treino automático
dia = datetime.datetime.today().weekday()

if dia in [0, 3]:
    treino = "A"
elif dia in [1, 4]:
    treino = "B"
else:
    treino = "C"

st.subheader(f"Treino {treino}")

# Exercícios
treinos = {
    "A": ["Supino", "Tríceps", "Abdominal"],
    "B": ["Puxada", "Bíceps", "Core"],
    "C": ["Agachamento", "Panturrilha", "HIIT"],
}

# Interface
concluidos = []

for exercicio in treinos[treino]:
    col1, col2 = st.columns([2, 1])

    with col1:
        check = st.checkbox(exercicio)
    with col2:
        carga = st.number_input(f"Carga {exercicio}", min_value=0, key=exercicio)

    if check:
        concluidos.append(exercicio)

# Finalizar treino
if st.button("✅ Finalizar treino"):
    st.success(f"Treino concluído! Você fez {len(concluidos)} exercícios.")
