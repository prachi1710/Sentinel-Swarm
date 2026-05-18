from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.redis_client import REDIS_URL
import redis.asyncio as aioredis
import asyncio

ws_router = APIRouter()

@ws_router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Async redis client for subscribing
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe("sentinel_events")
    
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_text(message["data"])
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await pubsub.unsubscribe("sentinel_events")
        await redis.close()
