
import streamlit as st  
import pandas as pd

def cal_general_stats(df: pd.DataFrame):
    df_data = df.groupby(by = "Data").sum()[["Valor"]].reset_index()
    df_data["lag_1"] = df_data["Valor"].shift(1)
    df_data["Diferença Mensal"] = df_data["Valor"] - df_data["lag_1"]
    df_data["Média Móvel 6 meses"] = df_data["Diferença Mensal"].rolling(window=6).mean()
    df_data["Média Móvel 12 meses"] = df_data["Diferença Mensal"].rolling(window=12).mean()
    df_data["Média Móvel 24 meses"] = df_data["Diferença Mensal"].rolling(window=24).mean()
    df_data["Evolucão 6 meses Total"] = df_data["Valor"].rolling(window=6).apply(lambda x: (x.iloc[-1] - x.iloc[0]))
    df_data["Evolucão 12 meses Total"] = df_data["Valor"].rolling(window=12).apply(lambda x: (x.iloc[-1] - x.iloc[0]))
    df_data["Evolucão 24 meses Total"] = df_data["Valor"].rolling(window=24).apply(lambda x: (x.iloc[-1] - x.iloc[0]))
    df_data["Evolucão 6 meses Relativa"] = df_data["Valor"].rolling(window=6).apply(lambda x: (x.iloc[-1] / x.iloc[0])) 
    df_data["Evolucão 12 meses Relativa"] = df_data["Valor"].rolling(window=12).apply(lambda x: (x.iloc[-1] / x.iloc[0])) 
    df_data["Evolucão 24 meses Relativa"] = df_data["Valor"].rolling(window=24).apply(lambda x: (x.iloc[-1] / x.iloc[0]))  
    df_data["Diferenca Mensal Relativa"] = df_data["Valor"]/df_data["lag_1"] - 1
    
    df_data = df_data.drop(columns=["lag_1"])
    
    return df_data


st.set_page_config(page_title="Financas App", page_icon="💰")

st.text ("Hello, World!")

st.markdown ("# Welcome to the Financas App")

# Widget de upload de dados 
file_upload = st.file_uploader(label="Upload your financial data here", type=["csv"])

