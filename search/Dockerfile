FROM python:3.13.2

ENV PROJECT_ROOT=.
# Set up working directiory
RUN mkdir -p /opt/search
WORKDIR /opt/search/
EXPOSE 8588
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD scripts ${PROJECT_ROOT}
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9012"]
CMD ["python", "api_server.py"]
