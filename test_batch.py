import base64
from PIL import Image, ImageDraw, ImageFont
import io
import sys
import os
from dataclasses import dataclass
import json
import ast

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

def create_test_images(num_images=3):
    """创建多个测试图片"""
    images = []
    texts = [
        ["Hello OCR", "测试文本", "123456"],
        ["图片2", "Test Image", "789"],
        ["第三张", "Third", "文本测试"]
    ]
    
    try:
        # 尝试加载中文字体
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        ]
        
        font = None
        for path in font_paths:
            try:
                font = ImageFont.truetype(path, 24)
                break
            except:
                continue
                
        if font is None:
            font = ImageFont.load_default()
            
    except:
        font = ImageFont.load_default()

    for i in range(min(num_images, len(texts))):
        img = Image.new('RGB', (300, 150), color='white')
        d = ImageDraw.Draw(img)
        
        for j, (text, pos) in enumerate(zip(texts[i], [(10, 10), (10, 50), (10, 90)])):
            # 绘制白色轮廓
            for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
                x, y = pos[0] + offset[0], pos[1] + offset[1]
                d.text((x, y), text, fill='white', font=font)
            # 绘制黑色文字
            d.text(pos, text, fill='black', font=font)
        
        # 转换为base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        images.append(img_str)
        
        # 保存测试图片
        img.save(f'test_image_{i+1}.png')
    
    return images

def format_results(result):
    """格式化输出结果"""
    # 处理消息对象
    if hasattr(result, 'message'):
        result = result.message
    
    # 处理文本消息
    if isinstance(result, dict) and 'text' in result:
        return result['text']
    
    # 处理 json_object 字段
    if isinstance(result, dict) and 'json_object' in result:
        result = result['json_object']
    
    if not isinstance(result, dict):
        return f"返回信息: {result}"
    
    output = []
    if result.get("success"):
        output.append(f"批量处理结果:")
        output.append(f"{'='*50}")
        output.append(f"总处理数量: {result['total_processed']}")
        output.append(f"成功处理数量: {result['successful_count']}")
        
        for i, batch_result in enumerate(result['batch_results'], 1):
            output.append(f"\n图片 {i}:")
            output.append(f"{'-'*40}")
            if batch_result.get("success"):
                output.append(f"检测到文本数量: {batch_result['total_detected']}")
                output.append(f"处理时间: {batch_result['time_cost']:.3f}秒")
                output.append("\n检测到的文本:")
                
                for j, item in enumerate(batch_result['results'], 1):
                    output.append(f"  {j}. {item['text']}")
                    output.append(f"     置信度: {item['confidence']:.2%}")
                    pos = item['position']
                    output.append(f"     位置: ({pos['top_left'][0]:.0f}, {pos['top_left'][1]:.0f}) -> "
                                f"({pos['bottom_right'][0]:.0f}, {pos['bottom_right'][1]:.0f})")
            else:
                output.append(f"处理失败: {batch_result.get('error')}")
    else:
        output.append("处理失败:")
        output.append(f"错误信息: {result.get('error')}")
    
    return "\n".join(output)

def test_batch_ocr():
    """测试批量OCR功能"""
    print("开始批量OCR测试...\n")
    
    try:
        # 初始化环境和工具
        env = DifyPluginEnv()
        plugin = Plugin(env)
        session = SimpleSession()
        
        # 初始化工具
        provider = RapidocrToolProvider()
        tool = RapidocrToolTool(provider, session)
        print("✓ 工具初始化成功")
        
        # 创建测试图片
        image_data = create_test_images(3)  # 创建3张测试图片
        print(f"✓ 创建了 {len(image_data)} 张测试图片")
        
        # 调用OCR工具
        print("\n执行批量OCR识别...")
        params = {
            "image": ",".join(image_data),
            "batch": True
        }
        
        for message in tool._invoke(params):
            print("\n" + format_results(message))
                
        print("\n✓ 测试完成")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")

if __name__ == "__main__":
    test_batch_ocr() 