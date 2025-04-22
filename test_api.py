from api_handler import AQIHandler
import base64  

def main():
    api = AQIHandler()
    
    print("=== 空气质量查询系统 ===")
    print("1. 查询单城市  2. 多城市对比")
    choice = input("请选择模式: ").strip()
    
    if choice == "1":
        # 单城市查询（兼容合肥）
        city = input("输入城市名(如hefei): ").strip()
        try:
            data = api.get_aqi_data(city)
            print(f"\n城市: {data['city']}")
            print(f"AQI: {data['aqi']} | 主要污染物: {data['dominant_pollutant']}")
        except Exception as e:
            print(f"错误: {str(e)}")
            
    elif choice == "2":
        # 多城市对比
        cities = input("输入城市列表(用逗号分隔，如hefei,beijing): ").split(',')
        cities = [c.strip() for c in cities if c.strip()]
        
        results = api.compare_cities(cities)
        if results:
            print("\n=== 对比结果 ===")
            for res in results:
                print(f"{res['city']}: AQI {res['aqi']} ({res['pollutant']})")
            
            # 生成图表
            # 替换原来的保存代码
            chart = api.generate_comparison_chart(results)
            if chart:  # 确保有图表数据
                with open("comparison.png", "wb") as f:
                    f.write(base64.b64decode(chart))
                print("✅ 图表已保存为 comparison.png")
            
if __name__ == "__main__":
    main()