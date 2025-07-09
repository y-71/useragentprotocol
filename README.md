# Log Server with Redis and Client

This is a Docker Compose setup with Redis, a Python Flask server, and a simple web client.

## Architecture

- **Redis**: Database for storing IO state and user messages
- **Server**: Python Flask application that serves logs and manages IO operations
- **Client**: Simple web interface to interact with the server

## How it works

1. **Get Logs**: The server provides 3 random logs when requested
2. **IO Process**: When IO is needed, the server sets an `awaiting_io` flag in Redis
3. **User Input**: The client allows users to write messages during IO
4. **Unblock**: Once the message is sent, the server unblocks and continues with more logs

## API Endpoints

### Server Endpoints

- `GET /logs` - Get 3 random logs (returns waiting status if IO is pending)
- `POST /io/start` - Start IO process (sets awaiting_io flag)
- `POST /io/write` - Write user message and unblock process
- `GET /io/read` - Read stored user message
- `GET /health` - Health check

### Client Endpoints

- `GET /` - Web interface
- `GET /api/logs` - Proxy to server logs
- `POST /api/io/start` - Proxy to start IO
- `POST /api/io/write` - Proxy to write IO
- `GET /api/io/read` - Proxy to read IO

## Running the Application

1. **Start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Access the client**:
   Open your browser and go to `http://localhost:8080`

3. **Test the workflow**:
   - Click "Get Logs" to see 3 random logs
   - Click "Start IO Process" to begin IO
   - Enter a message and click "Send Message"
   - Click "Get Logs" again to see 3 more random logs

## Services

- **Redis**: `localhost:6379`
- **Server**: `localhost:3000`
- **Client**: `localhost:8080`

## Development

The services are set up with volume mounts for development:
- Server code is in `./server/`
- Client code is in `./client/`
- Changes to the code will be reflected immediately

## Stopping the Application

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
``` 