FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY etl.py .
COPY extract.py .
COPY transform.py .
COPY load.py .

CMD [ "etl.lambda_handler" ]
