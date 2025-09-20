"""
Brawl Stars API 錯誤處理
"""

import json
from typing import Dict, Any, Optional

class ClientError:
    """官方 API 錯誤回應結構"""
    def __init__(self, reason: str = "", message: str = "", error_type: str = "", detail: Dict[str, Any] = None):
        self.reason = reason
        self.message = message
        self.type = error_type
        self.detail = detail or {}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClientError':
        return cls(
            reason=data.get('reason', ''),
            message=data.get('message', ''),
            error_type=data.get('type', ''),
            detail=data.get('detail', {})
        )

class BrawlStarsAPIError(Exception):
    """Brawl Stars API 自定義錯誤類別"""
    def __init__(self, status_code: int, message: str, client_error: Optional[ClientError] = None, details: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.message = message
        self.client_error = client_error
        self.details = details or {}
        super().__init__(self.message)

class ErrorHandler:
    """錯誤處理器類別"""
    
    @classmethod
    def parse_client_error(cls, response_text: str) -> Optional[ClientError]:
        try:
            data = json.loads(response_text)
            if isinstance(data, dict) and 'message' in data:
                return ClientError.from_dict(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        return None
    
    @classmethod
    def handle_http_error(cls, status_code: int, response_text: str = None) -> BrawlStarsAPIError:
        client_error = None
        if response_text:
            client_error = cls.parse_client_error(response_text)
        
        # 如果有 ClientError，使用其中的 message；否則使用預設訊息
        message = client_error.message if client_error and client_error.message else f"HTTP {status_code}"
        
        return BrawlStarsAPIError(status_code, message, client_error)
    
    @classmethod
    def handle_request_exception(cls, exception) -> BrawlStarsAPIError:
        if hasattr(exception, 'response') and exception.response is not None:
            status_code = exception.response.status_code
            response_text = exception.response.text
            return cls.handle_http_error(status_code, response_text)
        else:
            return BrawlStarsAPIError(0, f"Network error: {str(exception)}")
    
    @classmethod
    def handle_json_decode_error(cls, exception) -> BrawlStarsAPIError:
        return BrawlStarsAPIError(0, "JSON decode error")
    
    @classmethod
    def handle_general_error(cls, exception) -> BrawlStarsAPIError:
        return BrawlStarsAPIError(0, f"Unexpected error: {str(exception)}")
    
    @classmethod
    def print_error(cls, error: BrawlStarsAPIError):
        print("=" * 60)
        print("❌ Brawl Stars API 錯誤:")
        
        if error.status_code > 0:
            if error.client_error and error.client_error.message:
                print(f"{error.status_code} {error.client_error.message}")
            else:
                print(f"{error.status_code} {error.message}")
        else:
            print(f"{error.message}")
