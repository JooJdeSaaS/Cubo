def calcular_cor_temperatura(temp):
    """Calcula a transição de cor de Azul (0°C) para Vermelho (40°C)."""
    t = max(0.0, min(float(temp), 40.0))
    fator = t / 40.0
    r = int(255 * fator)
    g = 0
    b = int(255 * (1.0 - fator))
    return f"#{r:02x}{g:02x}{b:02x}"


def card_sensor(titulo, valor, unidade, cor_borda, cor_texto=None):
    """Gera o HTML estruturado com CSS inline para um cartão de sensor."""
    if "🌡️ Temperatura" in titulo:
        cor_borda = calcular_cor_temperatura(valor)
    if not cor_texto:
        cor_texto = cor_borda
    return f"""
        <div style="background-color: #1e1e24; padding: 20px; border-radius: 10px; border-left: 5px solid {cor_borda}; margin-bottom: 15px;">
            <p style="color: #888888; margin: 0; font-size: 14px;">{titulo}</p>
            <h2 style="color: {cor_texto}; margin: 0; font-size: 32px;">{valor} <span style="font-size: 18px;">{unidade}</span></h2>
        </div>
    """


def exibir_alerta_qualidade_ar(pm25):
    """Retorna um banner HTML/CSS com a cor correspondente à classificação da OMS."""
    if pm25 <= 12.0:
        cor_fundo = "#155724"  # Verde escuro
        cor_texto = "#d4edda"
        status = "EXCELENTE"
        efeito = "O ar está limpo e seguro para todos."
    elif pm25 <= 35.4:
        cor_fundo = "#fff3cd"  # Amarelo suave
        cor_texto = "#856404"
        status = "MODERADO"
        efeito = "Aceitável. Pessoas extremamente sensíveis podem ter leves sintomas."
    elif pm25 <= 55.4:
        cor_fundo = "#DAA520"  # Laranja/Amarelo de atenção
        cor_texto = "#a75d00"
        status = "PREJUDICIAL PARA GRUPOS SENSÍVEIS"
        efeito = "Atenção: Idosos, crianças e asmáticos devem evitar esforço ao ar livre."
    elif pm25 <= 150.4:
        cor_fundo = "#721c24"  # Vermelho Alerta
        cor_texto = "#f8d7da"
        status = "PREJUDICIAL (INSALUBRE)"
        efeito = "Qualquer pessoa pode começar a sentir efeitos (tosse, irritação nos olhos)."
    elif pm25 <= 250.4:
        cor_fundo = "#4b1319"  # Roxo / Vinho Escuro
        cor_texto = "#f5c6cb"
        status = "MUITO PREJUDICIAL"
        efeito = "Alerta crítico de saúde. Efeitos colaterais severos para toda a população."
    else:
        cor_fundo = "#210306"  # Quase preto / Emergência
        cor_texto = "#ffccd5"
        status = "PERIGOSO (EMERGÊNCIA)"
        efeito = "Condição extrema de poluição. Evite qualquer atividade externa!"

    return f"""
        <div style="background-color: {cor_fundo}; color: {cor_texto}; padding: 15px; border-radius: 8px; border-left: 8px solid; font-family: sans-serif; margin-bottom: 25px;">
            <strong style="font-size: 16px;">⚠️ STATUS: {status} (PM2.5: {pm25} µg/m³)</strong>
            <p style="margin: 5px 0 0 0; font-size: 14px;">{efeito}</p>
        </div>
    """