from pathlib import Path

#Creating path that points to each files
Path("app/__init__.py").touch()
Path("app/data/__init__.py").touch()
Path("app/services/__init__.py").touch()