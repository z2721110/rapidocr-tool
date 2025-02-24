import base64
from PIL import Image, ImageDraw, ImageFont
import io
from rapidocr_onnxruntime import RapidOCR

def create_test_image():
    """创建一个包含文字的测试图片"""
    # 创建一个白色背景的图片
    img = Image.new('RGB', (200, 50), color='white')
    d = ImageDraw.Draw(img)
    
    # 添加文字
    text = "Hello OCR"
    d.text((10,10), text, fill='black')
    
    # 转换为base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str, img

def format_float(value, precision=3):
    """格式化浮点数"""
    try:
        return str(round(float(value), precision))
    except (TypeError, ValueError):
        return str(value)

def format_time(time_list):
    """格式化时间显示"""
    if isinstance(time_list, list):
        total_time = sum(time_list)
        return format_float(total_time, 3)
    return format_float(time_list, 3)

def test_ocr():
    """测试OCR功能"""
    try:
        # 创建测试图片
        img_base64, img = create_test_image()
        print("✓ 测试图片创建成功")
        
        # 初始化OCR
        ocr = RapidOCR()
        print("✓ OCR引擎初始化成功")
        
        # 执行OCR识别
        result, elapse = ocr(img)
        print("\n识别结果:")
        
        success = True
        if result and len(result) > 0:
            for detection in result:
                box, text, confidence = detection
                print("文本:", text)
                print("置信度:", format_float(confidence, 4))
                print("位置坐标:")
                for i, (x, y) in enumerate(box, 1):
                    print(f"  点{i}: ({x}, {y})")  # 直接打印坐标值
                print("-" * 20)
        else:
            print("未检测到文本")
            success = False
            
        print("耗时:", format_time(elapse), "秒")
        
        # 保存测试图片供查看
        img.save('test_image.png')
        print("\n✓ 测试图片已保存为 'test_image.png'")
        
        if success:
            print("\n✓ 测试成功!")
            print("\nBase64图片数据片段(用于插件测试):")
            print(img_base64[:50] + "...")
            return img_base64
            
        return None
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return None

if __name__ == "__main__":
    print("开始OCR功能测试...\n")
    test_ocr() 