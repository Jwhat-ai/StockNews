import sys
import os
# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
from dotenv import load_dotenv
import tushare as ts

# 设置Tushare API token - 替换为你的实际token

load_dotenv() 
TUSHARE_API_TOKEN = os.getenv('TUSHARE_API_TOKEN')

ts.set_token('TUSHARE_API_TOKEN')
pro = ts.pro_api()

# 拉取数据
df = pro.major_news(**{
    "src": "新浪财经",
    "start_date": "6/16/2026",
    "end_date": "6/17/2026",
    "limit": "",
    "offset": ""
}, fields=[
    "pub_time",
    "src",
    "url",
    "content",
    "title"
])
print(df)