# Nom de l'exécutable final
TARGET = bigcat

# Script Python principal
SCRIPT = bigcat.py

# Options PyInstaller
OPTIONS = --onefile --noconsole

.PHONY: all clean

# Cible par défaut
all: $(TARGET)

# Générer l'exécutable
$(TARGET):
	source venv/bin/activate && python -m PyInstaller $(OPTIONS) $(SCRIPT)
# Nettoyer les fichiers générés
clean:
	rm -rf build dist __pycache__ $(TARGET).spec

