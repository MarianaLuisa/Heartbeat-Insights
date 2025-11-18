# src/ml_processor.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import json

NUMERIC_FEATURES = ['Age', 'BP', 'Cholesterol', 'MaxHR', 'Oldpeak']
CATEGORICAL_FEATURES = ['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExAngina', 'ST_Slope', 'NumVessels', 'Thallium']
TARGET_COLUMN = 'Target'


def get_ml_pipeline():
    """ Define e retorna o Pipeline de Pré-processamento e Modelo de ML. """
    
    # 1. Pré-processamento para Dados Numéricos (Normalização)
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

    # 2. Pré-processamento para Dados Categóricos (One-Hot Encoding)
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # 3. Combinar os transformadores (ColumnTransformer)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ],
        remainder='drop' 
    )

    # 4. Criar o Pipeline final com o modelo (Regressão Logística)
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42)) 
    ])
    
    return model

def generate_prediction_insight(df_original: pd.DataFrame):
    """
    Treina o modelo ML e gera o insight de 'predictions' (Importância das Features).
    """
    if df_original is None:
        return {}

    # 1. Preparação dos dados para ML
    X = df_original.drop(TARGET_COLUMN, axis=1)
    # Converter o alvo para binário: Presence=1, Absence=0
    y = df_original[TARGET_COLUMN].map({'Absence': 0, 'Presence': 1})

    # 2. Treinamento
    model = get_ml_pipeline()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    
    # 3. Extração da Importância das Features (Coeficientes)
    onehot_encoder = model.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
    cat_features_out = onehot_encoder.get_feature_names_out(CATEGORICAL_FEATURES)
    all_feature_names = np.concatenate([NUMERIC_FEATURES, cat_features_out])

    # Obtém coeficientes do modelo
    coeficientes = model.named_steps['classifier'].coef_[0]

    # Cria DataFrame de importância para ordenação
    df_importance = pd.DataFrame({'feature': all_feature_names, 'importance': coeficientes})
    df_importance = df_importance.sort_values(by='importance', ascending=False)
    
    # 4. Formatação do Insight JSON (Categoria 'predictions')
    # IDEIA CLÍNICA: Mostrar o peso (coeficiente) de cada fator no risco.
    insight_predicao = {
        "title": "Fatores Preditivos de Doença Cardíaca (Modelo ML)",
        "category": "predictions",
        "chartType": "bar_horizontal",
        "chartData": {
            "labels": df_importance['feature'].head(10).tolist(), # Top 10 fatores
            "datasets": [{
                "label": "Importância (Coeficiente)",
                "data": df_importance['importance'].head(10).tolist()
            }]
        },
        "statistics": {
            "modelo_usado": "Regressão Logística",
            "acuracia_teste": f"{accuracy:.2f}",
            "feature_mais_positiva": df_importance.iloc[0].to_dict(), # Mais aumenta o risco
            "feature_mais_negativa": df_importance.iloc[-1].to_dict() # Mais diminui o risco
        }
    }
    
    print("Insight 'predictions' gerado.")
    return insight_predicao

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    df_orig, _ = load_and_preprocess_data('Heart_Disease_Prediction.csv')
    if df_orig is not None:
        insight = generate_prediction_insight(df_orig)
        print("\n--- Insight Predictions JSON ---")
        print(json.dumps(insight, indent=4))