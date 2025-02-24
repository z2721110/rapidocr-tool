# Dify RapidOCR 插件

## 基本信息
- **作者:** zhouyang
- **版本:** 0.0.1
- **类型:** tool
- **适用 Dify 版本:** >= 0.3.0

## 功能简介
这是一个基于 RapidOCR 的 Dify 插件，提供高精度的文字识别功能。支持中英文混合文本识别，可以进行单图或批量处理，并提供文本位置和置信度信息。

### 主要特性
- 支持中英文混合文本识别
- 支持单图和批量处理
- 提供文本位置和置信度信息
- 自动图像预处理优化
- 高精度文本定位

## 安装要求
- Python 3.8+
- Dify Plugin SDK
- RapidOCR ONNX Runtime
- Pillow >= 10.0.0

### 依赖安装
```bash
pip install -r requirements.txt
```

## 使用方法

### 单图处理
```python
params = {
    "image": "base64_encoded_image_data",  # Base64编码的图片数据
    "batch": False
}
```

### 批量处理
```python
params = {
    "image": "base64_image1,base64_image2,base64_image3",  # 逗号分隔的多个Base64图片数据
    "batch": True
}
```

### 返回格式示例
```
批量处理结果
==================================================
总处理数量: 3
成功处理数量: 3

图片 1
----------------------------------------
检测到文本数量: 3
处理时间: 1.211秒

检测到的文本:
  1. Hello OCR
      置信度: 95.06%
      位置: (9, 13) -> (119, 34)
  2. 测试文本
      置信度: 99.99%
      位置: (9, 49) -> (107, 76)
```

## 技术特性

### 图像预处理
- 自动转换为RGB模式
- 自动调整对比度和锐度
- 智能缩放以确保文本清晰度
- 优化文本边缘检测

### 性能优化
- 批量处理时的内存优化
- 图像预处理加速
- 识别结果缓存

### 错误处理
- 空图片数据检查
- 图片格式验证
- Base64解码错误处理
- OCR识别异常处理

## 项目结构
```
rapidocr-tool/
├── tools/
│   ├── rapidocr_tool.py      # 主要工具实现
│   └── rapidocr-tool.yaml    # 工具配置
├── provider/
│   └── rapidocr_tool.py      # 提供者实现
├── tests/
│   ├── test_ocr_tool.py      # 单元测试
│   └── test_batch.py         # 批处理测试
├── README.md                 # 使用文档
└── PRIVACY.md               # 隐私政策
```

## 测试
运行单元测试：
```bash
python -m unittest tests/test_ocr_tool.py
```

运行批处理测试：
```bash
python test_batch.py
```

## 隐私说明
- 所有图片处理均在本地完成
- 不会上传或存储任何图片数据
- 处理完成后立即清理内存
- 详细隐私政策请参考 PRIVACY.md

## 版本历史
### v0.0.1 (当前版本)
- 初始版本发布
- 支持中英文文本识别
- 支持单图和批量处理
- 提供详细的位置和置信度信息

## 已知问题
- 暂无

## 计划功能
- [ ] 添加更多图像预处理选项
- [ ] 提供自定义输出格式
- [ ] 优化处理速度
- [ ] 添加更多语言支持

## 贡献指南
欢迎提交 Issue 和 Pull Request。在提交代码前，请确保：
1. 通过所有单元测试
2. 添加适当的测试用例
3. 更新相关文档

## 许可证
MIT License

## 联系方式
如有问题，请提交 Issue。

## 致谢
- RapidOCR 项目
- Dify 团队



