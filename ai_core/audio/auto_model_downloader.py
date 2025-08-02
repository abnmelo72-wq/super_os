import os
import whisper

def get_user_language():
    # يمكن استبداله لاحقًا بكود كشف لغة المستخدم الحقيقي
    return "ar"  # فرضًا اللغة عربية الآن

def select_model(language_code):
    if language_code in ["ar", "de", "ru", "ja"]:
        return "medium"  # نماذج متوسطة تعطي دقة أفضل للغات غير الإنجليزية
    else:
        return "base"  # سريع وخفيف، مناسب للغات إنجليزية أو أجهزة ضعيفة

def download_model_if_needed(model_name):
    model_path = os.path.expanduser(f"~/.cache/whisper/{model_name}.pt")
    if not os.path.exists(model_path):
        print(f"[+] جاري تحميل نموذج Whisper: {model_name}...")
        whisper.load_model(model_name)
        print("[✓] تم تحميل النموذج بنجاح.")
    else:
        print("[✓] النموذج موجود مسبقًا، لا حاجة للتحميل.")

if __name__ == "__main__":
    user_lang = get_user_language()
    model = select_model(user_lang)
    download_model_if_needed(model)
