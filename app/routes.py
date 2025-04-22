from flask import Blueprint, render_template, request, redirect, url_for
from .api_handler import AQIHandler
import base64

bp = Blueprint('weather', __name__)
api = AQIHandler()

@bp.route('/')
def index():
    """首页：展示查询表单和历史记录"""
    return render_template("index.html", history=api.history[:5])

@bp.route('/query')
def query():
    """
    单城市查询路由
    默认查询合肥，可接受 ?city=城市名 参数
    """
    city = request.args.get('city', 'hefei').strip()
    try:
        data = api.get_aqi_data(city)
        pollutant_chart = api.generate_pollutant_chart(data)
        return render_template(
            "result.html",
            data=data,
            pollutant_chart=pollutant_chart
        )
    except Exception as e:
        # 重定向到错误页面，并携带错误信息
        return redirect(url_for('weather.error', message=f"查询失败: {str(e)}"))

@bp.route('/compare', methods=['POST'])
def compare():
    """
    多城市对比路由
    接收城市列表（逗号分隔）
    """
    cities = request.form.get('cities', '').split(',')
    cities = [c.strip() for c in cities if c.strip()]
    
    results = api.compare_cities(cities)
    if len(results) >= 2:
        chart = api.generate_comparison_chart(results)
        return render_template("compare.html", results=results, chart=chart)
    else:
        return redirect(url_for('weather.error', message="至少需要2个有效城市进行对比"))

@bp.route('/error')
def error():
    """统一错误处理页面"""
    error_msg = request.args.get('message', '未知错误')
    return render_template("error.html", error_msg=error_msg)