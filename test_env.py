def test_dependencies():
    try:
        # 测试Dify插件SDK
        from dify_plugin import Plugin
        print("✓ Dify Plugin SDK 已安装")

        # 测试OCR环境
        from rapidocr_onnxruntime import RapidOCR
        ocr = RapidOCR()
        print("✓ RapidOCR 环境正常")

        # 测试图像处理
        from PIL import Image
        print("✓ Pillow 已安装")

        # 测试数值计算
        import numpy as np
        print("✓ Numpy 已安装")

        print("\n✓ 所有依赖安装成功!")
        return True

    except Exception as e:
        print(f"✗ 环境检查失败: {str(e)}")
        return False

def test_ocr_functionality():
    try:
        from rapidocr_onnxruntime import RapidOCR
        import numpy as np
        from PIL import Image
        
        # 创建一个简单的测试图片
        img = Image.new('RGB', (100, 30), color='white')
        ocr = RapidOCR()
        
        # 测试OCR基本功能
        result, elapse = ocr(img)
        print("✓ OCR功能测试通过")
        return True

    except Exception as e:
        print(f"✗ OCR功能测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始环境检测...\n")
    
    deps_ok = test_dependencies()
    if deps_ok:
        print("\n开始OCR功能测试...\n")
        test_ocr_functionality() 