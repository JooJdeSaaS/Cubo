from google import genai

class AssistenteCubo:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = None
        self._iniciar_cliente()

    def _iniciar_cliente(self):
        if self.api_key and self.api_key != "SUA_CHAVE_API_AQUI":
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Erro ao iniciar cliente Gemini: {e}")

    def analisar_condicoes(self, pergunta, temp, umid, pm25, co):
        if not self.client:
            return "Erro: Chave API do Gemini não configurada ou inválida."

        prompt = f"""
        Você é o assistente inteligente do projeto 'O Cubo', uma estação de monitoramento ambiental.
        Os dados atuais medidos pelos sensores agora são:
        - Temperatura: {temp}°C
        - Umidade Relativa do Ar: {umid}%
        - Material Particulado (PM2.5): {pm25} µg/m³
        - Monóxido de Carbono (CO): {co} ppm

        O usuário fez a seguinte pergunta: "{pergunta}"

        Responda de forma breve, direta e amigável, avaliando se a atividade descrita é recomendada ou não com base estritamente nesses números acima.
        """

        try:
            # Correção do modelo para o motor estável atualizado
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Erro ao consultar a IA: {e}"