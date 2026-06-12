# Message Templates

These are the standard message templates used for logging or Telegram notifications.

### 1. Startup Notification
```text
🚀 **AIRO Second Brain Runtime Started**
Status: {{ status }}
Sync Mode: {{ sync_mode }}
Time: {{ timestamp }}
```

### 2. State Change / Degraded Warning
```text
⚠️ **AIRO Second Brain State Change**
Previous State: {{ previous_state }}
Current State: {{ current_state }}
Reason: {{ reason }}
Time: {{ timestamp }}
```

### 3. Recovery Notification
```text
✅ **AIRO Second Brain Recovered**
State restored to Healthy.
Time: {{ timestamp }}
```

### 4. Queue Processed Notification
```text
📥 **Remote Queue Processed**
Items processed: {{ item_count }}
Results: {{ results_summary }}
Time: {{ timestamp }}
```

### 5. Sync Pushed (Only if Real Sync Enabled)
```text
🔄 **State Synced**
Commit: {{ commit_hash }}
Message: {{ commit_message }}
Time: {{ timestamp }}
```
