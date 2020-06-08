import smtplib
import pika
import time
import json
smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
smtpObj.starttls()
smtpObj.login('khasanova8@mail.ru','pass_for_rv')

def callback(ch, method, properties, data):
    body = json.loads(data)
    email = body['email']
    message = body['message']
    print(email, message, flush=True)
    smtpObj.sendmail("khasanova8@mail.ru", email, message)


while(1):
    try:
        credentials = pika.PlainCredentials('user', 'user')
        parameters = pika.ConnectionParameters('rabbitmq',
                                               5672,
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
    except Exception as e:
        time.sleep(1)
        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        smtpObj.starttls()
        smtpObj.login('khasanova8@mail.ru', 'pass_for_rv')
