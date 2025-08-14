# app.py
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import base64
# Configuração inicial
st.set_page_config(
    page_title="Observatório Jundiaí - Programa Social para Famílias de Baixa Renda",
    page_icon="📊",
    layout="wide"
)


df = pd.read_parquet('base_final.parquet')
df['count'] = 1
gdf = gpd.read_parquet('shp_bairros.parquet')
meses_referencia = sorted(df['mes_referencia_dados'].unique())


mapa_meses = {
    '01': 'Janeiro',
    '02': 'Fevereiro',
    '03': 'Março',
    '04': 'Abril',
    '05': 'Maio',
    '06': 'Junho',
    '07': 'Julho',
    '08': 'Agosto',
    '09': 'Setembro',
    '10': 'Outubro',
    '11': 'Novembro',
    '12': 'Dezembro'
}

mapa_meses_inverted = {
    'Janeiro': '01',
    'Fevereiro': '02',
    'Março': '03',
    'Abril': '04',
    'Maio': '05',
    'Junho': '06',
    'Julho': '07',
    'Agosto': '08',
    'Setembro': '09',
    'Outubro': '10',
    'Novembro': '11',
    'Dezembro': '12'
}


meses_opcoes = [mapa_meses[m] for m in meses_referencia]


@st.cache_data
def carregar_dados(meses_selecionados):

    meses = [mapa_meses_inverted[m] for m in meses_selecionados]

    df_filtrado = df[df['mes_referencia_dados'].isin(meses)]
    return df_filtrado



with st.sidebar:

    st.image('brasao.ico', width=40)
    st.title("Observatório de Jundiaí")
    st.subheader("Programa Social para Famílias de Baixa Renda")
    st.markdown("""
        Esta ferramenta foi desenvolvida por Henrique Pougy.
    """)


with open("brasao.ico", "rb") as f:
    data = f.read()
logo_base64 = base64.b64encode(data).decode()

