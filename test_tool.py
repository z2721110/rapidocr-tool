import base64
from PIL import Image, ImageDraw, ImageFont
import io
import sys
import os
from dataclasses import dataclass

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rapidocr_tool import RapidocrToolTool
from provider.rapidocr_tool import RapidocrToolProvider
from dify_plugin import Plugin, DifyPluginEnv

@dataclass
class SimpleSession:
    """简单的会话类，用于测试"""
    app_id: str = "test_app"
    conversation_id: str = "test_conversation"
    provider_id: str = "test_provider"
    provider_name: str = "test"
    tool_name: str = "rapidocr-tool"

def create_test_image():
    """创建一个包含多行文字的测试图片"""
    img = Image.new('RGB', (300, 150), color='white')
    d = ImageDraw.Draw(img)
    
    try:
        # 尝试加载中文字体
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",  # Windows 下的黑体
            "C:/Windows/Fonts/simsun.ttc",   # Windows 下的宋体
            "C:/Windows/Fonts/msyh.ttc",     # Windows 下的微软雅黑
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux 下的 Droid 字体
        ]
        
        font = None
        for path in font_paths:
            try:
                font = ImageFont.truetype(path, 24)  # 增大字体大小
                break
            except:
                continue
                
        if font is None:
            font = ImageFont.load_default()
            
    except:
        font = ImageFont.load_default()
    
    texts = [
        ("Hello OCR", (10, 10)),
        ("测试文本", (10, 50)),
        ("123456", (10, 90))
    ]
    
    # 使用黑色文字，增加对比度
    for text, pos in texts:
        # 绘制白色轮廓增加对比度
        for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
            x, y = pos[0] + offset[0], pos[1] + offset[1]
            d.text((x, y), text, fill='white', font=font)
        # 绘制黑色文字
        d.text(pos, text, fill='black', font=font)
    
    # 转换为base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # 保存测试图片用于检查
    img.save('test_image.png')
    
    return img_str

def test_ocr_tool():
    """测试OCR工具"""
    print("开始测试OCR工具...\n")
    
    try:
        # 初始化环境和工具
        env = DifyPluginEnv()
        plugin = Plugin(env)
        
        # 创建简单会话
        session = SimpleSession()
        
        # 初始化工具
        provider = RapidocrToolProvider()
        tool = RapidocrToolTool(provider, session)
        print("✓ 工具初始化成功")
        
        # 创建测试图片
        image_data = create_test_image()
        print("✓ 测试图片创建成功")
        
        # 调用OCR工具
        print("\n执行OCR识别...")
        params = {"image": image_data}
        
        for message in tool._invoke(params):
            result = message.message
            print("\n识别结果:")
            print("-" * 50)
            
            if isinstance(result, dict):
                if result.get("success"):
                    print(f"总检测文本数: {result['total_detected']}")
                    print(f"处理时间: {result['time_cost']:.3f}秒")
                    print("\n检测到的文本:")
                    
                    for i, item in enumerate(result['results'], 1):
                        print(f"\n文本 {i}:")
                        print(f"  内容: {item['text']}")
                        print(f"  置信度: {item['confidence']:.4f}")
                        print("  位置: ")
                        for pos_name, coords in item['position'].items():
                            print(f"    {pos_name}: ({coords[0]:.1f}, {coords[1]:.1f})")
                else:
                    print("处理失败:")
                    print(f"错误类型: {result.get('error_type')}")
                    print(f"错误信息: {result.get('error')}")
            else:
                print("返回信息:", result)
                
        print("\n✓ 测试完成")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")

if __name__ == "__main__":
    test_ocr_tool() 