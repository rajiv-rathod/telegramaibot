
import json
import asyncio
from typing import Optional, Callable
from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic import Topic
from solace.messaging.publisher.direct_message_publisher import DirectMessagePublisher
from solace.messaging.receiver.direct_message_receiver import DirectMessageReceiver
from solace.messaging.config.solace_properties import service_properties
from solace.messaging.config.authentication_strategy import ClientCertificateAuthentication
from datetime import datetime

class SolaceEventMesh:
    def __init__(self, broker_host: str, vpn_name: str, username: str, password: str):
        self.broker_host = broker_host
        self.vpn_name = vpn_name
        self.username = username
        self.password = password
        self.messaging_service: Optional[MessagingService] = None
        self.publisher: Optional[DirectMessagePublisher] = None
        self.receiver: Optional[DirectMessageReceiver] = None
        self.message_handlers = {}

    async def connect(self):
        """Connect to Solace Event Mesh"""
        try:
            # Configure connection properties
            broker_props = {
                service_properties.SOLACE_HOST: self.broker_host,
                service_properties.SOLACE_VPN_NAME: self.vpn_name,
                service_properties.AUTHENTICATION_STRATEGY_BASIC_USER_NAME: self.username,
                service_properties.AUTHENTICATION_STRATEGY_BASIC_PASSWORD: self.password
            }
            
            # Create messaging service
            self.messaging_service = MessagingService.builder().from_properties(broker_props).build()
            self.messaging_service.connect()
            
            # Create publisher
            self.publisher = self.messaging_service.create_direct_message_publisher_builder().build()
            self.publisher.start()
            
            # Create receiver
            self.receiver = self.messaging_service.create_direct_message_receiver_builder().build()
            self.receiver.start()
            
            print("✅ Connected to Solace Event Mesh")
            
        except Exception as e:
            print(f"❌ Failed to connect to Solace: {e}")
            raise

    async def disconnect(self):
        """Disconnect from Solace Event Mesh"""
        try:
            if self.publisher:
                self.publisher.terminate()
            if self.receiver:
                self.receiver.terminate()
            if self.messaging_service:
                self.messaging_service.disconnect()
            print("✅ Disconnected from Solace Event Mesh")
        except Exception as e:
            print(f"❌ Error disconnecting from Solace: {e}")

    async def publish_message_event(self, chat_id: str, user_id: str, message: str, response: str):
        """Publish message event to Solace"""
        try:
            if not self.publisher:
                print("❌ Publisher not initialized")
                return
                
            topic_string = f"telegram/bot/messages/{chat_id}"
            topic = Topic.of(topic_string)
            
            event_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "chat_id": chat_id,
                "user_id": user_id,
                "user_message": message,
                "bot_response": response,
                "event_type": "message_exchange"
            }
            
            message_payload = json.dumps(event_data)
            self.publisher.publish(destination=topic, message=message_payload)
            print(f"📤 Published event to {topic_string}")
            
        except Exception as e:
            print(f"❌ Failed to publish message event: {e}")

    async def publish_user_activity(self, chat_id: str, user_id: str, activity_type: str, metadata: dict = None):
        """Publish user activity events"""
        try:
            if not self.publisher:
                print("❌ Publisher not initialized")
                return
                
            topic_string = f"telegram/bot/activity/{activity_type}"
            topic = Topic.of(topic_string)
            
            activity_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "chat_id": chat_id,
                "user_id": user_id,
                "activity_type": activity_type,
                "metadata": metadata or {}
            }
            
            message_payload = json.dumps(activity_data)
            self.publisher.publish(destination=topic, message=message_payload)
            print(f"📤 Published activity: {activity_type}")
            
        except Exception as e:
            print(f"❌ Failed to publish activity: {e}")

    def subscribe_to_topic(self, topic_pattern: str, handler: Callable):
        """Subscribe to events on a topic"""
        try:
            if not self.receiver:
                print("❌ Receiver not initialized")
                return
                
            topic = Topic.of(topic_pattern)
            self.message_handlers[topic_pattern] = handler
            
            def message_handler(message):
                try:
                    payload = json.loads(message.get_payload_as_string())
                    asyncio.create_task(handler(payload))
                except Exception as e:
                    print(f"❌ Error handling message: {e}")
            
            self.receiver.receive_async(topic, message_handler)
            print(f"📥 Subscribed to {topic_pattern}")
            
        except Exception as e:
            print(f"❌ Failed to subscribe to {topic_pattern}: {e}")

    async def publish_bot_metrics(self, metrics: dict):
        """Publish bot performance metrics"""
        try:
            if not self.publisher:
                return
                
            topic = Topic.of("telegram/bot/metrics")
            
            metrics_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": metrics
            }
            
            message_payload = json.dumps(metrics_data)
            self.publisher.publish(destination=topic, message=message_payload)
            
        except Exception as e:
            print(f"❌ Failed to publish metrics: {e}")

# Global Solace instance
solace_client: Optional[SolaceEventMesh] = None

async def init_solace():
    """Initialize Solace connection with environment variables"""
    global solace_client
    
    # You'll need to set these in Replit Secrets
    broker_host = os.getenv("SOLACE_BROKER_HOST", "tcps://your-broker.messaging.solace.cloud:55443")
    vpn_name = os.getenv("SOLACE_VPN_NAME", "your-vpn")
    username = os.getenv("SOLACE_USERNAME", "your-username")
    password = os.getenv("SOLACE_PASSWORD", "your-password")
    
    if all([broker_host, vpn_name, username, password]):
        solace_client = SolaceEventMesh(broker_host, vpn_name, username, password)
        await solace_client.connect()
        
        # Set up subscriptions for bot commands
        async def handle_bot_commands(payload):
            print(f"📨 Received bot command: {payload}")
            # Handle remote bot commands here
            
        solace_client.subscribe_to_topic("telegram/bot/commands/+", handle_bot_commands)
    else:
        print("⚠️ Solace credentials not configured in environment variables")

async def cleanup_solace():
    """Cleanup Solace connection"""
    global solace_client
    if solace_client:
        await solace_client.disconnect()
