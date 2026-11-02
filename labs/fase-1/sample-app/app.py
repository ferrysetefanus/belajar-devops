import http.server
import json
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))
DB_HOST = os.environ.get("DB_HOST", "None (Standalone Mode)")
DB_NAME = os.environ.get("DB_NAME", "None")
DB_USER = os.environ.get("DB_USER", "None")

def get_sales_data():
    return {
        "company": "TBS Food",
        "service": "Internal Sales Dashboard API",
        "version": "1.1.0",
        "environment": os.environ.get("ENV", "Docker Container (Local)"),
        "database_connection": {
            "configured": DB_HOST != "None (Standalone Mode)",
            "host": DB_HOST,
            "database_name": DB_NAME,
            "user": DB_USER,
            "status": "CONNECTED_TO_DOCKER_NETWORK" if DB_HOST != "None (Standalone Mode)" else "STANDALONE"
        },
        "summary_today": {
            "total_revenue": "Rp 2.060.000",
            "total_transactions": 6,
            "successful_orders": 5,
            "failed_orders": 1
        },
        "outlets": ["Jakarta Barat", "Bandung", "Surabaya", "Jakarta Selatan", "Semarang", "Tangerang"]
    }

class SalesDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "UP", "database_host": DB_HOST}).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(get_sales_data(), indent=4).encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[SalesApp-Log] {self.address_string()} - {format % args}", flush=True)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SalesDashboardHandler) as httpd:
        print(f"==================================================", flush=True)
        print(f"🚀 TBS Food Sales App berjalan di port {PORT}...", flush=True)
        print(f"🔗 Target Database Host: {DB_HOST}", flush=True)
        print(f"👉 Akses browser di: http://localhost:{PORT}", flush=True)
        print(f"👉 Healthcheck di:   http://localhost:{PORT}/health", flush=True)
        print(f"==================================================", flush=True)
        httpd.serve_forever()
