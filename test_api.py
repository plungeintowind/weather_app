from api_handler import AQIHandler

def main():
    print("=== 空气质量查询系统 ===")
    api = AQIHandler()
    
    while True:
        city = input("\n请输入城市名称(英文或拼音，输入q退出): ").strip()
        if city.lower() == 'q':
            break
            
        try:
            data = api.get_aqi_data(city)
            print("\n✅ 查询成功！")
            print(f"城市: {data['city']}")
            print(f"AQI指数: {data['aqi']}")
            print(f"主要污染物: {data['dominant_pollutant']}")
            print(f"更新时间: {data['timestamp']}")
            print(f"最近查询: {api.history}")
            
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")

if __name__ == "__main__":
    main()