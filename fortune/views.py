# news/views.py
import random
from django.shortcuts import render
import random
from django.http import JsonResponse
from django.shortcuts import render

def daily_fortune(request):
    tarot_cards = get_tarot_cards()
    selected_card = random.choice(tarot_cards)

    return render(request, 'fortune/index.html', {
        'card': selected_card,
        'back_image': 'images/tarot_card/tarot_22.png',
    })

def draw_new_card(request):
    tarot_cards = get_tarot_cards()
    selected_card = random.choice(tarot_cards)

    return JsonResponse({
        'image_url': f"/static/{selected_card['image']}",
        'name': selected_card['name'],
        'description': selected_card['description'],
        'advice': selected_card['advice'],
    })

def get_tarot_cards():
    return [
        {
            'image': f'images/tarot_card/tarot_{i}.png',
            'name': name,
            'description': desc,
            'advice': advice,
        }
        for i, (name, desc, advice) in enumerate([
            ('愚者 (The Fool)', '冒險、開始新旅程', '敢於跳脫舒適圈，驚喜隨時來敲門。'),
            ('魔術師 (The Magician)', '創造力、掌控力', '今天你的點子特別靈光，快動手！'),
            ('女祭司 (The High Priestess)', '直覺、秘密', '保持神祕感，今天沉穩比衝動更好。'),
            ('皇后 (The Empress)', '豐饒、溫柔', '適合療癒自己，享受美好時光。'),
            ('皇帝 (The Emperor)', '紀律、掌控', '計畫未來，掌握主導權。'),
            ('教皇 (The Hierophant)', '傳統、信仰', '遵循規範會讓事情更順利。'),
            ('戀人 (The Lovers)', '愛情、選擇', '感情運旺，適合告白或修補關係。'),
            ('戰車 (The Chariot)', '勇往直前', '有行動力，適合一鼓作氣完成計畫。'),
            ('力量 (Strength)', '勇氣、耐心', '克服挑戰，慢慢來就是贏。'),
            ('隱士 (The Hermit)', '內省、智慧', '獨處沉澱，找到內心真正的聲音。'),
            ('命運之輪 (Wheel of Fortune)', '變化、機運', '迎接變化，好運即將到來。'),
            ('正義 (Justice)', '公正、平衡', '公平待人，今天因果特別明顯。'),
            ('吊人 (The Hanged Man)', '放下、等待', '轉念一想，局勢會開始改變。'),
            ('死神 (Death)', '結束、重生', '舊的不去，新的不來，勇敢告別。'),
            ('節制 (Temperance)', '平衡、協調', '適合調和矛盾，尋求中庸之道。'),
            ('惡魔 (The Devil)', '欲望、束縛', '小心誘惑，保持自律。'),
            ('塔 (The Tower)', '突變、震盪', '突發狀況多，保持冷靜應對。'),
            ('星星 (The Star)', '希望、療癒', '充滿希望，好運正在醞釀中。'),
            ('月亮 (The Moon)', '幻覺、迷惘', '有些事看不清，暫時按兵不動。'),
            ('太陽 (The Sun)',  '成就、喜悅', '開朗正能量，今天特別順利。'),
            ('審判 (Judgement)', '覺醒、審視', '檢視過去，為未來做好準備。'),
            ('世界 (The World)', '完成、圓滿', '收割成果，進入新階段。'),
        ])
    ]

