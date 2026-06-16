# Get笔记推送脚本模板

## 使用场景

anlects-review 阶段保存时需要将本地 `.md` 文件同步推送到 Get笔记。以下为已验证可用的 Python 推送脚本模板。

## 模板

```python
import json, urllib.request, urllib.error, time

# 1. 读取凭证
with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
    cfg = json.load(f)

api_key = cfg["getnote"]["api_key"]
client_id = cfg["getnote"]["client_id"]

# 2. 读取待推送内容
with open("/path/to/file.md") as f:
    content = f.read()

# 3. 推送（注意间隔 ≥ 2 秒）
url = "https://openapi.biji.com/open/api/v1/resource/note/save"
data = json.dumps({
    "title": "标题",
    "content": content,  # 完整正文，不可摘要
    "note_type": "plain_text",
    "tags": ["标签1", "标签2", "标签3"],  # ≤ 5 个
    "parent_id": 0
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={
    "Authorization": api_key,      # 裸 key，无 Bearer 前缀
    "X-Client-ID": client_id,       # 必须同时携带
    "Content-Type": "application/json"
})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        nid = result.get('data', {}).get('note_id', '?')
        print(f"OK note_id={nid}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}")
except Exception as e:
    print(f"ERR: {e}")
```

## 踩坑记录

| 陷阱 | 错误做法 | 正确做法 |
|------|---------|---------|
| Base URL | `noteim.laffitto2.com` | `openapi.biji.com` |
| Auth 前缀 | `Bearer gk_live_xxx` | `gk_live_xxx`（裸 key） |
| Config key | `cfg["getnote"]["token"]` | `cfg["getnote"]["api_key"]` |
| Shell 传参 | `export KEY=...` / 命令行传参 | 硬编码在脚本内，运行后删除 |
| Headers | 仅带 Authorization | 同时带 Authorization + X-Client-ID |
| 标签数量 | 6+ 个 | ≤ 5 个 |
| 推送间隔 | < 2 秒连续推送 | time.sleep(2) |
| 内容 | 摘要/索引占位符 | 完整正文（与 .md 文件一致） |
