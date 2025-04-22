import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class AQIHandler:
    """空气质量API处理器"""
    
    def __init__(self):
        self.base_url = "https://api.waqi.info/feed/"
        self.api_key = os.getenv("API_KEY")  # 从.env读取密钥
        self.history = []  # 查询历史记录

    def get_aqi_data(self, city):
        """获取指定城市的AQI数据"""
        if not self.api_key:
            raise ValueError("❌ 请在.env文件中配置API_KEY")

        url = f"{self.base_url}{city}/?token={self.api_key}"
        
        try:
            # 发送请求（设置5秒超时）
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # 自动检查HTTP错误
            
            data = response.json()
            if data.get("status") != "ok":
                raise ValueError(f"API返回错误: {data.get('data', '未知错误')}")
            
            # 记录查询历史
            self._add_to_history(city)
            
            # 返回解析后的数据
            return self._parse_data(data)
            
        except requests.exceptions.RequestException as e:
            # 网络请求异常
            raise ConnectionError(f"网络请求失败: {str(e)}")
        except ValueError as e:
            # JSON解析或业务逻辑错误
            raise ValueError(f"数据解析失败: {str(e)}")

    def _parse_data(self, raw_data):
        """解析原始API数据（私有方法）"""
        city_data = raw_data["data"]
        return {
            "city": city_data["city"]["name"],
            "aqi": city_data["aqi"],
            "dominant_pollutant": city_data.get("dominentpol", "N/A"),
            "timestamp": city_data["time"]["s"]
        }

    def _add_to_history(self, city):
        """添加查询历史（私有方法）"""
        if city not in self.history:
            self.history = [city] + self.history[:4]  # 最多保留5条记录