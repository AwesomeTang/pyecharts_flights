from pyecharts.charts import *
from pyecharts import options as opts
import json

# 读取航线文件
with open("flights.json", 'r') as f:
    data = json.loads(f.read())

airports = data['airports']
airlines = data['airlines']
routes = data['routes']


# 绘制全球机场散点图
def airports_viz(airports_data):
    """
    绘制全球机场散点图
    :param airports_data: 机场位置数据
    :return: pyecharts GEO图表实例
    """
    data_pair = []
    geo = Geo(init_opts=opts.InitOpts(theme='dark', bg_color='#000000', width='1980px', height='1080px'))
    for idx, item in enumerate(airports_data):
        # 新增机场位置信息到geo
        geo.add_coordinate(str(idx), item[3], item[4])
        data_pair.append([str(idx), 1])

    geo.add_schema(
        maptype="world",
        is_roam=False,  # 禁止缩放
        zoom=1.1,  # 显示比例
        itemstyle_opts=opts.ItemStyleOpts(color="#000000", border_color="#1E90FF"),
        emphasis_label_opts=opts.LabelOpts(is_show=False),
        emphasis_itemstyle_opts=opts.ItemStyleOpts(color="#323c48")
    )

    geo.add("机场",
            data_pair,
            type_='scatter',
            is_selected=True,
            symbol_size=2,
            is_large=True,
            itemstyle_opts=opts.ItemStyleOpts(color="#E1FFFF")
            )

    # 关闭Label显示
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    geo.set_global_opts(
        title_opts=opts.TitleOpts(title="全球机场分布", pos_top='3%', pos_left='center'),
        tooltip_opts=opts.TooltipOpts(is_show=False),  # 关闭提示框
        legend_opts=opts.LegendOpts(is_show=True, pos_left='left', pos_top='2', orient='vertical')
    )

    return geo


def flights_line_viz(airports_data, route_data):
    geo = Geo(init_opts=opts.InitOpts(theme='dark', bg_color='#000000', width='1980px', height='1080px'))

    # 添加机场的坐标点
    for idx, item in enumerate(airports_data):
        geo.add_coordinate("airports" + str(idx), item[3], item[4])

    geo.add_schema(
        maptype="world",
        is_roam=False,
        zoom=1.1,
        itemstyle_opts=opts.ItemStyleOpts(color="#000000", border_color="#1E90FF"),
        emphasis_label_opts=opts.LabelOpts(is_show=False),
        emphasis_itemstyle_opts=opts.ItemStyleOpts(color="#323c48")
    )

    idx = route_data[0][0]
    data_pair = []
    for item in route_data:
        if item[0] == idx:
            data_pair.append(["airports" + str(item[1]), "airports" + str(item[2])])
        else:
            geo.add(airlines[idx][0],
                    data_pair,
                    type_='lines',
                    is_selected=True if airlines[idx][0] == 'Air China' else False,
                    symbol_size=1,
                    is_large=True,
                    large_threshold=1e6,
                    progressive_threshold=100000,
                    linestyle_opts=opts.LineStyleOpts(curve=0.2, opacity=0.03, color='#1E90FF', width=0.2),
                    effect_opts=opts.EffectOpts(symbol='pin', period=5, symbol_size=2, trail_length=0.5,
                                                color="#E1FFFF"),
                    )
            data_pair = []
            idx = item[0]

    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    geo.set_global_opts(
        title_opts=opts.TitleOpts(title="航线图", pos_top='3%', pos_left='center'),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        legend_opts=opts.LegendOpts(is_show=True, pos_left='left', pos_top='50%', orient='vertical',
                                    selected_mode='single')
    )

    return geo


if __name__ == "__main__":
    charts = airports_viz(airports)
    charts.render('airports.html')

    charts = flights_line_viz(airports, routes)
    charts.render('flights_line.html')

