import asyncio
import websockets
import json
import threading
import time

class WebSocketServer:
    """
    WebSocket Server
    ================
    Broadcasts game actions to connected clients (e.g., Unity, Roblox, Web).
    Runs in a separate thread with its own asyncio event loop.
    """
    
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.loop = None
        self.running = False
        
    def start(self):
        """Start the WebSocket server in a separate thread"""
        self.running = True
        t = threading.Thread(target=self._run_server, name="WSServer", daemon=True)
        t.start()
        print(f"[OK] WebSocket Server started on ws://{self.host}:{self.port}")
        
    def _run_server(self):
        """Internal method to run the asyncio loop"""
        # Create a new event loop for this thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        shutdown_event = asyncio.Event()

        async def runner():
            # Create server within the loop context
            try:
                # On Windows, SO_REUSEADDR doesn't always work for TIME_WAIT, 
                # but let's try-catch properly.
                async with websockets.serve(self._handler, self.host, self.port):
                    await shutdown_event.wait()
            except OSError as e:
                if e.errno == 10048:
                    print(f"[WAIT] Port {self.port} is busy. WebSocket server skipped.")
                else:
                    print(f"[ERROR] WebSocket Server Error: {e}")
        
        try:
            self.loop.run_until_complete(runner())
        except Exception as e:
            print(f"[ERROR] WebSocket Loop Error: {e}")
        finally:
            self.loop.close()
            self.loop = None
        
    async def _handler(self, websocket, *args):
        """Handle new connections"""
        self.clients.add(websocket)
        try:
            # Keep connection open
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
            
    def broadcast(self, data):
        """
        Broadcast data to all connected clients.
        
        Args:
            data (dict): Dictionary to send as JSON.
        """
        if not self.clients or not self.loop or self.loop.is_closed():
            return
            
        message = json.dumps(data)
        
        # Schedule the broadcast coroutine in the server's loop
        asyncio.run_coroutine_threadsafe(self._broadcast_message(message), self.loop)
        
    async def _broadcast_message(self, message):
        """Internal coroutine to send message"""
        if self.clients:
            # websockets.broadcast is available in newer versions, 
            # but let's stick to simple iteration for compatibility
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
            
    def stop(self):
        """Stop the server (Graceful shutdown is hard with threads, usually daemon kills it)"""
        self.running = False
        # In a daemon thread, we usually just let it die when main app exits.
