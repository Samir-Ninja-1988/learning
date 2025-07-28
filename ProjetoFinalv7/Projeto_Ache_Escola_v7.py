import streamlit as st 
import pandas as pd 
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from geopy.distance import distance
import matplotlib.pyplot as plt
import seaborn as sns


with st.sidebar:
    st.markdown("Desenvolvido por:")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://github.com/Samir-Ninja-1988/learning/tree/main/ProjetoFinalv7/Imagem_Vini.png", width=40)
    with col2:
        st.text("Vinicius Ferreira Aguiar - \nBackend")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://github.com/Samir-Ninja-1988/learning/tree/main/ProjetoFinalv7/Imagem_Claudio.jpg", width=40)
    with col2:
        st.text("Claudio Regis de Lima Cruz - \nCientista de Dados")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://github.com/Samir-Ninja-1988/learning/tree/main/ProjetoFinalv7/Imagem_Samir.jpg", width=40)
    with col2:
        st.text("Samir Saraiva Machado - \nFrontend")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://github.com/Samir-Ninja-1988/learning/tree/main/ProjetoFinalv7/Imagem_Lucas.png", width=40)
    with col2:
        st.text("Lucas Cisne Cunha - \nEngenharia de Dados")

st.header("🔍📚 Acha a escola Fortaleza-CE")
df = pd.read_csv('datatratado.csv', sep=';')

tab1, tab2, tab3 = st.tabs(["Apresentação", "Análise de dados", "Inferência"])

with tab1:
    st.header("Introdução")
    st.text('A educação básica é um dos pilares fundamentais para o desenvolvimento social e econômico de qualquer país. Garantir o acesso à informação sobre instituições de ensino primário e médio é essencial para famílias, gestores públicos e pesquisadores que buscam compreender e melhorar a distribuição educacional em Fortaleza-CE')
    st.text('Este projeto tem como objetivo principal desenvolver uma solução capaz de localizar escolas de ensino fundamental e médio a partir de um endereço fornecido. A proposta envolve a integração de tecnologias de geolocalização, bases de dados educacionais e ferramentas de visualização para facilitar a identificação de instituições próximas, promovendo maior transparência e acessibilidade à informação.')
    st.text('Ao permitir que usuários encontrem escolas com base em sua localização, o projeto contribui para:')
    st.text('📍 Facilitar o planejamento familiar na escolha de instituições de ensino')
    st.text('🏫 Apoiar gestores públicos na análise da cobertura educacional')
    st.text('📊 Oferecer dados relevantes para estudos sobre distribuição escolar na cidade de Fortaleza-CE')
    st.text('Com essa iniciativa, buscamos aproximar a informação educacional da realidade cotidiana, promovendo uma sociedade mais informada e preparada para tomar decisões conscientes.')

