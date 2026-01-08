# Скрипт для инициализации Git репозитория
# Запустите этот скрипт в PowerShell из папки проекта

Write-Host "Инициализация Git репозитория..." -ForegroundColor Green

# Проверка наличия Git
try {
    $gitVersion = git --version
    Write-Host "Git найден: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ОШИБКА: Git не установлен или не найден в PATH" -ForegroundColor Red
    Write-Host "Скачайте Git с https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Инициализация репозитория
Write-Host "`nИнициализация Git репозитория..." -ForegroundColor Yellow
git init

# Добавление файлов
Write-Host "`nДобавление файлов..." -ForegroundColor Yellow
git add .

# Проверка статуса
Write-Host "`nСтатус репозитория:" -ForegroundColor Yellow
git status

# Создание первого коммита
Write-Host "`nСоздание первого коммита..." -ForegroundColor Yellow
git commit -m "Initial commit: Calorie Tracker application"

Write-Host "`n✓ Git репозиторий успешно инициализирован!" -ForegroundColor Green
Write-Host "`nСледующие шаги:" -ForegroundColor Cyan
Write-Host "1. Создайте репозиторий на GitHub (https://github.com/new)" -ForegroundColor White
Write-Host "2. Выполните команды, которые GitHub покажет после создания репозитория:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/ВАШ_USERNAME/ИМЯ_РЕПОЗИТОРИЯ.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray

