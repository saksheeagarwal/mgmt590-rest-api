# Question-Answering API

In this project, the objective is to display the correct answer to a question asked by a user, using a given context. We are using pretrained models from [Hugging Face](https://huggingface.co/models?pipeline_tag=question-answering) to complete this task. In addition to answeing a question, the user is also able to input their model of choice to answer their question, delete a model, and view all available models. They can also view all previously answered questions filtered by the timestamp and model name.

## Routes

Path         | Method
------------- | -------------
/models  | GET, PUT, DELETE
/answer  | POST , GET

- **/models**
  - PUT - To input a model into the database in the 'models' table.
    - Expected Request body
    ```
    {
      "name": "bert-tiny",
      "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
      "model": "mrm8488/bert-tiny-5-finetuned-squadv2"
    }
    ```
    - Expected Response body
    ```
    [
      {
      "name": "bert-tiny",
      "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
      "model": "mrm8488/bert-tiny-5-finetuned-squadv2"
      },
      {
      "name": "deepset-roberta",
      "tokenizer": "deepset/roberta-base-squad2",
      "model": "deepset/roberta-base-squad2"
      }
    ]
    ```
   - GET - To view all available models.
      - Expected Response Body
      ```
      [
        {
        "name": "bert-tiny",
        "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
        "model": "mrm8488/bert-tiny-5-finetuned-squadv2"
        },
        {
        "name": "deepset-roberta",
        "tokenizer": "deepset/roberta-base-squad2",
        "model": "deepset/roberta-base-squad2"
        }
      ]
     ```
   - DELETE - To delete a model from the models table.
      - Expected Parameters
          - model - This is the model name you would like to use to answer the question
                  - Path format example : /models?model=deepset-roberta
      - Expected Response Body - updated list of available models
      ```
      [
        {
        "name": "distilled-bert",
        "tokenizer": "distilbert-base-uncased-distilled-squad",
        "model": "distilbert-base-uncased-distilled-squad"
        }
      ]
     ```
    
- **/answer**
  - POST - To input a question and context in order to get an answer using the given model.
    - Expected Request Body
    ```
    [
      {
      "name": "distilled-bert",
      "tokenizer": "distilbert-base-uncased-distilled-squad",
      "model": "distilbert-base-uncased-distilled-squad"
      },
      {
      "name": "deepset-roberta",
      "tokenizer": "deepset/roberta-base-squad2",
      "model": "deepset/roberta-base-squad2"
      }
    ]
    ```
    - Expected Response Body
    ```
    {
      "timestamp": 1621602784,
      "model": "deepset-roberta",
      "answer": "Leigh-Ann Galloway",
      "question": "who did holly matthews play in waterloo rd?",
      "context": "She attended the British drama school East 15 in 2005,
                  and left after winning a high-profile role in the BBC drama Waterloo
                  Road, playing the bully Leigh-Ann Galloway.[6] Since that role,
                  Matthews has continued to act in BBC's Doctors, playing Connie
                  Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and
                  she was back in the BBC soap Doctors in 2009, playing Tansy Flack."
    }
    ```
  - GET - To get all previously answered questions filtered by the model, start time and end time.
    - Expected Parameters : Path format example : /models?start=1621602784&end=1621708884&model=deepset-roberta
        - start (Required) - Start timestamp to display all answered question after that.
        - end (Required) - Ending timestamp to display all answered question before that.
        - model(optional) - This is the model name from huggingface you would like to use to answer the question
                
    - Expected Response Body
    ```
    [
      {
        "timestamp": 1621602930,
        "model": "distilled-bert",
        "answer": "Travis Pastrana",
        "question": "who did the first double backflip on a dirt bike?",
        "context": "2006 brought footage of Travis Pastrana completing a
        double backflip on an uphill/sand setup on his popular /"Nitro
        Circus/" Freestyle Motocross movies. On August 4, 2006, at X Games 12
        in Los Angeles, he became the first rider to land a double backflip
        in competition. Having landed another trick that many had considered
        impossible, he vowed never to do it again."
        }
    ]
    ```
    
## Dependencies
Dependencies need to be installed and are provided in the requirements.txt file. They can be installed using : pip install -r requirements.txt
- flask
- transformers
- torch

## How to build and run the API locally
  - Clone the repo into your local repository
 ```
  git clone <github-repo-name>
```
- Install the dependencies using the command:
```
pip install -r requirements.txt
```
- Execute the command to run the answer.py file
```
python3 answer.py
```
- Use the api link to hit the endpoints mentioned above via Postman.

## Running the API via remote GCP server
To run the pre-deployed code use the link https://finalssignment2-xiicktdcsq-uc.a.run.app on your web browser or Postman, to access the endpoints by appending the path to the given link.

    
    
    
      
