import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- CONFIGURAÇÃO ---
ARQUIVO_BANCO = 'input_extrato_banco.csv'
ARQUIVO_SISTEMA = 'input_razao_contabil.csv'
ARQUIVO_RELATORIO = 'Relatorio_Auditoria_Divergencias.xlsx'

def gerar_dados_ficticios():
    """Gera massa de dados para teste (Mock Data) se os arquivos não existirem."""
    print("🛠️ Gerando dados simulados para demonstração...")
    
    # Cenário: Extrato Bancário (A Realidade)
    dados_banco = {
        'Data': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05', '2023-10-06'],
        'Descricao': ['Pgto Fornecedor A', 'Recebimento Cliente X', 'Tarifa Bancaria', 'Pgto Aluguel', 'TED Recebida', 'Pgto Software'],
        'Valor': [-1500.00, 5000.00, -45.90, -2000.00, 10000.00, -150.00],
        'ID_Transacao': ['TX001', 'TX002', 'TX003', 'TX004', 'TX005', 'TX006']
    }
    
    # Cenário: Razão Contábil (O Registro Humano - Com Falhas)
    # Erro 1: Omissão (Esqueceu a tarifa TX003)
    # Erro 2: Divergência (Aluguel TX004 lançado errado: -200 em vez de -2000)
    # Erro 3: Fantasma (Lançou TX999 que não existe no banco)
    dados_sistema = {
        'Data_Lancamento': ['2023-10-01', '2023-10-02', '2023-10-04', '2023-10-05', '2023-10-06'],
        'Historico': ['Pgto Fornecedor A', 'Recebimento Cliente X', 'Pgto Aluguel', 'TED Recebida', 'Pgto Fantasma'],
        'Valor_Lancado': [-1500.00, 5000.00, -200.00, 10000.00, -500.00], 
        'ID_Referencia': ['TX001', 'TX002', 'TX004', 'TX005', 'TX999']
    }
    
    pd.DataFrame(dados_banco).to_csv(ARQUIVO_BANCO, index=False)
    pd.DataFrame(dados_sistema).to_csv(ARQUIVO_SISTEMA, index=False)
    print("✅ Arquivos de entrada (CSV) gerados.")

def auditar_contas():
    if not os.path.exists(ARQUIVO_BANCO):
        gerar_dados_ficticios()
        
    print("\n🔍 Iniciando Cruzamento de Dados (Auditoria)...")
    
    # 1. Ingestão de Dados
    try:
        df_banco = pd.read_csv(ARQUIVO_BANCO)
        df_sistema = pd.read_csv(ARQUIVO_SISTEMA)
    except FileNotFoundError:
        print("❌ Erro: Arquivos de entrada não encontrados.")
        return

    # Tipagem forte para garantir precisão decimal
    df_banco['Valor'] = df_banco['Valor'].astype(float)
    df_sistema['Valor_Lancado'] = df_sistema['Valor_Lancado'].astype(float)
    
    # 2. Motor de Reconciliação (Full Outer Join)
    df_audit = pd.merge(
        df_banco, 
        df_sistema, 
        left_on='ID_Transacao', 
        right_on='ID_Referencia', 
        how='outer',
        indicator=True
    )
    
    divergencias = []
    
    # 3. Regras de Auditoria (Business Logic)
    for index, row in df_audit.iterrows():
        status = "OK"
        detalhe = "Conciliado"
        acao = "-"
        
        # Regra 1: Omissão (Está no Banco, não no Sistema)
        if row['_merge'] == 'left_only':
            status = "OMISSÃO CONTÁBIL"
            detalhe = f"Transação {row['ID_Transacao']} ({row['Descricao']}) não foi lançada."
            acao = "Lançar no sistema."
            
        # Regra 2: Sem Lastro (Está no Sistema, não no Banco)
        elif row['_merge'] == 'right_only':
            status = "SEM LASTRO FINANCEIRO"
            detalhe = f"Lançamento {row['ID_Referencia']} ({row['Historico']}) não consta no extrato."
            acao = "Verificar comprovante/estorno."
            
        # Regra 3: Divergência de Valor
        elif row['_merge'] == 'both':
            diff = row['Valor'] - row['Valor_Lancado']
            if abs(diff) > 0.01:
                status = "DIVERGÊNCIA DE VALOR"
                detalhe = f"Diferença de {diff:.2f}. Banco: {row['Valor']} | Sistema: {row['Valor_Lancado']}"
                acao = "Corrigir valor."

        if status != "OK":
            divergencias.append({
                'ID': row['ID_Transacao'] if pd.notna(row['ID_Transacao']) else row['ID_Referencia'],
                'Data': row['Data'] if pd.notna(row['Data']) else row['Data_Lancamento'],
                'Descricao': row['Descricao'] if pd.notna(row['Descricao']) else row['Historico'],
                'Valor_Banco': row['Valor'],
                'Valor_Sistema': row['Valor_Lancado'],
                'Status_Auditoria': status,
                'Analise_IA': detalhe, # Placeholder para futuro uso de IA
                'Recomendacao': acao
            })

    # 4. Geração de Relatório Executivo
    if divergencias:
        df_resultado = pd.DataFrame(divergencias)
        print(f"🚨 DIVERGÊNCIAS ENCONTRADAS: {len(df_resultado)}")
        print(df_resultado[['Status_Auditoria', 'Valor_Banco', 'Valor_Sistema']].to_string(index=False))
        
        # Salva Excel formatado
        df_resultado.to_excel(ARQUIVO_RELATORIO, index=False)
        print(f"\n📂 Relatório de Auditoria salvo em: {os.path.abspath(ARQUIVO_RELATORIO)}")
    else:
        print("✅ Sucesso: Nenhuma divergência encontrada. Contas conciliadas.")

if __name__ == "__main__":
    auditar_contas()