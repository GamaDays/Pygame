#Openai Setup

import openai
openai.api_key = '' #Key removed for security reasons

def Call_GPT(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    )

    # Extract and print the generated answer
    answer = response['choices'][0]['message']['content'].strip()
    return answer


