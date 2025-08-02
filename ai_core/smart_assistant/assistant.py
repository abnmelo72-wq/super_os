import os
import time
import traceback
from ai_core.audio_input.listen import listen
from ai_core.speech_to_text.transcribe import transcribe
from ai_core.command_executor.execute import execute_command
from ai_core.text_to_speech.speak import speak
from ai_core.memory.log import log_interaction
from ai_core.security.sanitize import sanitize_input
from ai_core.diagnostics.debug import report_error
from ai_core.self_learning.adapt import self_improve


def main():
    print("🎤 مساعدك الذكي جاهز! تحدث الآن...\n")

    while True:
        try:
            audio_file = listen()
            if not audio_file:
                continue

            text = transcribe(audio_file)
            print(f"🗣️ قلت: {text}")

            sanitized_text = sanitize_input(text)
            if "خروج" in sanitized_text or "أوقف" in sanitized_text:
                print("👋 إلى اللقاء!")
                break

            log_interaction(sanitized_text)
            response = execute_command(sanitized_text)
            self_improve(sanitized_text, response)

        except KeyboardInterrupt:
            print("\n⛔ تم إيقاف المساعد.")
            break
        except Exception as e:
            print(f"[⚠️] خطأ غير متوقع: {e}")
            traceback.print_exc()
            report_error(e)
            time.sleep(1)


if __name__ == "__main__":
    main()

