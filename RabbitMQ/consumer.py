import json
from Mongo.db_mongo import URI
import pika
from RabbitMQ.Models_RMQ import Contact
from mongoengine import connect

connect(host=URI)


def callback(ch, method, properties, body):
    contact_id = json.loads(body)['contact_id']
    contact = Contact.objects.get(id=contact_id)

    print(f"Sent email to {contact.fullname} at {contact.email}")

    contact.send_status = True
    contact.save()


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='contact_queue', durable=True)
    channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
