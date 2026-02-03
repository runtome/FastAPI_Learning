# FastAPI_Learning


pip install passlib
pip install bcrypt==4.0.1



sqlite3 todosapp.db 
SQLite version 3.51.1 2025-11-28 17:28:25
Enter ".help" for usage hints.
sqlite> select * from users;
1|code@mail.com|Code|MyCode|Code|$2b$12$/nPyd52UPqRR3Z2uqBrXJup.IvCxUGgKP9LfaLBfFR5ixnneulcaO|1|admin
sqlite>



pip install python-multipart
uvicorn main:app --reload   

https://www.jwt.io/

pip install "python-jose[cryptography]"

openssl rand -hex 32
8fa3a41c4a1df1a0980de3dcabc9cb78e39b4f91263ed4d47a0984b713866193


pip install psycopg2-binary 
pip install python-dotenv

pip install alembic

alembic init alembic

alembic revision -m "Create phone for user column"

alembic upgrade b9fa4699b4d8

alembic downgrade -1


alembic upgrade b9fa4699b4d8

