@echo off
chcp 65001 >nul
echo ============================================================
echo Подключение к GitHub и загрузка кода
echo ============================================================
echo.

echo Удаление проблемной папки git caltrack...
if exist "git caltrack" (
    rmdir /s /q "git caltrack" 2>nul
    echo Папка удалена
)

echo.
echo Добавление файлов в Git...
git add .gitignore
git add README.md
git add setup_git.py
git add setup_git.bat
git add setup_git.ps1
git add push_to_github.bat
git add аааа3.py
git add images/

echo.
echo Статус репозитория:
git status

echo.
echo Создание коммита (если есть изменения)...
git commit -m "Initial commit: Slavic Calorie Tracker application" 2>nul
if errorlevel 1 (
    echo Коммит не создан (возможно, нет изменений или не настроен пользователь)
    echo Если нужно настроить Git пользователя, выполните:
    echo   git config --global user.name "Ваше Имя"
    echo   git config --global user.email "your.email@example.com"
)

echo.
echo Подключение к GitHub репозиторию...
git remote remove origin 2>nul
git remote add origin https://github.com/u167860i-max/Slavic-Calorie-Tracker.git

echo.
echo Переименование ветки в main...
git branch -M main 2>nul

echo.
echo Загрузка кода на GitHub...
echo ВНИМАНИЕ: Вам может потребоваться ввести логин и пароль GitHub
echo Если используете двухфакторную аутентификацию, используйте Personal Access Token вместо пароля
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ОШИБКА при загрузке на GitHub
    echo ============================================================
    echo Возможные причины:
    echo 1. Неверные учетные данные
    echo 2. Нужен Personal Access Token (вместо пароля)
    echo    Создайте токен: https://github.com/settings/tokens
    echo 3. Репозиторий уже содержит файлы
    echo.
    echo Попробуйте выполнить команды вручную:
    echo   git push -u origin main
    echo.
) else (
    echo.
    echo ============================================================
    echo УСПЕХ! Код загружен на GitHub
    echo ============================================================
    echo Репозиторий: https://github.com/u167860i-max/Slavic-Calorie-Tracker
    echo.
)

pause

