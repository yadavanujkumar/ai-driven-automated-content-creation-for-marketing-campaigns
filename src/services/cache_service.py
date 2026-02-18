"""
Simple In-Memory Caching Service
Provides caching functionality for content generation results
"""

from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import hashlib
import json


class CacheEntry:
    """Represents a single cache entry with expiration"""
    
    def __init__(self, value: Any, ttl_seconds: int = 3600):
        self.value = value
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        """Check if this cache entry has expired"""
        return datetime.now() > self.expires_at
    
    def get_age_seconds(self) -> int:
        """Get age of cache entry in seconds"""
        return int((datetime.now() - self.created_at).total_seconds())


class SimpleCache:
    """
    Simple in-memory cache with TTL support
    
    Note: This is a demonstration cache. For production use, consider Redis.
    """
    
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time-to-live in seconds
            max_size: Maximum number of entries before eviction
        """
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
    
    def _generate_key(self, key: str) -> str:
        """Generate a hash key from input"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _cleanup_expired(self):
        """Remove expired entries from cache"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def _evict_oldest(self):
        """Evict oldest entries if cache is full"""
        if len(self.cache) >= self.max_size:
            # Sort by creation time and remove oldest 10%
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1].created_at
            )
            num_to_evict = max(1, self.max_size // 10)
            for key, _ in sorted_entries[:num_to_evict]:
                del self.cache[key]
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        cache_key = self._generate_key(key)
        
        # Check if key exists
        if cache_key not in self.cache:
            self.miss_count += 1
            return None
        
        entry = self.cache[cache_key]
        
        # Check if expired
        if entry.is_expired():
            del self.cache[cache_key]
            self.miss_count += 1
            return None
        
        self.hit_count += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        cache_key = self._generate_key(key)
        ttl = ttl or self.default_ttl
        
        # Cleanup and eviction
        self._cleanup_expired()
        self._evict_oldest()
        
        # Store new entry
        self.cache[cache_key] = CacheEntry(value, ttl)
    
    def delete(self, key: str) -> bool:
        """
        Delete entry from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        cache_key = self._generate_key(key)
        if cache_key in self.cache:
            del self.cache[cache_key]
            return True
        return False
    
    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
    
    def get_stats(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        self._cleanup_expired()
        
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate_percent': round(hit_rate, 2),
            'total_requests': total_requests
        }


class ContentCache:
    """Specialized cache for content generation"""
    
    def __init__(self, ttl: int = 3600):
        self.cache = SimpleCache(default_ttl=ttl, max_size=500)
    
    def generate_content_key(self, prompt: str, tone: str, length: int, 
                           keywords: list = None, platform: str = None) -> str:
        """Generate a unique cache key for content parameters"""
        key_data = {
            'prompt': prompt,
            'tone': tone,
            'length': length,
            'keywords': sorted(keywords or []),
            'platform': platform
        }
        return json.dumps(key_data, sort_keys=True)
    
    def get_content(self, prompt: str, tone: str, length: int,
                   keywords: list = None, platform: str = None) -> Optional[Dict]:
        """Get cached content if available"""
        key = self.generate_content_key(prompt, tone, length, keywords, platform)
        return self.cache.get(key)
    
    def cache_content(self, prompt: str, tone: str, length: int,
                     content_data: Dict, keywords: list = None, 
                     platform: str = None, ttl: int = None):
        """Cache generated content"""
        key = self.generate_content_key(prompt, tone, length, keywords, platform)
        self.cache.set(key, content_data, ttl)
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return self.cache.get_stats()
    
    def clear(self):
        """Clear content cache"""
        self.cache.clear()


# Global content cache instance
content_cache = ContentCache(ttl=3600)  # 1 hour TTL
