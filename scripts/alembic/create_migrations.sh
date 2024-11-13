echo "Enter name of migration:"
read message
docker-compose exec support_bot alembic revision -m "$message" --autogenerate