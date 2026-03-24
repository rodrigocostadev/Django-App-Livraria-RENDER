from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

def get_book_ai_description(title):
    print("####### RODOU get_book_ai_description #########")

    message= """
    Faça a descrição de venda para o livro {} em apenas 500 caracteres contendo um breve resumo sobre ele e o nome do autor. 
    """

    message = message.format(title)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message
             },
        ],
        model='gpt-3.5-turbo',  # ou 'gpt-4' se preferir        
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content # O response vai ser um JSON, a chave de acesso ao valor da resposta é choices, e 0 para pegar o primeiro valor


def get_book_ai_year(title):
    print("####### RODOU get_book_ai_year #########")

    message= """
    Informe somente o ano de lançamento do livro {} em no máximo 5 caracteres sem nenhuma pontuação. 
    """

    message = message.format(title)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message
             },
        ],
        model='gpt-3.5-turbo',  # ou 'gpt-4' se preferir        
        max_tokens=10,
        temperature=0.1,
    )
    return response.choices[0].message.content # O response vai ser um JSON, a chave de acesso ao valor da resposta é choices, e 0 para pegar o primeiro valor
