from google.cloud import pubsub_v1
from crud import get_book_by_id
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
project_id = 'united-crane-423621-t9'
subscription_id = 'verification-rent-sub'
subscription_path = subscriber.subscription_path(project_id, subscription_id)
topic_path = publisher.topic_path(project_id, 'verification-book')

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def verify_book(id: int):
    db = SessionLocal()
    return get_book_by_id(db=db, book_id=id)

async def subscribe_to_topic_rent():

    def callback(message):
        id = message.data.decode('utf-8')
        print(f"Received message: {id} from rent provider")
        
        id = verify_book(int(id))
            
        response_message = "OK" if id else "ERROR"
        response_message = response_message.encode('utf-8')
        print(f"Sending message: {response_message}")
        publisher.publish(topic_path, data=response_message)
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for verification requests on {}'.format(subscription_path))
