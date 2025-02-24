import dify_plugin
import inspect

# 打印模块属性
print("模块属性:")
print("-" * 50)
for attr in dir(dify_plugin):
    if not attr.startswith('__'):
        print(f"{attr}: {type(getattr(dify_plugin, attr))}")

# 打印版本信息
print("\n版本信息:")
print("-" * 50)
print(f"dify_plugin version: {dify_plugin.__version__ if hasattr(dify_plugin, '__version__') else 'unknown'}")

# 检查关键类
print("\n可用的类:")
print("-" * 50)
for name, obj in inspect.getmembers(dify_plugin, inspect.isclass):
    print(f"{name}: {obj.__module__}") 