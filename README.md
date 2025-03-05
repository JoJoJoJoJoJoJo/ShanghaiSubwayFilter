# 上海地铁站筛选
筛选从指定地铁站开始n站内有哪些地铁站，结果按地铁线分组

在寻找合适的租房的时候想到了这么个脚本🤣

地铁数据来自高德地图，感谢[知乎文章](https://zhuanlan.zhihu.com/p/681589792)提供的方案

## Usage
```bash
python subway.py 世纪大道 2 --banned-lines 6 --max-changes 1
```

output:
```
2号线: 陆家嘴 世纪公园 上海科技馆 浦东南路(原东昌路) 世纪大道
18号线: 杨高中路 民生路 迎春路
14号线: 浦东大道 浦东南路 源深路 陆家嘴
9号线: 商城路 小南门 杨高中路 世纪大道 芳甸路
4号线: 浦东大道 世纪大道 向城路 蓝村路 杨树浦路
```

## Structure
- `raw_subway_info.json`: 从高德地图抓来的原始json数据
- `subway_info.json`: 解析原始数据后生成的只包含地铁站及线路信息的数据

## 其他城市支持&数据更新
其他城市，或者上海数据更新后可以参考同样的方案复制json数据并覆盖`raw_subway_info.json`。覆盖后需运行`build_subway_info`

# TODO
- [x] 黑名单，排除掉某些特别挤的换乘站（比如东方体育中心）/ 地铁线
- [x] format args, 提供json数据更新的专用命令
- [x] 限制换乘次数

# Known issues
- 返回的结果没有排序