# Verifica se algum arquivo foi carregado
if file_upload:
    
    # Lê o arquivo CSV em um DataFrame
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date
    
    exp1 = st.expander("Dados Brutos")
    
    
    # Exibe o DataFrame na aplicação Streamlit
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)
    
    # Não mostra arquivo carregado
    st.success("File uploaded successfully!")
    
    
    # Visão geral dos valores por instituição
    exp2 = st.expander("Visão Geral por Instituição")
    df_intituicao = df.pivot_table(index='Data', values='Valor', columns='Instituição')
    
    # Cria abas dentro do expander
    tab_data, tab_history,tab_share = exp2.tabs(["Tabela de Valores por Data", "Histórico", "Distribuição"])
    
    # Exibe o DataFrame em cada aba
    with tab_data:  
        st.dataframe(df_intituicao)
    
    # Exibe o gráfico de linha no aba de histórico
    with tab_history:
        st.line_chart(df_intituicao)
        
    # Exibe o gráfico de barras na aba de distribuição
    with tab_share:
        date = st.date_input("Data para Distribuicão", 
                             min_value=df_intituicao.index.min(), 
                             max_value=df_intituicao.index.max())
        if date not in df_intituicao.index:
            st.warning("Data não disponível no conjunto de dados.")      
        else: 
            st.bar_chart(df_intituicao.loc[date])
    
    exp3 = st.expander("Estatísticas Gerais")

    df_stats = cal_general_stats(df)

    columns_config = {
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "Diferença Mensal": st.column_config.NumberColumn("Diferença Mensal", format="R$ %.2f"),
        "Média Móvel 6 meses": st.column_config.NumberColumn("Média Móvel 6 meses", format="R$ %.2f"),
        "Média Móvel 12 meses": st.column_config.NumberColumn("Média Móvel 12 meses", format="R$ %.2f"),
        "Média Móvel 24 meses": st.column_config.NumberColumn("Média Móvel 24 meses", format="R$ %.2f"),
        "Evolucão 6 meses Total": st.column_config.NumberColumn("Evolucão 6 meses Total", format="R$ %.2f"),
        "Evolucão 12 meses Total": st.column_config.NumberColumn("Evolucão 12 meses Total", format="R$ %.2f"), 
        "Evolucão 24 meses Total": st.column_config.NumberColumn("Evolucão 24 meses Total", format="R$ %.2f"), 
        "Diferenca Mensal Relativa": st.column_config.NumberColumn("Diferenca Mensal Relativa", format="percent"),
        "Evolucão 6 meses Relativa": st.column_config.NumberColumn("Evolucão 6 meses Relativa", format="percent"),
        "Evolucão 12 meses Relativa": st.column_config.NumberColumn("Evolucão 12 meses Relativa", format="percent"),
        "Evolucão 24 meses Relativa": st.column_config.NumberColumn("Evolucão 24 meses Relativa", format="percent")
        }   


    tab_abs, tab_stats, tab_rel = exp3.tabs(["Dados", "Histórico de Evolucão", "Crescimento Relativo"]) 

    with tab_abs:
         st.dataframe(df_stats, column_config=columns_config, hide_index=True)


    with tab_stats:
        abs_cols = ["Diferença Mensal",  
                    "Média Móvel 6 meses", 
                    "Média Móvel 12 meses", 
                    "Média Móvel 24 meses"
                 ]
        st.line_chart(df_stats.set_index("Data")[abs_cols])


    with tab_rel:
        rel_cols = ["Diferenca Mensal Relativa",
                 "Evolucão 6 meses Relativa",
                 "Evolucão 12 meses Relativa",
                 "Evolucão 24 meses Relativa"  
                 ]
        st.line_chart(df_stats.set_index("Data")[rel_cols])
    

    with st.expander("Metas"):
        
        col1, col2 = st.columns(2)
        data_inicio_meta = col1.date_input("Início da Meta", max_value=df_stats["Data"].max())
        filter_data = df_stats["Data"] <= data_inicio_meta
        data_filtrada = df_stats.loc[filter_data]["Data"].iloc[-1] if not filter_data.empty else df_stats["Data"].min()
        valor_inicio = df_stats.loc[df_stats["Data"] == data_filtrada, "Valor"]
        st.markdown("**Valor no Início da Meta:** R$ %.2f" % float(valor_inicio))
      
        salario_bruto = col1.number_input("Salário Bruto Mensal (R$)", min_value=0.0, value=5000.0, step=100.0, format="%.2f")
        salario_liquido = col2.number_input("Salário Líquido Mensal (R$)", min_value=0.0, value=3500.0, step=100.0, format="%.2f")
        custos_fixos = col2.number_input("Custos Fixos Mensais (R$)", min_value=0.0, value=2000.0, step=100.0, format="%.2f")

        col1_pot, col2_pot = st.columns(2)
        mensal = salario_liquido - custos_fixos
        anual = mensal * 12
        with col1_pot.container(border=True):
            st.markdown("**Potencial de Investimento Mensal:** \n\n R$ %.2f" % mensal)
        with col2_pot.container(border=True):
            st.markdown("**Potencial de Investimento Anual:** \n\n R$ %.2f" % anual)
        
        col1_meta, col2_meta = st.columns(2)
        
        with col1_meta.container(border=True):
            st.number_input("Meta Financeira (R$)", min_value=float(valor_inicio), value=float(anual), step=1000.0, format="%.2f")
        with col2_meta.container(border=True):
            st.markdown("Patrimônio estimado em 1 Ano (R$): \n\n R$ %.2f" % (float(valor_inicio) + anual))