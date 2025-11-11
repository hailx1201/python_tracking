from telethon import TelegramClient, events
import sys
import re
from deep_translator import GoogleTranslator

print("Importing libraries...")

api_id = 34825182
api_hash = 'cca8421e42f03c10bccdffddf07be13b'
session_name = 'rio_session'

TRACKING_MAP = {
    -4978036009: [-5060729291],
    -1001494331837: [-5060729291],
    -1001348564602: [-5060729291] 
}

client = TelegramClient(session_name, api_id, api_hash)

def translate_text(text):
    if not text or text.strip() == "":
        return text
    
    try:
        protected_words = {}
        uppercase_pattern = r'\b[A-Z]{2,}\b'
        
        def replace_with_placeholder(match):
            word = match.group()
            index = len(protected_words)
            placeholder = f"◆{index}◆"
            protected_words[index] = word
            return placeholder
        
        modified_text = re.sub(uppercase_pattern, replace_with_placeholder, text)
        translator = GoogleTranslator(source='en', target='vi')
        translated = translator.translate(modified_text)
        
        for index, original_word in protected_words.items():
            placeholder = f"◆{index}◆"
            translated = translated.replace(placeholder, original_word)
        
        return translated
        
    except Exception as e:
        print(f"[TRANSLATION ERROR] {e}")
        return text

@client.on(events.NewMessage(chats=list(TRACKING_MAP.keys())))
async def handler(event):
    message = event.message
    source_id = event.chat_id
    print(f"\n[NEW MESSAGE] from {source_id}:")
    print(f"   Text: {message.text or '<no text>'}")
    print(f"   Media: {message.media if message.media else '<no media>'}")
    
    targets = TRACKING_MAP.get(source_id, [])
    for target in targets:
        try:
            if message.media:
                translated_caption = translate_text(message.text) if message.text else None
                print(f"   Original caption: {message.text}")
                print(f"   Translated caption: {translated_caption}")
                
                await client.send_file(
                    target, 
                    message.media,
                    caption=translated_caption
                )
                print(f"[SUCCESS] Sent media copy with translated caption to {target}")
            elif message.text:
                translated_text = translate_text(message.text)
                print(f"   Original text: {message.text}")
                print(f"   Translated text: {translated_text}")
                
                await client.send_message(target, translated_text)
                print(f"[SUCCESS] Sent translated text copy to {target}")
            else:
                print(f"[SKIP] Empty message")
        except Exception as e:
            print(f"[FAILED] Could not send to {target}: {e}")

async def main():
    print("=" * 50)
    print("Starting Telegram Bot...")
    print("=" * 50)
    await client.start()
    print("[OK] Client started successfully!")
    print("\n[TRACKING CONFIGURATION]:")
    for source, targets in TRACKING_MAP.items():
        print(f"  {source} -> {targets}")
    print("\nWaiting for new messages...\n")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
