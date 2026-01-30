import requests
import json
import time
from config.config import Config
from typing import Dict, Any, Optional, Tuple
from config.logger_config import setup_logger

logger = setup_logger("api_client")


class APIClient:
    """HTTP客户端封装"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(
            self,
            method: str,
            endpoint: str,
            **kwargs
    ) -> Tuple[bool, Optional[Dict], Optional[requests.Response]]:
        """发送HTTP请求"""

        url = f"{self.base_url}{endpoint}"
        logger.info(f"请求方法: {method}, URL: {url}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            # 尝试解析JSON响应
            try:
                data = response.json()
                logger.debug(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return True, data, response
            except json.JSONDecodeError:
                return True, None, response

        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            return False, None, None
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            return False, None, None

    def get(self, endpoint: str, **kwargs):
        """GET请求"""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, data: Dict = None, **kwargs):
        """POST请求"""
        if data:
            kwargs["json"] = data
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, data: Dict = None, **kwargs):
        """PUT请求"""
        if data:
            kwargs["json"] = data
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, data: Dict = None, **kwargs):
        """PATCH请求"""
        if data:
            kwargs["json"] = data
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """DELETE请求"""
        return self._request("DELETE", endpoint, **kwargs)