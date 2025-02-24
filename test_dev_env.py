import os
from dotenv import load_dotenv
from dify_plugin import Plugin, DifyPluginEnv

def test_dify_connection():
    try:
        # 加载环境变量
        load_dotenv()
        
        # 验证必要的环境变量
        required_vars = ['INSTALL_METHOD', 'REMOTE_INSTALL_HOST', 'REMOTE_INSTALL_PORT', 'REMOTE_INSTALL_KEY']
        for var in required_vars:
            if not os.getenv(var):
                print(f"✗ 缺少环境变量: {var}")
                return False
        
        # 测试Dify连接
        plugin = Plugin(DifyPluginEnv())
        print("✓ Dify Plugin 环境配置正确")
        return True
        
    except Exception as e:
        print(f"✗ Dify连接测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试Dify开发环境...\n")
    test_dify_connection() 