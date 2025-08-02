import re

def clean_text(text):
    """
    تنظف النص الناتج من تحويل الصوت إلى نص.
    """
    if not isinstance(text, str):
        return ""

    # إزالة الرموز الغريبة
    text = re.sub(r"[^\w\s,.!?؟]", "", text)

    # توحيد علامات الترقيم
    text = re.sub(r"\s*([,.!?؟])\s*", r"\1 ", text)

    # إزالة التكرار العشوائي للكلمات
    words = text.split()
    cleaned_words = []
    for i, word in enumerate(words):
        if i == 0 or word != words[i - 1]:
            cleaned_words.append(word)
    text = " ".join(cleaned_words)

    # إزالة فراغات زائدة
    text = re.sub(r"\s+", " ", text).strip()

    return text
