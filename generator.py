import json
import openai
openai.api_key = 'Your api key'


def generate_test(question):
    while True:
        ask = f"""Write a question about {question} with 3 possible answers, 1 of which is correct and 2 are incorrect, according to the template:
          Question
          # Correct answer
          # Incorrect answer
          # Incorrect answer"""

        response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=ask,
                    temperature=1,
                    max_tokens=400
                )
        dict_response = response.to_dict()
        print(dict_response['choices'][0])
        result = json.loads(str(dict_response['choices'][0]))['text'].strip()
        if len(result.split('#')) == 4:
            break
    test = {}
    test['question'] = result.split('#')[0].strip()
    test['answer'] = result.split('#')[1].strip()
    test['var1'] = result.split('#')[2].strip()
    test['var2'] = result.split('#')[3].strip()
    print('test: ', test)
    return test


def generate_long_answer(question):
    ask = f"""{question}"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=ask,
        temperature=1,
        max_tokens=1000
    )
    dict_response = response.to_dict()
    print(dict_response['choices'][0])
    result = json.loads(str(dict_response['choices'][0]))['text'].strip()

    return result


def generate_parts(question):
    ask = f"""print theme {question} subfields"""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=ask,
        temperature=1,
        max_tokens=1000
    )
    dict_response = response.to_dict()
    print(dict_response['choices'][0])
    result = json.loads(str(dict_response['choices'][0]))['text'].strip()
    result = result.replace('\n\n', '\n')

    return result.split('\n')

