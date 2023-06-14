FROM python
WORKDIR /backend
COPY req.txt /backend
RUN python -m pip install -r req.txt

COPY . /backend
EXPOSE 8000

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
