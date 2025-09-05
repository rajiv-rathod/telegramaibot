
import os

class SolaceConfig:
    """Configuration for Solace Event Mesh integration"""
    
    # Topic patterns
    MESSAGE_EVENTS_TOPIC = "telegram/bot/messages/{chat_id}"
    ACTIVITY_TOPIC = "telegram/bot/activity/{activity_type}"
    METRICS_TOPIC = "telegram/bot/metrics"
    COMMANDS_TOPIC = "telegram/bot/commands/+"
    
    # Event types
    class ActivityTypes:
        USER_JOIN = "user_join"
        USER_LEAVE = "user_leave"
        MESSAGE_SENT = "message_sent"
        BOT_MENTION = "bot_mention"
        COMMAND_USED = "command_used"
    
    @staticmethod
    def get_broker_config():
        """Get broker configuration from environment variables"""
        return {
            "host": os.getenv("SOLACE_BROKER_HOST"),
            "vpn": os.getenv("SOLACE_VPN_NAME"),
            "username": os.getenv("SOLACE_USERNAME"),
            "password": os.getenv("SOLACE_PASSWORD")
        }
    
    @staticmethod
    def is_configured():
        """Check if all required Solace environment variables are set"""
        config = SolaceConfig.get_broker_config()
        return all(config.values())
