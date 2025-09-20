import requests
import json
import os
from dotenv import load_dotenv
from collections import Counter
from datetime import datetime, timezone, timedelta
from error_handler import ErrorHandler, BrawlStarsAPIError

# 載入 .env 檔案
load_dotenv()

# 使用者輸入玩家ID
print("Brawl Stars 近期對戰統計")
print("=" * 40)
PLAYER_TAG = input("請輸入玩家標籤 (例如: 1ABCD0ABC): ").strip()
print(f"正在查詢玩家 #{PLAYER_TAG} 的戰鬥記錄...")

# API URL
url = f"https://api.brawlstars.com/v1/players/%23{PLAYER_TAG}/battlelog"
headers = {
    "Authorization": f"Bearer {os.getenv('BRAWLSTARS_API_KEY')}"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    data = response.json()
    
    # 分析對戰記錄
    battles = data.get('items', [])
    total_battles = len(battles)
    
    # 統計對戰期間
    battle_times = []
    for battle in battles:
        battle_time_str = battle.get('battleTime', '')
        if battle_time_str:
            # 解析 ISO 格式時間 (例如: 20250919T151317.000Z)
            try:
                # 解析 UTC 時間
                battle_time_utc = datetime.strptime(battle_time_str, '%Y%m%dT%H%M%S.%fZ')
                # 設定為 UTC 時區
                battle_time_utc = battle_time_utc.replace(tzinfo=timezone.utc)
                # 轉換為台灣時區 (UTC+8)
                taiwan_tz = timezone(timedelta(hours=8))
                battle_time_taiwan = battle_time_utc.astimezone(taiwan_tz)
                battle_times.append(battle_time_taiwan)
            except ValueError:
                # 如果解析失敗，嘗試沒有毫秒的格式
                try:
                    battle_time_utc = datetime.strptime(battle_time_str, '%Y%m%dT%H%M%SZ')
                    battle_time_utc = battle_time_utc.replace(tzinfo=timezone.utc)
                    taiwan_tz = timezone(timedelta(hours=8))
                    battle_time_taiwan = battle_time_utc.astimezone(taiwan_tz)
                    battle_times.append(battle_time_taiwan)
                except:
                    pass
    
    # 統計玩家常用的角色
    player_brawlers = Counter()
    # 完整的玩家標籤（用於比較
    full_player_tag = f"#{PLAYER_TAG}"
    
    for battle in battles:
        battle_data = battle.get('battle', {})
        
        # 檢查團隊模式
        if 'teams' in battle_data:
            for team in battle_data['teams']:
                for player in team:
                    if player.get('tag') == full_player_tag:
                        brawler_name = player.get('brawler', {}).get('name', 'Unknown')
                        player_brawlers[brawler_name] += 1
        
        # 檢查單人模式
        if 'players' in battle_data:
            for player in battle_data['players']:
                if player.get('tag') == full_player_tag:
                    brawler_name = player.get('brawler', {}).get('name', 'Unknown')
                    player_brawlers[brawler_name] += 1
    
    # 顯示統計結果
    print("=" * 40)
    print(f" 玩家ID: #{PLAYER_TAG}")
    print(f" 近期對戰場數: {total_battles}")

    
    # 顯示對戰期間（台灣時區）
    if battle_times:
        oldest_battle = min(battle_times)
        newest_battle = max(battle_times)
        print(f" 期間: {oldest_battle.strftime('%Y-%m-%d %H:%M')} 至 {newest_battle.strftime('%Y-%m-%d %H:%M')} (台灣時間)")
    else:
        print(" 期間: 無法解析時間資料")
    
    print("=" * 40)
    
    if player_brawlers:
        print(" 常用角色排名:")
        for i, (brawler, count) in enumerate(player_brawlers.most_common(), 1):
            print(f"  {i:2d}. {brawler}: {count} 次")
    else:
        print(" 未找到該玩家的戰鬥記錄")
    
    print("=" * 40)
    
except requests.exceptions.RequestException as e:
    error = ErrorHandler.handle_request_exception(e)
    ErrorHandler.print_error(error)
except json.JSONDecodeError as e:
    error = ErrorHandler.handle_json_decode_error(e)
    ErrorHandler.print_error(error)
except Exception as e:
    error = ErrorHandler.handle_general_error(e)
    ErrorHandler.print_error(error)
