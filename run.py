from app import create_app, db

app = create_app()

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
