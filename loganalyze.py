def analyze_user_activity(log_file_path: str) -> dict:
    import os
    default_result = {
        "total_users": 0,
        "action_counts": {},
        "most_active_user": None,
        "average_session_time": 0.0
    }
    
    if not os.path.exists(log_file_path):
        return default_result

    users = set()
    action_counts = {}
    user_activity_counts = {}
    total_duration = 0.0
    valid_session_count = 0

    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            
            if len(parts) != 4:
                continue
                
            timestamp, user_id, action, duration_str = parts
            
            try:
                duration = float(duration_str)
            except ValueError:
                continue
                
            users.add(user_id)
            
            action_counts[action] = action_counts.get(action, 0) + 1
            
            user_activity_counts[user_id] = user_activity_counts.get(user_id, 0) + 1
            
            if duration > 0:
                total_duration += duration
                valid_session_count += 1

    
    if not users:
        return default_result

    most_active_user = max(user_activity_counts, key=user_activity_counts.get)
    
    average_session_time = (total_duration / valid_session_count) if valid_session_count > 0 else 0.0

    return {
        "total_users": len(users),
        "action_counts": action_counts,
        "most_active_user": most_active_user,
        "average_session_time": round(average_session_time, 2)
    }
    

if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}
