import streamlit as st  
import pandas as pd

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
    
    tab_data, tab_history,tab_share = exp2.tabs(["Tabela de Valores por Data", "Histórico", "Distribuição"])
    with tab_data:  
        st.dataframe(df_intituicao)
        
    with tab_history:
        st.line_chart(df_intituicao)
        
    with tab_share:
        date = st.date_input("Data para Distribuicão", 
                             min_value=df_intituicao.index.min(), 
                             max_value=df_intituicao.index.max())
        if date not in df_intituicao.index:
            st.warning("Data não disponível no conjunto de dados.")      
        else: 
            st.bar_chart(df_intituicao.loc[date])
    

    