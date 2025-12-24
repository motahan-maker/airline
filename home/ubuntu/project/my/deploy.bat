@echo off
echo 🚀 Deploying Airline Management System to Heroku...
echo.

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI not found. Please install it from https://devcenter.heroku.com/articles/heroku-cli
    echo Or run: npm install -g heroku
    pause
    exit /b 1
)

REM Login to Heroku
echo 🔐 Logging into Heroku...
heroku login
if %errorlevel% neq 0 (
    echo ❌ Heroku login failed
    pause
    exit /b 1
)

REM Create app
echo 📦 Creating Heroku app...
set /p APP_NAME="Enter your app name: "
heroku create %APP_NAME%
if %errorlevel% neq 0 (
    echo ❌ Failed to create Heroku app
    pause
    exit /b 1
)

REM Set environment variables
echo 🔧 Setting environment variables...
heroku config:set SECRET_KEY=django-insecure-production-key-change-this-123456789 -a %APP_NAME%
heroku config:set STRIPE_PUBLIC_KEY=pk_test_placeholder_public_key -a %APP_NAME%
heroku config:set STRIPE_SECRET_KEY=sk_test_placeholder_secret_key -a %APP_NAME%
heroku config:set DEBUG=False -a %APP_NAME%

REM Deploy
echo 🚀 Deploying application...
git push heroku main
if %errorlevel% neq 0 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

REM Run migrations
echo 🗄️ Running database migrations...
heroku run python manage.py migrate -a %APP_NAME%

REM Create superuser
echo 👤 Creating admin user...
heroku run python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('superadmin', 'admin@example.com', 'admin123')" -a %APP_NAME%

REM Populate sample data
echo ✈️ Populating sample flights...
heroku run python manage.py populate_flights -a %APP_NAME%

echo.
echo ✅ Deployment complete!
echo 🌐 Your app is live at: https://%APP_NAME%.herokuapp.com/
echo 🔑 Admin panel: https://%APP_NAME%.herokuapp.com/admin/
echo    Username: superadmin
echo    Password: admin123
echo.
echo ⚠️  IMPORTANT: Update your Stripe keys in Heroku config for real payments!
echo    heroku config:set STRIPE_PUBLIC_KEY=pk_live_... STRIPE_SECRET_KEY=sk_live_... -a %APP_NAME%
echo.
pause