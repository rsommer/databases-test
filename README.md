# Prepare postgres test database
`podman run -d --name pytest-db --rm -ti -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_DB=example -e POSTGRES_USER=pytest -p 5436:5432 postgres:14`

# Setup testcase
```
pip install --user pdm
eval "$(pdm --pep582)"
pdm run pytest -sv test_sql.py
```
