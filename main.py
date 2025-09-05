import sys
from roles import RolePreset
from chat_service import ChatService
from config import settings

# Se pide rol al usuario- RolPreset lo mapea y lo manda
def choose_role() -> RolePreset:
    print("Elegí un rol inicial:")
    print("1) Profesor 2) Traductor 3) Programador 4) Asistente")
    self = input(">").strip()
    mapping = {
        "1": RolePreset.PROFESOR,
        "2": RolePreset.TRADUCTOR,
        "3": RolePreset.PROGRAMADOR,
        "4": RolePreset.ASISTENTE,
    }
    return mapping.get(self, RolePreset.ASISTENTE)

# Instrucciones de cómo se usa
def print_help():
    print("\nComandos:")
    print(":rol profesor|traductor|programador|asistente -> cambia el rol")
    print(":reset                                       -> limpia la memoria")
    print(":salir                                       -> termina\n")

# Se presenta el robot, toma el rol, y comienza la conversación
def main():
    print(f"🤖{settings.system_name}")
    role = choose_role()
    chat = ChatService(role)
    print_help()
    while True:
        try:
            user = input(" 👋🏻Vos: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋🏻Chau!")
            break
        if not user:
            continue
        if user.lower() in (":salir", "salir", "exit", "quit"):
            print("¡Chau!")
            break
        if user.lower() == ":reset":
            chat.reset()
            print("Memoria borrada.")
            continue
        if user.lower().startswith(":rol"):
            rest = user.split()
            new_role = (rest[1] if len(rest) > 1 else "").lower()
            mapping = {
                "profesor": RolePreset.PROFESOR,
                "traductor": RolePreset.TRADUCTOR,
                "programador": RolePreset.PROGRAMADOR,
                "asistente": RolePreset.ASISTENTE,
            }
            if new_role in mapping:
                chat.set_role(mapping[new_role])
                print(f"Rol cambiado a: {new_role}")
            else:
                print("Rol inválido. Opciones: profesor, traductor, programador, asistente")
            continue
        if user.lower() == ":help":
            print_help()
            continue

        # Pregunta normal
        try:
            answer = chat.ask(user)
            print(" Bot:", answer)
        except Exception as e:
            print("✖️ Error manejado:", e)

if __name__ == "__main__":
    main()
