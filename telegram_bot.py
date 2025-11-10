from telethon import TelegramClient, events
import sys

print("Importing libraries...")

api_id = 34825182
api_hash = 'cca8421e42f03c10bccdffddf07be13b'
session_name = 'rio_session'

TRACKING_MAP = {
    -5030834670: [-5077669868],  # id group tracking => id group push tin nhắn
    -1001494331837: [-5077669868],
    -1001348564602: [-5077669868] 
}

client = TelegramClient(session_name, api_id, api_hash)

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
                await client.send_file(
                    target, 
                    message.media,
                    caption=message.text
                )
                print(f"[SUCCESS] Sent media copy to {target}")
            elif message.text:
                await client.send_message(target, message.text)
                print(f"[SUCCESS] Sent text copy to {target}")
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
