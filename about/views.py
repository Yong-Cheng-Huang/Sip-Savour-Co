from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def about_view(request):
    return render(request, 'about/about.html')

@login_required
def feature_detail(request, feature_id):
    # 特色詳細資料
    features = {
        'tea': {
            'title': '嚴選茶葉',
            'image': 'images/about/tea.jpg',
            'description': '我們嚴選來自台灣各高山茶區的優質茶葉，每一片茶葉都經過嚴格的品質把關，確保為您帶來最純粹的茶香體驗。',
            'details': [
                '精選台灣高山茶區茶葉',
                '嚴格的品質控管流程',
                '專業的茶葉保存技術',
                '定期更新茶葉庫存'
            ],
            'benefits': [
                '香氣濃郁持久',
                '口感回甘順口',
                '無農藥殘留',
                '新鮮度保證'
            ],
            'related_items': [
                {
                    'name': '經典熱紅茶',
                    'image': 'images/about/tea/black-tea.jpg',
                    'description': '來自阿里山的高山紅茶，茶香濃郁，甘醇順口，餘韻悠長。'
                },
            ]
        },
        'ingredients': {
            'title': '天然原料',
            'image': 'images/about/ingredients.jpg',
            'description': '我們堅持使用天然食材，拒絕添加人工香料與色素，讓每一杯飲品都充滿自然的風味。',
            'details': [
                '嚴選天然食材',
                '無添加人工香料',
                '無添加人工色素',
                '定期檢驗食材品質'
            ],
            'benefits': [
                '健康無負擔',
                '自然風味',
                '安心飲用',
                '品質保證'
            ],
            'related_items': [
                {
                    'name': '夏日柑橘莓果氣泡飲',
                    'image': 'images/about/ingredients/fruit-tea.jpg',
                    'description': '嚴選新鮮柑橘與莓果，融合微氣泡的輕盈口感，清新自然，適合盛夏的午後時光。'
                },
                {
                    'name': '地中海海鮮番茄義大利麵',
                    'image': 'images/about/ingredients/spaghetti.jpg',
                    'description': '使用天然木薯粉製作，口感Q彈。'
                }
            ]
        },
        'process': {
            'title': '專業製程',
            'image': 'images/about/process.jpg',
            'description': '我們採用標準化的製程，從原料選擇到成品製作，每個環節都經過嚴格的品質控管。',
            'details': [
                '標準化製作流程',
                '專業設備控溫',
                '嚴格的衛生管理',
                '定期設備維護'
            ],
            'benefits': [
                '品質穩定',
                '衛生安全',
                '效率提升',
                '一致性保證'
            ],
            'related_items': [
                {
                    'name': '專業茶具',
                    'image': 'images/about/process/cups.jpg',
                    'description': '使用專業茶具，確保每杯茶的最佳風味。'
                },
                {
                    'name': '溫度控制',
                    'image': 'images/about/process/kitchen-fire.jpg',
                    'description': '精確的溫度控制，讓茶葉完美釋放香氣。'
                }
            ]
        },
        'service': {
            'title': '貼心服務',
            'image': 'images/about/service.jpg',
            'description': '我們提供客製化的服務，根據每位顧客的需求，打造專屬的茶飲體驗。',
            'details': [
                '客製化服務',
                '專業諮詢',
                '貼心建議',
                '售後服務'
            ],
            'benefits': [
                '個人化體驗',
                '專業建議',
                '即時回應',
                '滿意保證'
            ],
            'related_items': [
                {
                    'name': '會員服務',
                    'image': 'images/about/service/service.jpg',
                    'description': '專屬會員優惠與服務。'
                },
                {
                    'name': '客製化飲品',
                    'image': 'images/about/service/customize.jpg',
                    'description': '根據您的喜好調整飲品配方。'
                }
            ]
        }
    }

    feature = features.get(feature_id)
    if not feature:
        return render(request, '404.html')

    return render(request, 'about/feature_detail.html', {'feature': feature})