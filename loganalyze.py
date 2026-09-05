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
    user_total_duration = {}
    total_login_time = 0.0
    login_count = 0

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
            
            user_total_duration[user_id] = user_total_duration.get(user_id, 0.0) + duration
            
            if action == "login":
                total_login_time += duration
                login_count += 1

    if not users:
        return default_result

    most_active_user = max(user_total_duration, key=user_total_duration.get)
    
    average_session_time = (total_login_time / login_count) if login_count > 0 else 0.0

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
