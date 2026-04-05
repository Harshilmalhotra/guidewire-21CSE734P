import logging
import json
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "layer": getattr(record, "layer", "system"),
            "trace_id": getattr(record, "trace_id", "N/A"),
            "event": record.getMessage(),
            "model_version": getattr(record, "model_version", "v1.0.0"),
            "latency_ms": getattr(record, "latency_ms", 0.0),
            "status": getattr(record, "status", "success")
        }
        return json.dumps(log_obj)

def get_system_logger():
    os.makedirs("data", exist_ok=True)
    logger = logging.getLogger("UCDE_SYSTEM")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # Rotate on 10MB limits matching Phase 10 boundaries gracefully retaining 5 logs natively
        try:
            handler = RotatingFileHandler("data/ucde_system.log", maxBytes=10*1024*1024, backupCount=5)
            handler.setFormatter(JSONFormatter())
            logger.addHandler(handler)
        except Exception:
            pass
        
        # Optionally stream natively handling metrics actively parsing strings gracefully
        console = logging.StreamHandler()
        console.setFormatter(JSONFormatter())
        logger.addHandler(console)
        
    return logger

system_logger = get_system_logger()
