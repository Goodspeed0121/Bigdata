from django.shortcuts import render
import pandas as pd

from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

'''
{'CARDINAL': {'政治': [('2020', 249),
   ('10', 170),
   ('15', 113),
   ('13', 105),
  ...
  }
'''

# ne names
ne_name =['EVENT','FAC','GPE','LANGUAGE','LAW','LOC','NORP','ORG','PERSON','PRODUCT','WORK_OF_ART']
idx2nename = { str(i) : item for i, item in enumerate(ne_name)}
'''
{0: 'EVENT',
 1: 'FAC',
 2: 'GPE',
 3: 'LANGUAGE',
 4: 'LAW',
 5: 'LOC',
 6: 'NORP',
 7: 'ORG',
 8: 'PERSON',
 9: 'PRODUCT',
 10: 'WORK_OF_ART'}

Name	Description
CARDINAL	數字
DATE	日期
EVENT	事件
FAC	設施
GPE	行政區
LANGUAGE	語言
LAW	法律
LOC	地理區
MONEY	金錢
NORP	民族、宗教、政治團體
ORDINAL	序數
ORG	組織
PERCENT	百分比率
PERSON	人物
PRODUCT	產品
QUANTITY	數量
TIME	時間
WORK_OF_ART	作品

'''

# category names
news_categories=['即時','國際','熱門','政治','生活','社會','蒐奇','地方','全部']
idx2cate = { str(i) : item for i, item in enumerate(news_categories)}
'''
{'0': '即時',
 '1': '國際',
 '2': '熱門',
 '3': '政治',
 '4': '生活',
 '5': '社會',
 '6': '蒐奇',
 '7': '地方',
 '8': '全部'}
'''

def load_data_topNer():
    # read data
    df_topNer = pd.read_csv('app_top_ner/dataset/省宏專用/Finals_topkey_by_ne_and_category.csv')

    global data
    data = {}
    for idx, row in df_topNer.iterrows():
        ne_row = eval(row['top_keys'])
        cate_wf={}
        for cate_wf_row in ne_row:
            cate_wf[ cate_wf_row[0] ] = cate_wf_row[1]
        data[row['ne_name']]= cate_wf
    return

# We should call load_data() at first.
load_data_topNer()

def home(request):
    return render(request,'app_top_ner/home.html')

# When Post is used, the csrf of this function should be ignored
@csrf_exempt
def api_get_cat_topkey(request):

    # POST方式取得新聞類別
    cate = request.POST.get('news_category')
    cate = idx2cate[cate]

    # 取得多少筆關鍵詞
    topk = int(request.POST.get('topk'))

    ner_value = request.POST.get('ner_value')
    ner_value = idx2nename[ner_value]

    print(ner_value, cate, topk)

    responseData = get_category_topkey(ner_value, cate, topk)
    response = {'data': responseData }
    print(response)
    return JsonResponse(response)


# Cloud chart
# text size based on the value of word frequency for drawing cloud chart
'''
    clouddata=[{
      'text': '台北市',
      'size': 40
    },
    {
      'text': '高雄市',
      'size': 15
    },
    {
      'text': '台北市',
      'size': 25
    }]
'''

def get_category_topkey(ner_value, cate, topk):

    wf_pairs = data[ner_value][cate][0:topk]

    if wf_pairs == []:
        return []

    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]

    # Prepare cloud chart data
    # the minimum and maximum frequency of top words
    min_ = wf_pairs[-1][1]  # the last line is smaller
    max_ = wf_pairs[0][1]   # the first frequency value is larger

    textSizeMin = 10
    textSizeMax = 90

    if (min_ != max_):
        max_min_range = max_ - min_

    else:
        max_min_range = len(wf_pairs)
        min_ = min_ - 1

    # cloud chart data
    # using proportional scaling
    clouddata = [{'text':w, 'size':int(textSizeMin+(f - min_)/max_min_range*(textSizeMax-textSizeMin))} for w, f in wf_pairs]

    responseData = {
        "wf_pairs": wf_pairs,
        "data_barchart":{
                        "category": cate,
                        "labels": words,
                        "values": freqs
                        },
        "data_cloud": clouddata}
    return responseData


print("app_top_ner載入成功!")
