import sys
import os
# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                
from dotenv import load_dotenv
import tushare as ts

load_dotenv() 
TUSHARE_API_TOKEN = os.getenv('TUSHARE_API_TOKEN')

pro = ts.pro_api(TUSHARE_API_TOKEN)

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