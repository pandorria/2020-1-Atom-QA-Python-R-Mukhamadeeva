FROM python:3.8

ADD mock_vk_api.py /

RUN pip install vk
RUN pip install flask

CMD [ "python", "./mock_vk_api.py" ]