"""
Rate Limiting Middleware
Implements simple in-memory rate limiting for API endpoints
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import time


class RateLimiter:
    """
    Simple in-memory rate limiter for API endpoints
    """
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Maximum requests allowed per minute per IP
            requests_per_hour: Maximum requests allowed per hour per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Storage for request timestamps: {ip_address: [timestamps]}
        self.request_history: Dict[str, list] = defaultdict(list)
        
        # Last cleanup time
        self.last_cleanup = datetime.now()
    
    def _cleanup_old_entries(self):
        """Remove entries older than 1 hour to prevent memory bloat"""
        now = datetime.now()
        
        # Only cleanup every 10 minutes
        if (now - self.last_cleanup).seconds < 600:
            return
        
        cutoff_time = now - timedelta(hours=1)
        
        for ip in list(self.request_history.keys()):
            # Filter out old timestamps
            self.request_history[ip] = [
                ts for ts in self.request_history[ip]
                if ts > cutoff_time
            ]
            
            # Remove empty entries
            if not self.request_history[ip]:
                del self.request_history[ip]
        
        self.last_cleanup = now
    
    def is_rate_limited(self, ip_address: str) -> Tuple[bool, str]:
        """
        Check if an IP address should be rate limited
        
        Args:
            ip_address: The IP address to check
            
        Returns:
            Tuple of (is_limited, reason)
        """
        now = datetime.now()
        
        # Cleanup old entries periodically
        self._cleanup_old_entries()
        
        # Get request history for this IP
        timestamps = self.request_history[ip_address]
        
        # Check requests in the last minute
        minute_ago = now - timedelta(minutes=1)
        recent_requests = [ts for ts in timestamps if ts > minute_ago]
        
        if len(recent_requests) >= self.requests_per_minute:
            return True, f"Rate limit exceeded: {self.requests_per_minute} requests per minute"
        
        # Check requests in the last hour
        hour_ago = now - timedelta(hours=1)
        hourly_requests = [ts for ts in timestamps if ts > hour_ago]
        
        if len(hourly_requests) >= self.requests_per_hour:
            return True, f"Rate limit exceeded: {self.requests_per_hour} requests per hour"
        
        return False, ""
    
    def record_request(self, ip_address: str):
        """
        Record a new request from an IP address
        
        Args:
            ip_address: The IP address making the request
        """
        now = datetime.now()
        self.request_history[ip_address].append(now)
    
    def get_rate_limit_info(self, ip_address: str) -> Dict:
        """
        Get current rate limit status for an IP
        
        Args:
            ip_address: The IP address to check
            
        Returns:
            Dictionary with rate limit information
        """
        now = datetime.now()
        timestamps = self.request_history[ip_address]
        
        # Count recent requests
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        requests_last_minute = len([ts for ts in timestamps if ts > minute_ago])
        requests_last_hour = len([ts for ts in timestamps if ts > hour_ago])
        
        return {
            'requests_last_minute': requests_last_minute,
            'minute_limit': self.requests_per_minute,
            'requests_last_hour': requests_last_hour,
            'hour_limit': self.requests_per_hour,
            'remaining_minute': max(0, self.requests_per_minute - requests_last_minute),
            'remaining_hour': max(0, self.requests_per_hour - requests_last_hour)
        }


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60, requests_per_hour=1000)


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware function to apply rate limiting to requests
    
    Args:
        request: The incoming request
        call_next: The next middleware/endpoint in the chain
        
    Returns:
        Response or rate limit error
    """
    # Get client IP address
    client_ip = request.client.host if request.client else "unknown"
    
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)
    
    # Check if rate limited
    is_limited, reason = rate_limiter.is_rate_limited(client_ip)
    
    if is_limited:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "message": reason,
                "retry_after_seconds": 60
            }
        )
    
    # Record this request
    rate_limiter.record_request(client_ip)
    
    # Get rate limit info for headers
    rate_info = rate_limiter.get_rate_limit_info(client_ip)
    
    # Process request
    response = await call_next(request)
    
    # Add rate limit headers to response
    response.headers["X-RateLimit-Limit-Minute"] = str(rate_info['minute_limit'])
    response.headers["X-RateLimit-Remaining-Minute"] = str(rate_info['remaining_minute'])
    response.headers["X-RateLimit-Limit-Hour"] = str(rate_info['hour_limit'])
    response.headers["X-RateLimit-Remaining-Hour"] = str(rate_info['remaining_hour'])
    
    return response
