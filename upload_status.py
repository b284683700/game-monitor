"""
游戏助手状态上传模块
用于将程序状态上传到GitHub Gist，供网页监控使用
"""

import requests
import json
from datetime import datetime
import time


class StatusUploader:
    """状态上传器"""
    
    def __init__(self, github_token, gist_id, computer_name="电脑1"):
        """
        初始化上传器
        
        Args:
            github_token: GitHub Personal Access Token
            gist_id: GitHub Gist ID
            computer_name: 电脑名称（用于区分多台电脑）
        """
        self.github_token = github_token
        self.gist_id = gist_id
        self.computer_name = computer_name
        self.last_upload_time = 0
        self.upload_interval = 30  # 上传间隔（秒）
        
    def should_upload(self):
        """判断是否应该上传"""
        current_time = time.time()
        if current_time - self.last_upload_time >= self.upload_interval:
            return True
        return False
    
    def upload_status(self, status_data):
        """
        上传状态到GitHub Gist
        
        Args:
            status_data: 状态数据字典，包含：
                - current_account: 当前账号
                - current_task: 当前任务
                - workbench_status: 工作台状态（可选）
                - hafnium_consumed: 哈夫币消耗（可选）
                - 其他自定义字段
        
        Returns:
            bool: 上传是否成功
        """
        try:
            # 检查是否需要上传
            if not self.should_upload():
                return True
            
            # 准备完整的状态数据
            full_data = {
                "computer_name": self.computer_name,
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_online": True,
                **status_data  # 合并传入的状态数据
            }
            
            # 准备API请求
            url = f"https://api.github.com/gists/{self.gist_id}"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # 文件名使用电脑名称，确保多台电脑数据不冲突
            filename = f"status_{self.computer_name.replace(' ', '_')}.json"
            
            data = {
                "files": {
                    filename: {
                        "content": json.dumps(full_data, ensure_ascii=False, indent=2)
                    }
                }
            }
            
            # 发送请求
            response = requests.patch(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                self.last_upload_time = time.time()
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] 状态上传成功")
                return True
            else:
                print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] 上传失败: HTTP {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] 上传超时")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] 网络错误: {e}")
            return False
        except Exception as e:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] 上传异常: {e}")
            return False
    
    def test_connection(self):
        """
        测试连接是否正常
        
        Returns:
            bool: 连接是否成功
        """
        try:
            url = f"https://api.github.com/gists/{self.gist_id}"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ GitHub连接测试成功")
                gist = response.json()
                print(f"   Gist名称: {gist.get('description', '无描述')}")
                print(f"   文件数量: {len(gist.get('files', {}))}")
                return True
            else:
                print(f"❌ GitHub连接测试失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ GitHub连接测试异常: {e}")
            return False


# 使用示例
if __name__ == "__main__":
    # 配置信息（需要替换为你的实际信息）
    GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # 替换为你的GitHub Token
    GIST_ID = "YOUR_GIST_ID"  # 替换为你的Gist ID
    COMPUTER_NAME = "电脑1"  # 可以自定义电脑名称
    
    # 创建上传器
    uploader = StatusUploader(GITHUB_TOKEN, GIST_ID, COMPUTER_NAME)
    
    # 测试连接
    print("正在测试GitHub连接...")
    if uploader.test_connection():
        print("\n开始上传测试数据...")
        
        # 测试数据
        test_data = {
            "current_account": "1079308174",
            "current_task": "特勤处运行中",
            "workbench_status": "2空闲/2生产中",
            "hafnium_consumed": 15000
        }
        
        # 上传数据
        if uploader.upload_status(test_data):
            print("\n✅ 测试成功！")
            print("你现在可以在网页上查看数据了")
        else:
            print("\n❌ 测试失败，请检查配置")
    else:
        print("\n❌ 连接失败，请检查：")
        print("1. GitHub Token是否正确")
        print("2. Gist ID是否正确")
        print("3. Token是否有gist权限")
        print("4. 网络连接是否正常")