from flask import Flask
from flask import render_template
from flask import request
import sys
import time
import json
import os
import dialogflow

try:
    fp = open('.env', 'r', encoding='utf8')
except Exception as e:
    print('加载失败，.env文件不存在')
    raise Exception(e)
lines = fp.readlines()
# print(lines)
os.environ['DIALOGFLOW_PROJECT_ID'] = lines[1][:-1]  # 加载DIALOGFLOW_PROJECT_ID
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = lines[3]  # 加载GOOGLE_APPLICATION_CREDENTIALS
fp.close()

project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

app = Flask(__name__)


def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

print('============ chatbot imported ==========')


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversaion."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text


def ans(query):
    start = time.time()
    fulfillment_text = detect_intent_texts(project_id, "unique", query, 'en')
    response_text = {"message": fulfillment_text}

    end = time.time()
    print('[LOG INFO] parse time:', end-start)
    return json.dumps(response_text)


@app.route('/query/<query>')
def QA(query):
    # if request.method == 'POST':
    #     answer = ans(request.form['query'])
        # print ('query --------------------', request.form['query'])
        # return render_template('qa.html', **answer)
    #     return answer
    if request.method == 'GET':
        answer = ans(query)
        return answer
    else:
        return 'hello world'

if __name__ == '__main__':
    # implicit()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    # while(1):
    #     txt = input()
    #     fulfillment_text = detect_intent_texts(project_id, "unique", txt, 'en')
    #     print(fulfillment_text)
