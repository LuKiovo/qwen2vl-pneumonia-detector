from modelscope.hub.api import HubApi
from modelscope.hub.constants import ModelVisibility

# 请务必替换成你自己的 SDK 访问令牌，它通常以 'ms-' 开头
YOUR_ACCESS_TOKEN = "ms-68adc0aa-4d29-44c6-a251-6821c9299f11"

YOUR_USERNAME = "lyeroq"
MODEL_NAME = "Qwen2-VL-Pneumonia-Finetuned"
LOCAL_MODEL_DIR = "/root/autodl-tmp/merged_model"

# 初始化API并登录
api = HubApi()
# 修正点：直接传入Token作为位置参数
api.login(YOUR_ACCESS_TOKEN)

repo_id = f"{YOUR_USERNAME}/{MODEL_NAME}"

# 检查模型仓库是否存在，如果不存在则创建
try:
    api.get_model(repo_id)
    print(f"模型仓库 '{repo_id}' 已存在，将直接上传文件。")
except Exception:
    print(f"模型仓库 '{repo_id}' 不存在，正在创建...")
    api.create_model(
        model_id=repo_id,
        visibility=ModelVisibility.PUBLIC,
        license='apache-2.0',
        chinese_name="Qwen2-VL 肺炎X光片诊断助手"
    )
    print(f"模型仓库 '{repo_id}' 创建成功！")

print("正在上传模型文件，请耐心等待...")
api.upload_folder(
    repo_id=repo_id,
    folder_path=LOCAL_MODEL_DIR,
    commit_message="Initial upload of merged Qwen2-VL-Pneumonia model"
)
print(f"✅ 模型已成功上传至: https://modelscope.cn/models/{repo_id}")
