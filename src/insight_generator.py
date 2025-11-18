# src/insight_generator.py
import pandas as pd

def generate_dashboard_insights(df_eda: pd.DataFrame):
    """ Gera insights da categoria 'dashboard'. """
    if df_eda is None: return []
    insights = []

    # IDEIA CLÍNICA: Taxa de prevalência e idade média dos pacientes de risco.
    doenca_presente = df_eda[df_eda['Target_Desc'] == 'Com Doença Cardíaca']
    risco_geral = (len(doenca_presente) / len(df_eda)) * 100
    
    insights.append({
        "title": "Taxa de Prevalência de Doença Cardíaca",
        "category": "dashboard",
        "statistics": {
            "prevalencia_amostra": f"{risco_geral:.1f}%",
            "idade_media_diagnostico": f"{doenca_presente['Age'].mean():.1f} anos",
            "total_pacientes": len(df_eda)
        }
    })

    # IDEIA CLÍNICA: Prevalência de Doença Cardíaca em Pacientes com Glicemia Alta (FBS).
    risco_por_fbs = df_eda.groupby('FastingBS_Desc')['Target'].value_counts(normalize=True).mul(100).unstack().fillna(0)

    insights.append({
        "title": "Risco de Doença por Glicemia em Jejum (FBS)",
        "category": "dashboard",
        "statistics": {
            "prevalencia_fbs_elevado": f"{risco_por_fbs.loc['Jejum Açúcar > 120 mg/dl', 'Presence']:.1f}%",
            "prevalencia_fbs_normal": f"{risco_por_fbs.loc['Jejum Açúcar <= 120 mg/dl', 'Presence']:.1f}%"
        }
    })
    
    print("Insights 'dashboard' gerados.")
    return insights

def generate_distributions_insights(df_eda: pd.DataFrame):
    """ Gera insights da categoria 'distributions'. """
    if df_eda is None: return []
    insights = []

    # IDEIA CLÍNICA: A dor 'Assintomática' é a mais perigosa.
    doentes_por_dor = df_eda[df_eda['Target_Desc'] == 'Com Doença Cardíaca']['ChestPainType_Desc'].value_counts()
    total_doentes = doentes_por_dor.sum()

    insights.append({
        "title": "Tipo de Dor Mais Comum em Pacientes Cardíacos",
        "category": "distributions",
        "chartData": {
            "labels": doentes_por_dor.index.tolist(),
            "datasets": [{
                "label": "% dos Pacientes Cardíacos",
                "data": (doentes_por_dor / total_doentes * 100).round(1).tolist()
            }]
        },
        "statistics": {
            "insight_principal": f"A dor mais prevalente é a '{doentes_por_dor.index[0]}' ({round(doentes_por_dor.iloc[0]/total_doentes * 100, 1)}%)"
        }
    })

    print("Insights 'distributions' gerados.")
    return insights

def generate_correlations_insights(df_eda: pd.DataFrame):
    """ Gera insights da categoria 'correlations'. """
    if df_eda is None: return []
    insights = []

    # IDEIA CLÍNICA: Avaliar se a MaxHR está baixa para a idade, sugerindo baixa capacidade.
    scatter_data_doente = df_eda[df_eda['Target_Desc'] == 'Com Doença Cardíaca'][['Age', 'MaxHR']].to_dict('records')
    scatter_data_saudavel = df_eda[df_eda['Target_Desc'] == 'Sem Doença Cardíaca'][['Age', 'MaxHR']].to_dict('records')

    insights.append({
        "title": "Relação Idade vs. Frequência Cardíaca Máxima (MaxHR)",
        "category": "correlations",
        "chartData": {
            "datasets": [
                {"label": "Com Doença", "data": [{"x": p['Age'], "y": p['MaxHR']} for p in scatter_data_doente]},
                {"label": "Sem Doença", "data": [{"x": p['Age'], "y": p['MaxHR']} for p in scatter_data_saudavel]}
            ]
        },
        "statistics": {
            "corr_geral": f"{df_eda['Age'].corr(df_eda['MaxHR']):.3f}",
            "observacao": "Esperada correlação negativa. MaxHR de doentes geralmente fica abaixo da curva esperada para a idade."
        }
    })
    
    print("Insights 'correlations' gerados.")
    return insights

def generate_trends_placeholder():
    """ Gera o placeholder para a categoria 'trends'. """
    # IDEIA CLÍNICA: Placeholder para futura análise temporal.
    return [{
        "title": "Placeholder: Tendência de Risco (Requer Dados Temporais)",
        "category": "trends",
        "chartData": {"message": "Dados temporais não disponíveis no dataset atual."},
        "statistics": {"status": "Aguardando dados com carimbo de tempo (timestamp) para análise."}
    }]