from abc import ABC, abstractmethod


# Фабричний метод
class ServerConfig:
    def __init__(self, os_name, cpu, ram):
        self.os_name = os_name
        self.cpu = cpu
        self.ram = ram

    def clone(self):
        return ServerConfig(
            os_name=self.os_name,
            cpu=self.cpu,
            ram=self.ram
        )

    def __str__(self):
        return f"OS: {self.os_name}, CPU: {self.cpu}, RAM: {self.ram}GB"






def main():
    print("Прототип")
    base_nixos_config = ServerConfig("NixOS", 4, 16)
    db_config = base_nixos_config.clone()
    db_config.ram = 32
    print(base_nixos_config)
    print(db_config)


if __name__ == '__main__':
    main()