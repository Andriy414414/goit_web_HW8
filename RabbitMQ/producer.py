from Mongo.db_mongo import URI
from mongoengine import connect
from RabbitMQ.Models_RMQ import Contact
from faker import Faker
import json
import pika

fake = Faker('uk-UA')
connect(host=URI)

NUMBER_CONTACTS = 10


def create_contact():
    return {
        "fullname": fake.name(),
        "email": fake.email()
    }


def publish_message(channel, body):
    channel.basic_publish(
        exchange='',
        routing_key='contact_queue',
        body=json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='contact_queue', durable=True)

    for _ in range(NUMBER_CONTACTS):
        contact_data = create_contact()
        contact = Contact(**contact_data).save()
        publish_message(channel, {'contact_id': str(contact.id)})

    connection.close()


if __name__ == '__main__':
    main()
