from flask import Flask, request, render_template
import openai
import json  # Import necessário para manipular o arquivo JSON

app = Flask(__name__)

# Configuração da API OpenAI
openai.api_key = "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"

# Carregar os dados dos clientes
with open("clientes.json", "r") as f:
    clientes = json.load(f)


@app.route("/")
def home():
    return render_template("form.html")  # Renderiza o formulário


@app.route("/generate", methods=["POST"])
def generate():
    cliente_id = request.form["cliente_id"]  # Exemplo: "incitat" ou "tag"
    lead_name = request.form["contato"]
    company_name = request.form["company"]
    dados = request.form["dados"]  # Informações adicionais

    cliente = clientes.get(cliente_id, {})
    if not cliente:
        return "<h1>Erro:</h1><p>Cliente não encontrado.</p>"

    # Texto do system e criação do prompt
    system_text = cliente["texto_system"]
    prompt = f"""
    Crie uma mensagem personalizada de vendas para o seguinte lead:
    - Nome do contato: {lead_name}
    - Empresa: {company_name}
    - Informações adicionais: {dados}
    - Serviços oferecidos: {cliente['servicos']}
    - Diferenciais: {cliente['diferenciais']}
    - Objetivo: {cliente['objetivo']}

    Sua tarefa:
    1. Analise as informações fornecidas sobre o lead e utilize-as para criar uma conexão genuína.
    2. Destaque como os serviços de {cliente['nome']} podem resolver os desafios ou aproveitar as oportunidades do lead.
    3. Use uma linguagem profissional, amigável e personalizada, que demonstre empatia com o perfil do contato.
    4. Inclua elementos do perfil do LinkedIn, como conquistas ou desafios mencionados, para tornar a mensagem única.
    5. A mensagem deve ser objetiva e focada no objetivo de agendar uma reunião. Evite redundâncias e seja direto ao ponto.
    6. Você é um assistente especializado em criar mensagens de vendas personalizadas. Sempre seja objetivo e direto, focando no agendamento de uma reunião com o lead. Limite suas respostas a mensagens curtas e impactantes.
    7. Evite usar palavras como "seria", "poderia", trocar por "quero que você tenha a oportunidade de avaliar" ou "você está aberto a uma oportunidade de avaliar"
    8. Evitar mensagens genéricas, clichês ou jargões como "no que tange".
    9. Finalizar com um convite claro para uma conversa.
    """

    try:
        response = openai.ChatCompletion.create(model="gpt-4",
                                                messages=[{
                                                    "role":
                                                    "system",
                                                    "content":
                                                    system_text
                                                }, {
                                                    "role": "user",
                                                    "content": prompt
                                                }],
                                                max_tokens=350,
                                                temperature=0.9)

        suggestion = response["choices"][0]["message"]["content"].strip()
        return f"<h1>Sugestão de abordagem:</h1><p>{suggestion}</p>"

    except Exception as e:
        return f"<h1>Erro:</h1><p>{e}</p>"


if __name__ == "__main__":
    app.run(debug=True)
