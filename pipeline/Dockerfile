FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY extract.py .
COPY transform.py .
COPY load.py .
COPY etl.py .

CMD [ "etl.lambda_handler" ]