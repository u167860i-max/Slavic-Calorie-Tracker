@echo off
chcp 65001 >nul
echo ============================================================
echo Инициализация Git репозитория
echo ============================================================
echo.

echo Проверка наличия Git...
git --version
if errorlevel 1 (
    echo ОШИБКА: Git не найден! Установите Git с https://git-scm.com/download/win
    pause
    exit /b 1
)
echo.

echo Инициализация Git репозитория...
git init
if errorlevel 1 (
    echo ОШИБКА при инициализации
    pause
    exit /b 1
)
echo.

echo Удаление проблемной папки git caltrack (если содержит вложенный репозиторий)...
if exist "git caltrack\.git" (
    echo Найден вложенный репозиторий, удаляю...
    rmdir /s /q "git caltrack\.git" 2>nul
)

echo Добавление файлов...
git add .
if errorlevel 1 (
    echo.
    echo ВНИМАНИЕ: Возможна проблема с папкой git caltrack
    echo Попробуйте удалить папку git caltrack вручную, если она не нужна
    echo Или выполните команды вручную:
    echo   git add .gitignore README.md setup_git.* аааа3.py images/
    pause
    exit /b 1
)
echo.

echo Статус репозитория:
git status
echo.

echo Создание первого коммита...
git commit -m "Initial commit: Calorie Tracker application"
if errorlevel 1 (
    echo.
    echo ВНИМАНИЕ: Возможно, не настроен пользователь Git
    echo Выполните команды:
    echo   git config --global user.name "Ваше Имя"
    echo   git config --global user.email "your.email@example.com"
    echo   Затем запустите этот скрипт снова
    pause
    exit /b 1
)
echo.

echo ============================================================
echo Git репозиторий успешно инициализирован!
echo ============================================================
echo.
echo Следующие шаги:
echo 1. Создайте репозиторий на GitHub: https://github.com/new
echo 2. После создания выполните команды:
echo    git remote add origin https://github.com/ВАШ_USERNAME/ИМЯ_РЕПОЗИТОРИЯ.git
echo    git branch -M main
echo    git push -u origin main
echo.
pause

