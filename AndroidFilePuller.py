#================================================================
# File Name: AndroidFilePuller.py
# Author: He Ronghua
# mail: heronghua1989@126.com
# Created Time: Fri Mar 14 13:28:44 2025
#================================================================
#!/usr/bin/env python

import os
import time
import subprocess
from pathlib import Path
from collections import defaultdict
import hashlib
import logging
from typing import List, Dict

class AndroidFilePuller:
    def __init__(self, configs: List[Dict], adb_cmd: str = "adb"):
        """
        :param configs: 监控配置列表
            [{
                "phone_dir": "/sdcard/DCIM",    # 手机监控目录
                "local_dir": "./downloads",      # 本地保存目录
                "check_interval": 5,             # 检查间隔（秒）
                "stable_checks": 3               # 稳定检测次数
            }]
        :param adb_cmd: adb命令路径
        """
        self.configs = self._validate_configs(configs)
        self.adb_cmd = adb_cmd
        self.trackers = defaultdict(dict)
        self.running = False
        self._init_logging()

    class FileTracker:
        def __init__(self):
            self.file_stats = defaultdict(lambda: {'size': -1, 'mtime': 0, 'counter': 0})

        def update(self, filepath: str, size: int, mtime: int) -> int:
            key = hashlib.md5(filepath.encode()).hexdigest()
            current = self.file_stats[key]
            
            if current['size'] == size and current['mtime'] == mtime:
                current['counter'] += 1
            else:
                current.update(size=size, mtime=mtime, counter=1)
            
            return current['counter']

        def remove(self, filepath: str):
            key = hashlib.md5(filepath.encode()).hexdigest()
            if key in self.file_stats:
                del self.file_stats[key]

    def _validate_configs(self, configs: List[Dict]) -> List[Dict]:
        """验证配置有效性"""
        required_keys = {'phone_dir', 'local_dir'}
        for conf in configs:
            if not required_keys.issubset(conf.keys()):
                raise ValueError(f"配置缺少必要参数: {required_keys - conf.keys()}")
            conf['check_interval'] = conf.get('check_interval', 5)
            conf['stable_checks'] = conf.get('stable_checks', 3)
        return configs

    def _init_logging(self):
        """初始化日志配置"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("android_puller.log"),
                logging.StreamHandler()
            ]
        )

    def _adb_command(self, cmd: List[str], check_output: bool = False):
        """执行ADB命令"""
        try:
            result = subprocess.run(
                [self.adb_cmd] + cmd,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip() if check_output else True
        except subprocess.CalledProcessError as e:
            logging.error(f"ADB命令失败: {e.cmd}\n错误信息: {e.stderr.strip()}")
            return None

    def _get_phone_files(self, phone_dir: str) -> List[str]:
        """获取手机目录文件列表"""
        cmd = ["shell", f"ls -1 {phone_dir}"]
        output = self._adb_command(cmd, check_output=True)
        return [f for f in output.split('\n') if f.strip()] if output else []

    def _get_file_stat(self, filepath: str):
        """获取文件状态信息"""
        stat_cmd = ["shell", f"stat -c '%s:%Y' {filepath} || ls -l --time-style=+%s {filepath} | awk '{{print $4\":\"$6}}'"]
        output = self._adb_command(stat_cmd, check_output=True)
        if not output or ':' not in output:
            return None, None
        return map(int, output.split(':', 1))

    def _process_file(self, config: Dict, filename: str):
        """处理单个文件"""
        phone_path = f"{config['phone_dir']}/{filename}"
        tracker = self.trackers[config['phone_dir']]
        
        size, mtime = self._get_file_stat(phone_path)
        if size is None or mtime is None:
            return

        counter = tracker.update(phone_path, size, mtime)
        
        if counter >= config['stable_checks']:
            local_dir = Path(config['local_dir'])
            local_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                # 拉取文件
                if self._adb_command(["pull", phone_path, str(local_dir)]):
                    # 删除手机文件
                    if self._adb_command(["shell", f"rm -f {phone_path}"]):
                        logging.info(f"成功处理: {phone_path} -> {local_dir}")
                        tracker.remove(phone_path)
            except Exception as e:
                logging.error(f"处理失败: {phone_path} - {str(e)}")

    def start(self):
        """启动监控守护进程"""
        self.running = True
        logging.info("Android文件监控守护进程启动")
        
        try:
            while self.running:
                for config in self.configs:
                    if not self.running:
                        break
                    
                    try:
                        files = self._get_phone_files(config['phone_dir'])
                        for filename in files:
                            self._process_file(config, filename)
                        time.sleep(config['check_interval'])
                    except Exception as e:
                        logging.error(f"目录监控异常 {config['phone_dir']}: {str(e)}")
                        time.sleep(5)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """停止监控"""
        self.running = False
        logging.info("正在停止监控守护进程...")

    def add_config(self, config: Dict):
        """动态添加监控配置"""
        self.configs.append(self._validate_configs([config])[0])
        logging.info(f"已添加监控配置: {config['phone_dir']}")

    def remove_config(self, phone_dir: str):
        """移除监控配置"""
        self.configs = [c for c in self.configs if c['phone_dir'] != phone_dir]
        if phone_dir in self.trackers:
            del self.trackers[phone_dir]
        logging.info(f"已移除监控配置: {phone_dir}")


if __name__ == "__main__":
    # 监控配置示例
    configs = [
        {
            "phone_dir": "/sdcard/DCIM",
            "local_dir": "./photos",
            "check_interval": 5,
            "stable_checks": 3
        },
        {
            "phone_dir": "/sdcard/Downloads",
            "local_dir": "./downloads",
            "check_interval": 10,
            "stable_checks": 2
        }
    ]

    # 创建监控实例
    puller = AndroidFilePuller(configs)
    
    try:
        # 启动监控
        puller.start()
    except KeyboardInterrupt:
        puller.stop()

    # 动态添加配置示例
    puller.add_config({
        "phone_dir": "/sdcard/Documents",
        "local_dir": "./documents",
        "check_interval": 15
    })
