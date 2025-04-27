from prometheus_client import Counter, Gauge, start_http_server
import psutil


class MetricsCollector:
    def __init__(self, port=8000):
        start_http_server(port)

        self.detections_total = Counter(
            "reverse_shell_detections_total", "Total number of reverse shell detections"
        )
        self.false_positive_total = Counter(
            "false_positives_total", "Total number of false positives"
        )

        self.cpu_usage = Gauge(
            "daemon_cpu_usage", "Current CPU usage percentage of daemon"
        )
        self.memory_usage = Gauge(
            "daemon_memory_usage", "Current memory usage MB of daemon"
        )

    def update_resource_usage(self):
        process = psutil.Process()
        self.cpu_usage.set(process.cpu_percent(interval=1))
        self.memory_usage.set(process.memory_info().rss / 1024 / 1024)
