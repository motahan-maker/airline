#!/bin/bash

echo "🚀 Deploying Airline Management System to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Create app
echo "📦 Creating Heroku app..."
read -p "Enter your app name: " APP_NAME
heroku create $APP_NAME

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set SECRET_KEY=django-insecure-production-key-change-this-123456789 -a $APP_NAME
heroku config:set STRIPE_PUBLIC_KEY=pk_test_placeholder_public_key -a $APP_NAME
heroku config:set STRIPE_SECRET_KEY=sk_test_placeholder_secret_key -a $APP_NAME
heroku config:set DEBUG=False -a $APP_NAME

# Deploy
echo "🚀 Deploying application..."
git push heroku main

# Run migrations
echo "🗄️ Running database migrations..."
heroku run python manage.py migrate -a $APP_NAME

# Create superuser
echo "👤 Creating admin user..."
heroku run python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('superadmin', 'admin@example.com', 'admin123')" -a $APP_NAME

# Populate sample data
echo "✈️ Populating sample flights..."
heroku run python manage.py populate_flights -a $APP_NAME

echo "✅ Deployment complete!"
echo "🌐 Your app is live at: https://$APP_NAME.herokuapp.com/"
echo "🔑 Admin panel: https://$APP_NAME.herokuapp.com/admin/"
echo "   Username: superadmin"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Update your Stripe keys in Heroku config for real payments!"
echo "   heroku config:set STRIPE_PUBLIC_KEY=pk_live_... STRIPE_SECRET_KEY=sk_live_... -a $APP_NAME"