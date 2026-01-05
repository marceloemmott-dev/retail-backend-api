from app.core.database import engine

try:
    with engine.connect() as conn:
        print("✅ Conectado correctamente a Neon (development)")
except Exception as e:
    print("❌ Error de conexión:", e)
