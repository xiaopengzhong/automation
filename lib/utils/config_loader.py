#@File   : .py
#@Time   : 2025/8/11 18:16
#@Author : 
#@Software: PyCharm
# 读取数据

import os
import logging
import yaml
from pathlib import Path  # 提供面向对象的文件路径操作
from copy import deepcopy  # 用于深拷贝字典

# 获取当前模块的日志记录器
logger = logging.getLogger(__name__)




def load_yaml(file_path):
    """加载 YAML 文件，如果文件不存在或格式错误则抛出异常"""
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件不存在: {file_path}")
    try:
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ValueError(f"YAML 文件内容必须是字典: {file_path}")
            return data
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 格式错误: {file_path} - {e}")


def deep_merge_dicts(base, override):
    """递归合并两个字典（深拷贝安全）

    Args:
        base (dict): 基础字典
        override (dict): 要覆盖的字典

    Returns:
        dict: 合并后的新字典（不会修改原始字典）
    """
    result = deepcopy(base)  # 防止污染原始数据
    for k, v in override.items():
        # 如果双方的值都是字典，则递归合并
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = deep_merge_dicts(result[k], v)
        else:
            result[k] = v  # 直接覆盖
    return result


def get_config():
    """加载并合并配置文件（主配置 + 环境配置）

    优先级规则：
        1. 环境变量 CONFIG_ENV 指定环境（最高优先级）
        2. 主配置中的 env 字段（默认值）
        3. 默认使用 dev 环境（保底值）

    Returns:
        dict: 包含 env 和合并后配置的字典

    Raises:
        FileNotFoundError: 主配置文件不存在时抛出
    """
    # 获取项目根目录（假设此文件在 project_root/src/utils/ 下）
    project_root = Path(__file__).resolve().parents[2]  # 上溯两级到项目根
    conf_dir = project_root / "conf"  # 配置文件目录

    # 1. 加载主配置（必须存在）
    main_config_path = conf_dir / "config.yaml"
    if not main_config_path.exists():
        raise FileNotFoundError(f"主配置文件不存在: {main_config_path}")
    main_config = load_yaml(main_config_path)

    # 2. 确定当前环境（环境变量 > 主配置 > 默认dev）
    env = os.environ.get("CONFIG_ENV", main_config.get("env", "dev"))

    # 3. 加载环境配置（可选）
    env_config_path = conf_dir / "env" / f"config_{env}.yaml"
    env_config = load_yaml(env_config_path) if env_config_path.exists() else {}

    # 4. 合并配置（环境配置覆盖主配置）
    final_config = deep_merge_dicts(main_config, env_config)

    return {
        "env": env,  # 当前环境标识
        "config": final_config  # 最终合并配置
    }


if __name__ == "__main__":
    # 测试用例
    print(load_yaml('../../case_data/api/user/payload.yaml'))
    cfg_info = get_config()
    print(f"当前环境: {cfg_info['env']}")
    print(f"Base URL: {cfg_info['config']['api']['base_url']}")

    print(load_yaml('../../case_data/api/user/product.yaml')['search_product'])