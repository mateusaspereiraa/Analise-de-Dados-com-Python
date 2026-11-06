"""Análise de cancelamentos (versão em script do notebook).
Roda os 5 passos, imprime os resultados e gera relatorio.html com gráficos (se plotly estiver instalado).
Uso: python analise_melhorada.py [cancelamentos.csv]
"""
import sys
import pandas as pd

arq = sys.argv[1] if len(sys.argv) > 1 else "cancelamentos.csv"
tabela = pd.read_csv(arq)                                       # 1. importar
tabela = tabela.drop(columns="CustomerID", errors="ignore")      # 2. remover coluna inútil
antes = len(tabela)
tabela = tabela.dropna()                                         # 3. corrigir vazios
print(f"{antes} linhas, {antes - len(tabela)} vazias removidas, {len(tabela)} na análise")

taxa = tabela["cancelou"].mean()                                 # 4. quantos cancelaram
print(f"Cancelaram: {int(tabela['cancelou'].sum())} ({taxa:.1%})")

print("\nTaxa de cancelamento por contrato:")                     # 5. causas
print(tabela.groupby("duracao_contrato")["cancelou"].mean().map("{:.1%}".format).to_string())
print(f"Mais de 4 ligações: {tabela[tabela.ligacoes_callcenter > 4]['cancelou'].mean():.1%}")
print(f"Atraso acima de 20 dias: {tabela[tabela.dias_atraso > 20]['cancelou'].mean():.1%}")

filtrada = tabela[(tabela.duracao_contrato != "Monthly") & (tabela.ligacoes_callcenter <= 4) & (tabela.dias_atraso <= 20)]
print(f"\nCom as regras de retenção: {len(filtrada)} clientes, taxa {filtrada['cancelou'].mean():.1%}")

try:
    import plotly.express as px
    with open("relatorio.html", "w", encoding="utf-8") as f:
        for col in tabela.columns.drop("cancelou"):
            f.write(px.histogram(tabela, x=col, color="cancelou", title=col).to_html(full_html=False, include_plotlyjs="cdn"))
    print("Gráficos salvos em relatorio.html")
except ImportError:
    print("(instale plotly para gerar os gráficos: pip install plotly)")
