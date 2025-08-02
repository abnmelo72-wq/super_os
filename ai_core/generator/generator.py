# ~/super_os/ai_core/generator/generator.py

import random

# ردود جاهزة كأمثلة مبدئية
basic_responses = {
    "open_browser": [
        "تمام! جاري فتح المتصفح...",
        "أعطيني لحظة، رح شغّلك المتصفح فوراً.",
        "لحظة، هي فتح المتصفح قدامك."
    ],
    "play_music": [
        "هي عم شغّل الموسيقى 🎵",
        "جهّز حالك لصوت حلو 😎",
        "تمام، شغّلتلك الأغنية!"
    ],
    "unknown": [
        "ممم ما فهمت تمامًا، ممكن توضحلي؟ 🤔",
        "فيك تعيد بصياغة تانية؟",
        "لسه عم أتعلم... عيدلي الطلب بطريقة تانية 😊"
    ]
}

# دالة التوليد
def generate_response(command_tag: str) -> str:
    return random.choice(basic_responses.get(command_tag, basic_responses["unknown"]))

# اختبار مباشر
if __name__ == "__main__":
    # جرب أمر معروف
    print(generate_response("open_browser"))

    # جرب أمر غير معروف
    print(generate_response("shutdown_pc"))
