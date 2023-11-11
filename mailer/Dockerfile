FROM python:3.10
RUN mkdir /mailer
WORKDIR /mailer
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m pip install -U pydantic pydantic-extra-types pydantic-settings pydantic[email]
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
EXPOSE 8002