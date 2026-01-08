#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для инициализации Git репозитория
Запустите: python setup_git.py
"""

import subprocess
import os
import sys

def run_command(cmd, description):
    """Выполняет команду и выводит результат"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"ОШИБКА: {result.stderr}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"ОШИБКА при выполнении команды: {e}", file=sys.stderr)
        return False

def main():
    # Переходим в директорию скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Рабочая директория: {script_dir}")
    
    # Проверка наличия Git
    print("\n🔍 Проверка наличия Git...")
    if not run_command("git --version", "Проверка версии Git"):
        print("\n❌ Git не найден! Установите Git с https://git-scm.com/download/win")
        sys.exit(1)
    
    # Инициализация репозитория
    if os.path.exists(".git"):
        print("\n⚠️  Git репозиторий уже инициализирован")
        response = input("Переинициализировать? (y/n): ")
        if response.lower() != 'y':
            print("Отменено.")
            sys.exit(0)
    
    print("\n📦 Инициализация Git репозитория...")
    if not run_command("git init", "Инициализация репозитория"):
        sys.exit(1)
    
    # Добавление файлов
    print("\n📝 Добавление файлов...")
    if not run_command("git add .", "Добавление файлов в индекс"):
        sys.exit(1)
    
    # Проверка статуса
    print("\n📊 Статус репозитория:")
    run_command("git status", "Проверка статуса")
    
    # Создание первого коммита
    print("\n💾 Создание первого коммита...")
    commit_message = "Initial commit: Calorie Tracker application"
    if not run_command(f'git commit -m "{commit_message}"', "Создание коммита"):
        print("\n⚠️  Возможно, нет изменений для коммита или не настроен пользователь Git")
        print("Настройте Git пользователя командами:")
        print('  git config --global user.name "Ваше Имя"')
        print('  git config --global user.email "your.email@example.com"')
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ Git репозиторий успешно инициализирован!")
    print("="*60)
    
    print("\n📋 Следующие шаги:")
    print("1. Создайте репозиторий на GitHub:")
    print("   https://github.com/new")
    print("\n2. После создания репозитория выполните команды:")
    print("   git remote add origin https://github.com/ВАШ_USERNAME/ИМЯ_РЕПОЗИТОРИЯ.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n   (Замените ВАШ_USERNAME и ИМЯ_РЕПОЗИТОРИЯ на свои значения)")

if __name__ == "__main__":
    main()

