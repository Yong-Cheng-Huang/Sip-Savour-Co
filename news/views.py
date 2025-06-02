from django.shortcuts import render
from products.models import Product
from datetime import date
from django.core.paginator import Paginator

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:3]
    context = {
        'featured_products': featured_products
    }
    return render(request, 'home.html', context)

def news_index(request):
    news_list = [
        {
            'publish_date': date(2025, 6, 4),
            'title': 'SipSavour｜全新菜單 Coming Soon ✨',
            'image': 'images/0604.jpg',
            'content': [
                '🍋 【沁涼特調】手工現榨檸檬搭配薄荷香氣，清新直擊味蕾，一口喝走盛夏的燥熱。',
                '🥗 【活力沙拉碗】嚴選鮮嫩雞胸，搭配多彩時蔬與穀物，輕盈無負擔，健康滿分。',
                '🥞 【經典鬆餅塔】金黃酥香的鬆餅層層堆疊，淋上香甜楓糖，每一口都是幸福感爆棚。',
                '🍛 【風味焗烤飯】特製香料飯搭配豐富配料，起司焗烤香氣四溢，溫暖你的每個午後。',
                '📅 2025年6月14日 全新登場｜首日打卡享驚喜好禮，數量有限，送完為止！',
                'SipSavour — 用心選料，用味道記住每個季節。'
            ]
        },
        {
            'publish_date': date(2025, 5, 28),
            'title': 'SipSavour｜冷萃工藝・細品夏日',
            'image': 'images/0528.jpg',
            'content': [
                '夏日炎炎，來一杯手工冷萃的細膩沁涼。',
                '我們嚴選高品質咖啡豆，歷經長時低溫慢釀，綻放出絲滑香氣與溫潤口感，只為給你專屬於夏季的極致享受。',
                '📅 即日起至 2025年5月28日｜全品項冷萃系列享 30% OFF',
                '歡迎光臨門市或線上訂購，與我們一同細品這個夏日。'
            ]
        },
        {
            'publish_date': date(2025, 5, 21),
            'title': 'SipSavour｜期間限定 抹茶狂熱',
            'image': 'images/0521.jpg',
            'content': [
                '嚴選上等抹茶粉，融合冰涼口感，完美調製三款經典抹茶飲品：',
                '細膩打磨的【抹茶冰沙】，帶來極致清涼；',
                '香醇馥郁的【抹茶牛奶】，層層交疊奶香與茶韻；',
                '綿密濃郁的【抹茶鮮奶油特調】，讓每一口都回味無窮。',
                '每一杯，都是對抹茶的極致詮釋，每一口，都是夏日專屬的療癒時光',
                '✨ 限時限定｜ONLY 7 DAYS！'
            ]
        },
        {
            'publish_date': date(2025, 5, 14),
            'title': 'SipSavour｜早晨好食光',
            'image': 'images/0514.jpg',
            'content': [
                '春夏交替的清晨，怎麼能少了溫暖療癒的早午餐？',
                '帕尼尼烤雞三明治',
                '金黃酥脆的帕尼尼，夾入鮮嫩烤雞與清脆生菜，外酥內潤，簡單而美好',
                '切達起司火腿堡',
                '經典火腿與香濃切達起司，搭配蓬鬆麵包，每一口都是熟悉又溫柔的滋味。',
                '香草培根嫩蔬堡',
                '脆烤培根佐上義式香草醬，搭配鮮蔬層層堆疊，輕盈中帶點濃郁。',
                '全麥元氣火腿三明治',
                '全麥麵包搭配新鮮蔬菜與低脂火腿，清爽無負擔，專為忙碌的你而準備。',
                '早餐時段開賣，售完為止',
                '用一份晨間儀式，為自己準備一個溫柔又美好的開始。'
            ]
        },
        {
            'publish_date': date(2025, 5, 7),
            'title': 'SipSavour｜ 母親節限定 感謝有妳',
            'image': 'images/0507.jpg',
            'content': [
                '在這個屬於母親的特別日子，SipSavour 獻上最溫柔的祝福,',
                '一杯咖啡，一份心意，獻給世界上最溫暖的存在。',
                '即日起至 2025年5月12日，',
                '消費滿 500 元，即享 50% OFF 限量折扣券 一張。',
                '咖啡全品項不限口味使用',
                '甜點系列同步適用',
                '活動期間： 2025/5/7 – 5/13',
                '不妨以一杯溫熱的咖啡，陪媽媽一起，慢慢享受午後的溫柔時光。'
            ]
        },
        {
            'publish_date': date(2025, 4, 30),
            'title': 'SipSavour｜5/1勞動節限定',
            'image': 'images/0430.jpg',
            'content': [
                '今天，犒賞最努力的自己。',
                '用一杯咖啡，慰勞每一份認真；',
                '用兩杯咖啡，分享每一份溫暖。',
                '購買兩杯相同容量/冰熱/口味的飲料',
                '另外一杯由SipSavour招待(不限口味使用)',
                '活動期間： 2025/4/30-5/2',
                '不論是為了自己，或是為了一起打拼的好夥伴，'
                'SipSavour 都在這裡，陪你一起慶祝每一份努力的成果。'
            ]
        },
                {
            'publish_date': date(2025, 4, 23),
            'title': 'SipSavour｜Earth Day 特別企劃',
            'image': 'images/0423.png',
            'content': [
                '4月23日起，帶著你的環保杯與環保袋，',
                '一起加入友善地球的行列！',
                '自備環保杯，享飲品 10% 優惠',
                '自帶環保袋，當次購物 10% 折扣同步回饋。',
                '活動期間： 2025/4/23-4/29',
                '每一杯、每一次選擇，都是對地球最溫柔的承諾。'
            ]
        },
        {
            'publish_date': date(2025, 4, 16),
            'title': 'SipSavour｜奶昔新勢力崛起',
            'image': 'images/0416.jpg',
            'content': [
                '4/16 起，奶昔新體驗！',
                '☕ 醇香咖啡 X 雲朵奶蓋',
                '🍯 爆汁珍珠 X 香濃牛奶',
                '🍫 濃情巧克力 X 絲柔乳香',
                '活動期間： 2025/4/16-4/22',
                '甜在心，冰在手，從第一口就愛上！'
            ]
        },
        {
            'publish_date': date(2025, 4, 9),
            'title': 'SipSavour｜沙拉派對登場',
            'image': 'images/0409.png',
            'content': [
                '4/9 起，每日新鮮直送，美味加倍！！',
                '🥗陽光田園沙拉',
                '嚴選鮮採番茄、生菜與香草，清爽開胃，每一口都是陽光滋味。',
                '🌿 森野綠洲沙拉',
                '豐富綠意，搭配小黃瓜與嫩葉生菜，輕盈無負擔，讓你綠得剛剛好。',
                '🎶 繽紛活力沙拉',
                '多種蔬果交織出繽紛色彩，營養滿分，健康又飽足！',
            ]
        }
    ]

        # 加上分頁功能：每頁顯示 3 筆
    paginator = Paginator(news_list, 3)

    # 取得目前頁碼 (如果沒有就預設第 1 頁)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/index.html', {'page_obj': page_obj})
