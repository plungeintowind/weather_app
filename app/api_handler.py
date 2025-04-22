import requests
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from dotenv import load_dotenv

load_dotenv()

class AQIHandler:
    """空气质量API处理器（完整版）"""
    
    def __init__(self):
        self.base_url = "https://api.waqi.info/feed/"
        self.api_key = os.getenv("API_KEY")
        self.history = []  # 查询历史记录

    def get_aqi_data(self, city):
        """获取单城市AQI数据（如合肥）"""
        if not self.api_key:
            raise ValueError("❌ 请在.env文件中配置API_KEY")

        url = f"{self.base_url}{city}/?token={self.api_key}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "ok":
                raise ValueError(f"API返回错误: {data.get('data', '未知错误')}")
            
            self._add_to_history(city)
            return self._parse_data(data)
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"网络请求失败: {str(e)}")
        except Exception as e:
            raise ValueError(f"数据处理失败: {str(e)}")

    def compare_cities(self, cities):
        """比较多个城市AQI（自动跳过无效数据）"""
        results = []
        for city in cities:
            try:
                data = self.get_aqi_data(city)
                # 确保AQI是有效数字
                if isinstance(data["aqi"], int) and data["aqi"] >= 0:
                    results.append({
                        "city": data["city"],
                        "aqi": data["aqi"],
                        "pollutant": data["dominant_pollutant"]
                    })
                else:
                    print(f"⚠️ 跳过{city}：无效AQI值({data['aqi']})")
            except Exception as e:
                print(f"⚠️ 跳过{city}：{str(e)}")
        return results

    def generate_comparison_chart(self, cities_data):
        """生成对比图表（返回Base64编码的图片数据）"""
        try:
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure(figsize=(10, 5))
            cities = [d["city"] for d in cities_data]
            aqis = [d["aqi"] for d in cities_data]
            
            bars = plt.bar(cities, aqis, color=[self._get_aqi_color(aqi) for aqi in aqis])
            
            # 添加数据标签
            for bar, aqi in zip(bars, aqis):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                        f"{aqi}", ha='center', va='bottom')
            
            plt.title("城市AQI对比")
            plt.ylabel("AQI指数")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # 保存到内存缓冲区
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            plt.close()
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            print(f"图表生成失败: {str(e)}")
            return None

    def _parse_data(self, raw_data):
        """解析原始数据"""
        data = raw_data["data"]
        return {
            "city": data["city"]["name"],
            "aqi": data["aqi"],
            "dominant_pollutant": data.get("dominentpol", "N/A"),
            "timestamp": data["time"]["s"]
        }

    def _add_to_history(self, city):
        """记录查询历史"""
        if city not in self.history:
            self.history = [city] + self.history[:4]  # 保留最近5条

    def _get_aqi_color(self, aqi):
        """根据AQI值返回颜色（兼容无效值）"""
        if not isinstance(aqi, (int, float)) or aqi < 0:
            return 'gray'  # 无效值显示灰色
        elif aqi <= 50: return 'green'
        elif aqi <= 100: return 'yellowgreen'
        elif aqi <= 150: return 'orange'
        elif aqi <= 200: return 'red'
        else: return 'purple'
