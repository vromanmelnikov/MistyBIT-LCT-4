FROM python:3.10
RUN mkdir /api
WORKDIR /api
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install -U pydantic pydantic-extra-types pydantic-settings phonenumbers pydantic[email]
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000



