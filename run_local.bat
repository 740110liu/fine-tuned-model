@echo off
echo ========================================
echo 自动化专业导师模型 - 本地微调
echo GPU: RTX 3050 4GB
echo ========================================
echo.

echo [1/3] 安装依赖...
pip install -q transformers peft datasets accelerate bitsandbytes trl
if %errorlevel% neq 0 (
    echo 依赖安装失败！
    pause
    exit /b 1
)

echo [2/3] 开始微调...
python scripts\local_finetune.py
if %errorlevel% neq 0 (
    echo 微调失败！
    pause
    exit /b 1
)

echo [3/3] 完成！
echo 模型已保存到: automation_advisor_lora
echo.
pause
