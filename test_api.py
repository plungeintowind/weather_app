import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_api_connection():
    """
    测试aqicn.org API的连通性
    """
    API_KEY = os.getenv('API_KEY')
    TEST_CITY = 'beijing'  # 测试城市
    
    if not API_KEY:
        print("错误：未找到API_KEY，请在.env文件中设置")
        return
    
    url = f"https://api.waqi.info/feed/{TEST_CITY}/?token={API_KEY}"
    
    try:
        print(f"正在测试API连接，查询城市: {TEST_CITY}...")
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 检查HTTP错误
        
        data = response.json()
        
        if data['status'] == 'ok':
            print("API连接成功！")
            print(f"城市: {data['data']['city']['name']}")
            print(f"当前AQI: {data['data']['aqi']}")
            print(f"主要污染物: {data['data']['dominentpol']}")
        else:
            print(f"API返回错误: {data.get('data', '未知错误')}")
            
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
    except ValueError as e:
        print(f"JSON解析错误: {e}")

if __name__ == "__main__":
    test_api_connection()