# MealPlanner

todo how the different subprojects work

## Development

Ensure you have Docker and docker-compose installed. Run:
```
docker-compose up
```
in your terminal. The API should be accessible at http://127.0.0.1:5000

Alternatively, if you want to develop outside of docker, ensure you have pipenv installed, then run:
```
pipenv install
FLASK_APP=api FLASK_ENVIRONMENT=development pipenv run flask run
```

To get a psql shell in the development database:
```
docker-compose exec database psql --host=127.0.0.1 --user=postgres
```
To run a migration (or other sql file) manually, run:
```
docker-compose exec -T database psql --host=127.0.0.1 --user=postgres <data/migrations/0000-up.sql
```
