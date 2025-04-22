from flask import Blueprint, render_template, request
from .api_handler import AQIHandler
import base64

bp = Blueprint('weather', __name__)
api = AQIHandler()

@bp.route('/')
def index():
    return render_template('index.html', history=api.history[:5])

@bp.route('/query', methods=['GET'])
def query():
    city = request.args.get('city', 'hefei')  # 合肥为默认查询
    try:
        data = api.get_aqi_data(city)
        return render_template('result.html', data=data)
    except Exception as e:
        return f"<h2>查询失败: {str(e)}</h2>"

@bp.route('/compare', methods=['POST'])
def compare():
    cities = request.form.get('cities', '').split(',')
    cities = [c.strip() for c in cities if c.strip()]
    
    results = api.compare_cities(cities)
    if len(results) >= 2:
        chart = api.generate_comparison_chart(results)
        return render_template('compare.html', results=results, chart=chart)
    else:
        return "至少需要2个有效城市进行对比"