from google.cloud import pubsub_v1
import asyncio

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('united-crane-423621-t9', 'verification')

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('united-crane-423621-t9', 'verification-response')


def request_verification(token: str):
    # Initialize Pub/ clien    
    message = token.encode('utf-8')
    print(f"Sending message: {message}")
    future = publisher.publish(topic_path, data=message)
    future.result()  

def process_message(message):
    status = message.data.decode('utf-8')
    print(f"Received message: {status}")
    if status == "OK":
        return True  
    return False

async def subscribe_to_topic():
    event = asyncio.Event()  # Event to signal status change
    print('Listening for verification responses on {}'.format(subscription_path))

    def callback(message):
        nonlocal event
        # Process the message (verify the user) and send the response
        status = message.data.decode('utf-8')
        print(f"Received message: {status} from auth provider")

        # Acknowledge the message
        message.ack()
        
        if status == "OK":
            event.set()  # Set the event to signal status change
        if status == "ERROR":
            return False
    # Subscribe to the verification response topic
    subscriber.subscribe(subscription_path, callback=callback)

    # Wait for the event to be set
    await event.wait()
    return True
# Start message processing loop
if __name__ == '__main__':
    subscribe_to_topic()
