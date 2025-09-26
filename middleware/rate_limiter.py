import time
from typing import Dict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Rate limiter simple basé sur une fenêtre glissante
        
        Args:
            max_requests: Nombre maximum de requêtes par fenêtre
            time_window: Fenêtre de temps en secondes
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_ip: str) -> bool:
        """Vérifie si la requête est autorisée pour cette IP"""
        current_time = time.time()
        
        # Nettoyer les anciennes requêtes
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.time_window
            ]
        else:
            self.requests[client_ip] = []
        
        # Vérifier la limite
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        
        # Ajouter cette requête
        self.requests[client_ip].append(current_time)
        return True


# Instance globale du rate limiter
rate_limiter = RateLimiter(max_requests=5, time_window=60)  # 5 requêtes par minute


async def rate_limit_middleware(request: Request, call_next):
    """Middleware pour limiter le taux de requêtes"""
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Trop de requêtes. Limite: {rate_limiter.max_requests} requêtes par {rate_limiter.time_window}s",
                "retry_after": rate_limiter.time_window
            }
        )
    
    response = await call_next(request)
    return response
