import openai
import os
import configobj


def get_api_key():
    config = configobj.ConfigObj('.env')
    return config['OPENAI_API_KEY']


if __name__ == '__main__':
    openai.api_key = get_api_key()
    response = openai.Completion.create(model='text-davinci-002', prompt="Say this is a test", temperature=0,
                                        max_tokens=6)
    print(response)
