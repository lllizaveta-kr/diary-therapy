import traceback

try:
    # Импортируем МОДУЛЬ, а не класс — тогда увидим настоящую ошибку
    import windows.admin_window as m

    print("✓ Модуль загружен")
    print("Классы в модуле:", [n for n in dir(m) if not n.startswith("_")])
except Exception:
    print("❌ РЕАЛЬНАЯ ОШИБКА (вот она!):")
    traceback.print_exc()
