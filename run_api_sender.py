"""
Interpretação do Insight de Predição:
Positivo Alto	Aumenta drasticamente o risco de doença.
Negativo Alto	Diminui drasticamente o risco de doença (fator protetor).
Próximo a Zero	Tem pouco ou nenhum impacto no risco.
"""

import requests
import json
import time
import os
from dotenv import load_dotenv 


load_dotenv() 

from src.data_loader import load_and_preprocess_data
from src.ml_processor import generate_prediction_insight
from src.insight_generator import (
    generate_dashboard_insights, 
    generate_distributions_insights, 
    generate_correlations_insights, 
    generate_trends_placeholder
)

DATA_FILE_PATH = 'Heart_Disease_Prediction.csv'


ADMIN_TOKEN = os.getenv('ADMIN_TOKEN') 
API_URL = os.getenv('API_INSIGHTS_URL', 'http://localhost:5000/api/analytics/insights')


def send_insights_to_api(insights_list: list, token: str, api_url: str):
    """
    Função para enviar insights via POST.
    """
    if not token:
        print("ERRO: ADMIN_TOKEN não encontrado nas variáveis de ambiente. Abortando envio.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n--- Iniciando envio de {len(insights_list)} insights para a API ({api_url}) ---")
    
    for i, insight in enumerate(insights_list):
        try:
            payload = json.dumps(insight)
            response = requests.post(api_url, data=payload, headers=headers)
            response.raise_for_status() 
            
            print(f"Sucesso ({i+1}/{len(insights_list)}): '{insight.get('title', 'Sem Título')}' enviado. Status: {response.status_code}")
            time.sleep(0.1)
            
        except requests.exceptions.HTTPError as errh:
            print(f"Erro HTTP ({i+1}/{len(insights_list)}): Status: {response.status_code}. Título: {insight.get('title', 'N/A')}. Mensagem: {errh}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de Conexão ({i+1}/{len(insights_list)}): Título: {insight.get('title', 'N/A')}. Verifique se o servidor Node.js está rodando. Erro: {e}")

    print("--- Processo de envio de insights finalizado. ---")


def main():
    """ Orquestra a pipeline completa. """
    
    print("--- 1. INICIANDO O PIPELINE HEARTBEAT INSIGHTS ---")
    
    # 1. Carregamento e Pré-processamento
    df_original, df_eda = load_and_preprocess_data(DATA_FILE_PATH)
    
    if df_original is None:
        return

    all_insights = []
    
    # 2. Geração de Insights de Análise Exploratória (EDA)
    all_insights.extend(generate_dashboard_insights(df_eda))
    all_insights.extend(generate_distributions_insights(df_eda))
    all_insights.extend(generate_correlations_insights(df_eda))
    all_insights.extend(generate_trends_placeholder())
    
    # 3. Geração do Insight de Machine Learning
    ml_insight = generate_prediction_insight(df_original)
    all_insights.append(ml_insight)
    
    print(f"\nTotal de insights gerados: {len(all_insights)}")
    
    # 4. Envio para a API
    send_insights_to_api(all_insights, ADMIN_TOKEN, API_URL)


if __name__ == '__main__':
    main()