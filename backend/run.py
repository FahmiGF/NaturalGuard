"""NATURALGUARD AI — Server Entry Point."""
import os
import socket
import uvicorn


def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


if __name__ == "__main__":
    requested_port = int(os.getenv("PORT", 8000))
    port = requested_port if is_port_available(requested_port) else 8005
    print("=" * 60)
    print(" 🛡️  NATURALGUARD AI — Early Warning & Disaster Platform")
    print(f" 🌐 Dashboard: http://localhost:{port}")
    print(f" 📚 OpenAPI Docs: http://localhost:{port}/docs")
    print("=" * 60)
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
