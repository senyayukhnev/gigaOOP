class Settings:
    PROJECT_NAME: str = 'gigaOOP'
    PROJECT_VERSION: str = '0.1.0'

    SQLITE_DB = '/backend/gigaOOP_database.db'
    DATABASE_URL = f'sqlite+aiosqlite://{SQLITE_DB}'
    SECRET = 'eyJzdWIiOiJkaXNjbyIsIm5hbWUiOiJlbHlzaXVtIiwiaWF0IjoxNTE2MjM5MDIyfQ'


settings = Settings()