st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" style="height:50px; margin-right:15px;">
        <h1 style="margin: 0;">Observatório de Jundiaí - Programa Social para Famílias de Baixa Renda</h1>
    </div>
    """,
    unsafe_allow_html=True
)
    
st.markdown("Observatório de Jundiaí - Programa Social para Famílias de Baixa Renda")
st.subheader("Análise de Dados do Programa Social para Famílias de Baixa Renda de Jundiaí")
with st.expander("Sobre o Programa"):
    st.markdown("""
        O Programa Social para Famílias de Baixa Renda de Jundiaí é uma iniciativa da Prefeitura Municipal que visa promover a inclusão social e a redução das desigualdades na cidade. Através deste programa, são oferecidos diversos serviços e benefícios às famílias em situação de vulnerabilidade, com o objetivo de melhorar a qualidade de vida e proporcionar oportunidades de desenvolvimento social e econômico.
    """)
with st.expander("Sobre a Ferramenta de Análise de Dados"):
    st.markdown("""
            Esta ferramenta de análise de dados foi desenvolvida para apoiar a gestão e o monitoramento do Programa Social para Famílias de Baixa Renda de Jundiaí, oferecendo aos gestores públicos e à sociedade um meio ágil e interativo de explorar informações atualizadas sobre o público atendido. Com base em princípios de política pública orientada por evidências, a solução permite transformar dados gerenciais em conhecimento aplicado, fortalecendo a tomada de decisão, o acompanhamento de resultados e a transparência na execução das ações voltadas à promoção da inclusão social e à redução das desigualdades.
        """)

df['elegivel_txt'] = df['eligivel'].apply(lambda x: 'Sim' if x else 'Não')

with st.container():
    st.subheader("Série Histórica")
    st.markdown("""
        Esta seção apresenta a evolução das pessoas e famílias elegíveis ao programa ao longo do tempo.
    """)
    columns = st.columns(2)

    with columns[0]:

        st.markdown("##### Evolução das Quantidade de Pessoas Elegíveis ao Programa ao longo dos meses")

        df_grouped_eligivel_time_series = (
        df.groupby(['mes_referencia_dados', 'elegivel_txt'])['count']
        .sum()
        .reset_index()
        )

        fig = px.line(
        df_grouped_eligivel_time_series,
        x="mes_referencia_dados",
        y="count",
        color="elegivel_txt",  
        markers=True,
        title="Total de pessoas elegíveis por mês",
        labels={
            "mes_referencia_dados": "Mês de Referência",
            "count": "Total de Pessoas",
            "elegivel_txt": "Elegibilidade"  
        }
        )
        st.plotly_chart(fig, use_container_width=True)

    with columns[1]:

        st.markdown("##### Evolução da quantidade de Famílias Elegíveis ao Programa ao longo dos meses")


        df_grouped_eligivel_time_series_family = (
        df[['mes_referencia_dados', 'cod_familiar', 'elegivel_txt', 'count']].drop_duplicates()\
            .groupby(['mes_referencia_dados', 'elegivel_txt'])['count']
        .sum()
        .reset_index()
        )

        fig = px.line(
        df_grouped_eligivel_time_series_family,
        x="mes_referencia_dados",
        y="count",
        color="elegivel_txt",  
        markers=True,
        title="Total de famílias elegíveis por mês",
        labels={
            "mes_referencia_dados": "Mês de Referência",
            "count": "Total de famílias",
            "elegivel_txt": "Elegibilidade"  
        }
        )
        st.plotly_chart(fig, use_container_width=True)
    


# Seletor múltiplo
meses_selecionados = st.multiselect(
    "Selecione um ou mais meses",
    options=meses_opcoes,
    default='Janeiro'  # seleciona janeiro por padrao
)
df_filtrado = carregar_dados(meses_selecionados)


with st.container(border=True):

    st.subheader("Dados Gerais do Programa para os meses selecionados")

    columns = st.columns(2)
    with columns[0]:
        st.metric(
            label="Total de pessoas elegíveis",
            value=df_filtrado['eligivel'].sum(),
        )

    with columns[1]:
        st.metric(
            label="Total de famílias elegíveis",
            value=df_filtrado[df_filtrado['eligivel']]['cod_familiar'].nunique(),
        )

with st.container(border=True):

    st.subheader("Distribuição Geográfica das Pessoas Elegíveis")
    st.markdown("""
        O mapa abaixo mostra a distribuição geográfica das pessoas elegíveis ao programa, permitindo identificar as áreas com maior concentração de beneficiários.
    """)

    df_elegiveis = df_filtrado[df_filtrado['eligivel']]
    df_elegiveis = df_elegiveis.groupby('cdbairro')['count'].sum().reset_index()
    df_elegiveis = df_elegiveis[df_elegiveis['cdbairro'].notnull()]
    df_elegiveis['cdbairro'] = df_elegiveis['cdbairro'].astype(int)

    mapper_bairros = df_filtrado[['cdbairro', 'bairro_oficial']].drop_duplicates()
    df_elegiveis = df_elegiveis.merge(mapper_bairros, on='cdbairro', how='left')

    gdf.to_crs(epsg=4326, inplace=True)  # Certifique-se de que o GeoDataFrame está no CRS correto
    geojson = gdf.to_geo_dict()



    fig = px.choropleth_map(
        df_elegiveis,
        geojson=geojson,
        locations='cdbairro',                 # chave no seu DF
        featureidkey='properties.cdbairro',             # chave correspondente no GeoJSON
        color='count',
        color_continuous_scale="OrRd",
        zoom=11,
        center={"lat": -23.185, "lon": -46.897},  # centro aproximado de Jundiaí; ajuste se necessário
        opacity=0.8,
        labels={'count': 'Número de Pessoas'},
        hover_data={  # colunas extras no tooltip
        'bairro_oficial': True,
        'count': True,
        'cdbairro': False    # oculta o código se não quiser exibir
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    columns = st.columns(3)
    with columns[0]:
        st.subheader("Percentual de pessoas elegíveis")
        df_grouped_eligivel = (
            df_filtrado.groupby('elegivel_txt')['count']
            .sum()
            .reset_index()
        )
        fig = px.pie(
        df_grouped_eligivel,
        names="elegivel_txt",   # coluna de categorias
        values="count",         # valores
        hole=0.4,               # cria a "rosca" (0.4 é um bom tamanho)
        title="Distribuição por Elegibilidade"
        )
        st.plotly_chart(fig, use_container_width=True)

        columns_inside = st.columns(2)
        with columns_inside[0]:
            st.metric(
                label="Total de pessoas elegíveis",
                value=df_grouped_eligivel[df_grouped_eligivel['elegivel_txt'] == 'Sim']['count'].values[0],
            )
        with columns_inside[1]:
            st.metric(
                label="Total de pessoas não elegíveis",
                value=df_grouped_eligivel[df_grouped_eligivel['elegivel_txt'] == 'Não']['count'].values[0],
            )

    with columns[1]:
        st.subheader("Distribuição das pessoas por faixa de renda")
        df_grouped_renda = (
            df_filtrado.groupby('faixa_renda')['count']
            .sum()
            .reset_index()
        )
        fig = px.pie(
            df_grouped_renda,
            names="faixa_renda",   # coluna de categorias
            values="count",         # valores
            hole=0.4,               # cria a "rosca" (0.4 é um bom tamanho)
            title="Distribuição por Faixa de Renda"
        )
        fig.update_layout(
            legend_title_text='Faixa de Renda',
        )
        fig.update_traces(textposition='inside')  # coloca os rótulos dentro do gráfico
        fig.update_traces(textfont_size=12)  # tamanho da fonte dos rótulos
        fig.update_traces(hoverinfo="label+percent")  # mostra rótulo e porcentagem ao passar o mouse
        fig.update_layout(legend=dict(title="Faixa de Renda"))  # título da legenda


        fig.update_traces(textinfo="percent")  # mostra porcentagem e nome
        st.plotly_chart(fig, use_container_width=True)

    with columns[2]:
        st.subheader("Distribuição das pessoas por sexo")
        df_grouped_sexo = (
            df_filtrado.groupby('sexo')['count']
            .sum()
            .reset_index()
        )
        fig = px.pie(
            df_grouped_sexo,
            names="sexo",   # coluna de categorias
            values="count",         # valores
            hole=0.4,               # cria a "rosca" (0.4 é um bom tamanho)
            title="Distribuição por Sexo"
        )

        fig.update_traces(textinfo="percent+label")  # mostra porcentagem e nome
        st.plotly_chart(fig, use_container_width=True)


with st.container(border=True):
    columns = st.columns(2)

    with columns[0]:
        st.subheader("Distribuição da idade das pessoas")
        fig = px.histogram(
            df_filtrado,
            x='idade',
            nbins=50,
            title="Distribuição da Idade das Pessoas",
            labels={'idade': 'Idade', 'count' : 'Número de Pessoas'},
            color_discrete_sequence=["#656EEC"]
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with columns[1]:
        st.subheader("Distribuição da idade das pessoas por elegibilidade")

        fig = px.violin(
            df_filtrado,
            x="elegivel_txt",       
            y="idade",              
            box=True,               
            points="all",           
            color="elegivel_txt",   
            color_discrete_sequence=["#656EEC", "#F08A24"],  
            labels={
                "idade": "Idade",
                "elegivel_txt": "Elegibilidade"
            },
            title="Distribuição da Idade por Status de Elegibilidade"
        )

        st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):

    columns = st.columns(2)
    with columns[0]:
        st.subheader("Escolaridade do chefe da família - valores absolutos")

        chefes = df_filtrado[df_filtrado['parentesco'] == 'Pessoa Responsável Familiar']
        chefes= chefes[['escolaridade', 'elegivel_txt', 'count']]
        fig = px.bar(
            chefes.groupby(['escolaridade', 'elegivel_txt'])['count'].sum().reset_index(),
            x='escolaridade',
            y='count',
            color='elegivel_txt',
            title="Escolaridade do Chefe da Família",
            labels={'escolaridade': 'Escolaridade', 'count': 'Número de Pessoas'},
            color_discrete_sequence=["#656EEC", "#F08A24"],
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

    with columns[1]:
        st.subheader("Escolaridade do chefe da família - valores percentuais")

        escolaridade_selecionada = st.multiselect(
            "Selecione a escolaridade para comparação",
            options=chefes['escolaridade'].unique(),
            default=chefes['escolaridade'].unique()[0]
        )

        chefes = df_filtrado[df_filtrado['parentesco'] == 'Pessoa Responsável Familiar']
        chefes= chefes[['escolaridade', 'elegivel_txt', 'count']]
        chefes_escolaridade = chefes[chefes['escolaridade'].isin(escolaridade_selecionada)]
        total_elegivel = chefes[chefes['elegivel_txt'] == 'Sim']['count'].sum()
        total_nao_elegivel = chefes[chefes['elegivel_txt'] == 'Não']['count'].sum()
        percent_elegivel = (chefes_escolaridade[chefes_escolaridade['elegivel_txt'] == 'Sim']['count'].sum() / (total_elegivel)) * 100 
        percent_n_elegivel = (chefes_escolaridade[chefes_escolaridade['elegivel_txt'] == 'Não']['count'].sum() / (total_nao_elegivel)) * 100 

        dados = {
            'elegivel_txt': ['Sim', 'Não'],
            'percent': [percent_elegivel, percent_n_elegivel]
        }

        df_grafico = pd.DataFrame(dados)

        fig = px.pie(
            df_grafico,
            names="elegivel_txt",
            values="percent",
            hole=0.4,
            title="Distribuição por Elegibilidade (Chefes de Família)"
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)





st.subheader("📊 Detalhes dos dados para o mês selecionado")
st.write('### Total de pessoas selecionadas:', df_filtrado.shape[0],
         ' | Total de famílias:', df_filtrado['cod_familiar'].nunique())
with st.expander("Ver tabela completa"):
    st.dataframe(df_filtrado)




columns = st.columns(8)
with columns[7]:
    st.image('logo_cidade.jpg', width=100)