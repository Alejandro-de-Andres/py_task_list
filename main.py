# Crear un gestor de tareas CRUD (Create, read, update, delete) que lea un JSON para guardar las tareas.
#
# ID único → para identificarla (número incremental o UUID).
# Título → breve descripción de la tarea.
# Descripción → detalles adicionales.
# Estado → pendiente, en progreso, completada.
# Fecha de creación → cuándo se añadió.
# Fecha límite (deadline) → opcional, para poder ordenar o avisar.
#
# Prioridad → alta, media, baja.
# Categoría/etiquetas → por ejemplo, trabajo, personal, estudio.
# Fecha de finalización → para métricas o historial.
# Usuario asignado → si más adelante quieres hacerlo multiusuario.
#
# Subtareas → lista de tareas internas (checklist).
# Repetición → por ejemplo, cada X días/semanas.
# Adjuntos → rutas a archivos o URLs relacionadas.
# Recordatorios → fecha/hora para avisar.

from crud import create, read, update, delete
from InquirerPy import inquirer

def main():
    while True:
        action = inquirer.select(
            message = "¿Qué acción quiere realizar?: ",
            choices = [
                {"name": "Finalizar", "value": 0},
                {"name": "Crear tarea", "value": 1},
                {"name": "Mostrar tareas", "value": 2},
                {"name": "Editar tarea", "value": 3},
                {"name": "Eliminar tarea", "value": 4},
            ]
        ).execute()
        
        if action == 1:
            create()
        elif action == 2:
            read()
        elif action == 3:
            update()
        elif action == 4:
            delete()
        else:
            break

if __name__ == "__main__":
    main()