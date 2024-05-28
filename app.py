import pandas as pd
import streamlit as st
import plotly.express as px

# URL del archivo Excel en el repositorio de GitHub
excel_url = 'https://github.com/dcamarena2505/dashboard1/raw/main/calificaciones.xlsx'

@st.cache
def load_data(url):
    return pd.read_excel(url)

# Cargar el archivo de Excel desde la URL
df = load_data(excel_url).copy()

# Calcular las notas promedio de cada estudiante
df['Promedio_Tareas'] = df[['TS1', 'TS2', 'TS3', 'TS4', 'TS5', 'TS6', 'TS7', 'TS8', 'TS9', 'TS10', 'TS11']].mean(axis=1)
df['Promedio_Evaluaciones'] = df[['Q1', 'Q2', 'Q3', 'Q4']].mean(axis=1)
df['Promedio_Laboratorio'] = df[['EL1', 'EL2']].mean(axis=1)
df['Promedio_Trabajo_Grupal'] = df[['TG1', 'TG2', 'TG3', 'TG4']].mean(axis=1)
df['Promedio_Proyectos'] = df[['P1', 'P2']].mean(axis=1)
df['Promedio_General'] = df[['Promedio_Tareas', 'Promedio_Evaluaciones', 'Promedio_Laboratorio', 'Promedio_Trabajo_Grupal', 'Promedio_Proyectos']].mean(axis=1)

# Definir los rangos de calificaciones
def categorize_grade(grade):
    if pd.isna(grade):
        return 'NP'
    elif grade >= 18:
        return 'Excelente'
    elif grade >= 16:
        return 'Muy Bueno'
    elif grade >= 14:
        return 'Bueno'
    elif grade >= 11:
        return 'Moderado'
    elif grade >= 8:
        return 'Malo'
    else:
        return 'Muy Malo'

# Aplicar la categorización a todas las evaluaciones
evaluaciones = ['TS1', 'TS2', 'TS3', 'TS4', 'TS5', 'TS6', 'TS7', 'TS8', 'TS9', 'TS10', 'TS11', 'Q1', 'Q2', 'Q3', 'Q4', 'EL1', 'EL2', 'TG1', 'TG2', 'TG3', 'TG4', 'P1', 'P2', 'P2E', 'EP', 'EF']
for eval in evaluaciones:
    df[f'{eval}_Cat'] = df[eval].apply(categorize_grade)

# Configurar Streamlit
st.title("Dashboard de Calificaciones")

filter_option = st.selectbox("Seleccionar filtro", ["Profesor", "Carrera", "Sección", "Vez", "Alumno"])
filter_value = st.selectbox("Seleccionar valor", df[filter_option].unique())

filtered_df = df[df[filter_option] == filter_value]

evaluacion_option = st.selectbox("Seleccionar evaluación", evaluaciones)

if filter_option == "Alumno":
    # Mostrar todas las evaluaciones para un estudiante específico
    fig = px.histogram(filtered_df.melt(id_vars=[filter_option], value_vars=evaluaciones),
                       x='variable', y='value', color='variable',
                       title=f'Rendimiento Histórico - {filter_value}',
                       labels={'variable': 'Evaluación', 'value': 'Nota'})
    
    st.plotly_chart(fig)

    st.subheader("Promedios")
    st.write(f"Promedio acumulado de la evaluación continua: {filtered_df['Promedio_General'].values[0]:.2f}")
    st.write(f"Promedio de quiz: {filtered_df['Promedio_Evaluaciones'].values[0]:.2f}")
    st.write(f"Promedio de exámenes de laboratorio: {filtered_df['Promedio_Laboratorio'].values[0]:.2f}")
    st.write(f"Promedio de trabajos grupales: {filtered_df['Promedio_Trabajo_Grupal'].values[0]:.2f}")
    st.write(f"Promedio de tareas semanales: {filtered_df['Promedio_Tareas'].values[0]:.2f}")

    fig_comparacion = px.scatter(df, x='Promedio_General', y='Promedio_Evaluaciones',
                                 color='Carrera',
                                 title='Comparación de Promedio General vs Promedio de Evaluaciones',
                                 labels={'Promedio_General': 'Promedio General', 'Promedio_Evaluaciones': 'Promedio de Evaluaciones'})
    st.plotly_chart(fig_comparacion)
else:
    # Mostrar una evaluación específica para todos los estudiantes filtrados
    fig = px.histogram(filtered_df, 
                       x=f'{evaluacion_option}_Cat', 
                       color=f'{evaluacion_option}_Cat',
                       category_orders={f'{evaluacion_option}_Cat': ['Excelente', 'Muy Bueno', 'Bueno', 'Moderado', 'Malo', 'Muy Malo', 'NP']},
                       title=f'Rendimiento en {evaluacion_option} - {filter_value}',
                       labels={f'{evaluacion_option}_Cat': 'Categoría', 'count': 'Cantidad de Estudiantes'},
                       color_discrete_map={
                           'Excelente': 'green',
                           'Muy Bueno': 'limegreen',
                           'Bueno': 'yellow',
                           'Moderado': 'orange',
                           'Malo': 'orangered',
                           'Muy Malo': 'red',
                           'NP': 'blue'
                       })
    
    st.plotly_chart(fig)
    
    # Calcular los promedios correctamente para la evaluación específica
    prom_aula = filtered_df[evaluacion_option].mean()
    prom_general = df[evaluacion_option].mean()

    st.subheader("Promedios")
    st.write(f"Promedio del Aula ({filter_value}) en {evaluacion_option}: {prom_aula:.2f}")
    st.write(f"Promedio General en {evaluacion_option}: {prom_general:.2f}")

    fig_comparacion = px.scatter(filtered_df, x='Promedio_General', y='Promedio_Evaluaciones',
                                 color='Carrera',
                                 title='Comparación de Promedio General vs Promedio de Evaluaciones',
                                 labels={'Promedio_General': 'Promedio General', 'Promedio_Evaluaciones': 'Promedio de Evaluaciones'})
    st.plotly_chart(fig_comparacion)
