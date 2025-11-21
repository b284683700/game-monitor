"""
监控系统配置文件
请在这里填写你的GitHub信息
"""

# ============================================================
# GitHub配置（需要填写）
# ============================================================

# 你的GitHub Token（创建后填写）
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

# 你的Gist ID（创建后填写）
GIST_ID = "YOUR_GIST_ID"

# 你的GitHub用户名（用于网页访问）
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"

# 电脑名称（如果有多台电脑，每台设置不同的名称）
COMPUTER_NAME = "电脑1"

# ============================================================
# 上传设置
# ============================================================

# 状态上传间隔（秒）
UPLOAD_INTERVAL = 30

# 是否启用自动上传
ENABLE_UPLOAD = True

# ============================================================
# 配置说明
# ============================================================
"""
1. GITHUB_TOKEN: 
   - 在GitHub创建Personal Access Token
   - 需要勾选 'gist' 权限
   - 创建步骤见README.md

2. GIST_ID:
   - 创建一个新的Gist
   - 从URL中获取ID
   - 例如: https://gist.github.com/username/abc123 中的 abc123

3. GITHUB_USERNAME:
   - 你的GitHub用户名
   - 用于生成网页访问地址

4. COMPUTER_NAME:
   - 给每台电脑起个名字
   - 例如: "主机", "笔记本", "电脑1", "电脑2"
   - 多台电脑时用于区分

5. UPLOAD_INTERVAL:
   - 状态上传频率
   - 建议30-60秒
   - 太频繁可能被GitHub限流

6. ENABLE_UPLOAD:
   - True: 启用自动上传
   - False: 禁用上传（用于测试）
"""