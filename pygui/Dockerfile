# Slim version of Python
FROM python:3.8.12-slim

# Download Package Information
RUN apt-get update -y

# Install Tkinter
RUN apt-get install -y tk curl jq

RUN pip install pysimplegui

CMD ["/app/netapp_gui.py"]
ENTRYPOINT ["python3"]