with tab2:
  st.header("Análise de Dados das Escolas em Fortaleza")
  st.subheader("Top 10 Bairros com Mais Escolas")
  
    # Prepara o gráfico
  plt.figure(figsize=(12, 6))
  top_10_bairros = df['BAIRRO'].value_counts().nlargest(10)
  sns.barplot(x=top_10_bairros.index, y=top_10_bairros.values, palette='viridis')
  plt.title('Top 10 Bairros com Mais Escolas em Fortaleza')
  plt.xlabel('Bairro')
  plt.ylabel('Número de Escolas')
  plt.xticks(rotation=45, ha='right')
  plt.tight_layout()
    
    # Exibe o gráfico no Streamlit
  st.pyplot(plt)
  st.info("Este gráfico mostra os 10 bairros com a maior concentração de escolas, permitindo identificar as áreas com maior infraestrutura educacional.")


    # --- Gráfico 2: Distribuição de Tipos de Escola ---
  st.subheader("Distribuição de Tipos de Escola")

    # Prepara o gráfico
  plt.figure(figsize=(10, 8))
    # Usamos 'BUSCA_ID' por não ter valores faltantes para o tipo de escola
  school_type_counts = df['BUSCA_ID'].value_counts()
  plt.pie(school_type_counts, labels=school_type_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
  plt.title('Distribuição de Tipos de Escola')
  plt.ylabel('') # Oculta o label do eixo y

    # Exibe o gráfico no Streamlit
  st.pyplot(plt)
  st.info("O gráfico de pizza ilustra a proporção de cada tipo de escola no dataset. Vemos que a maioria das escolas é de 'Ensino Médio', seguida por 'escola primária'.")
  
with tab3:
    st.header("Ache sua escola")

    # Entrada do nome
    nome = st.text_input("Digite seu nome")
    if nome:
        st.write(f"Saudações {nome}! Agora nós vamos encontrar as escolas mais próximas do bairro!")

    #Carregando csv dos bairros
    df=pd.read_csv('datatratado.csv',sep=';')

    bairros = (
                df['BAIRRO'].astype(str).str.strip().replace({'': pd.NA, 'nan': pd.NA}).dropna().sort_values().unique()
                )

    # Entrada do Bairro
    bairro = st.selectbox(
                                    "Cidade",
                                    bairros,
                                    index=None,                        
                                    placeholder="Digite para pesquisar..." 
                            )
    
    if bairro:
        
        #geolocator=Nominatim(user_agent='geoapi')
        #location=geolocator.geocode(bairro)
        #lat=location.latitude
        #lon=location.longitude
        
        lat=df[df['BAIRRO']==bairro]['LAT_BAIRRO'].iloc[0]
        lon=df[df['BAIRRO']==bairro]['LONG_BAIRRO'].iloc[0]
        
        #print(df['LAT'].mean(),df['LON'].mean())
        
        mapa=folium.Map(location=(lat.mean(),lon.mean()),zoom_start=12)
        marcador=folium.Marker(location=(lat,lon),icon=folium.Icon(color='red'))
        marcador.add_to(mapa)
        
        df_proximo = df[df['BAIRRO']==bairro]
        df_proximo_medio = df_proximo[df_proximo['BUSCA_ID']=='Ensino Médio']
        df_proximo_primaria = df_proximo[df_proximo['BUSCA_ID']=='escola primária']

        #def calculadistancia(row):
        #    return distance((lat,lon),(row['LAT'],row['LON'])).km
        #df['DISTANCIA']=df.apply(calculadistancia,axis=1)
        #df_proximo=df[df['DISTANCIA']<0.5].reset_index(drop=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<p style='color: red;'>Bairro</p>", unsafe_allow_html=True)

        with col2:
            st.markdown("<p style='color: green;'>Escola Primária</p>", unsafe_allow_html=True)

        with col3:
            st.markdown("<p style='color: blue;'>Ensino Médio</p>", unsafe_allow_html=True)


        for i in range(len(df_proximo_medio)):
            marcador=folium.Marker(location=(df_proximo_medio['LATITUDE'].iloc[i],df_proximo_medio['LONGITUDE'].iloc[i]),popup=df_proximo_medio['NOME'].iloc[i],icon=folium.Icon(color='blue'))
            marcador.add_to(mapa)
        
        for i in range(len(df_proximo_primaria)):
            marcador1=folium.Marker(location=(df_proximo_primaria['LATITUDE'].iloc[i],df_proximo_primaria['LONGITUDE'].iloc[i]),popup=df_proximo_primaria['NOME'].iloc[i],icon=folium.Icon(color='green'))
            marcador1.add_to(mapa)

        
        st_folium(mapa, width=725, height=500)
  
        st.write(f"Escolas Primarias encontradas no bairro {bairro}:\n")
        st.dataframe(df_proximo_primaria[['NOME', 'LOCAL']],hide_index=True)

        st.write(f"Escolas de Ensino Médio encontradas no bairro {bairro}:\n")
        st.dataframe(df_proximo_medio[['NOME', 'LOCAL']],hide_index=True)
