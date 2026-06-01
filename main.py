from abc import ABC, abstractmethod


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


class ServerNode(ABC):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    @abstractmethod
    def get_role(self):
        pass

class WebServer(ServerNode):
    def get_role(self): return "веб сервер"

class DatabaseServer(ServerNode):
    def get_role(self): return "База даних сервер"

class ServerFactory:
    @staticmethod
    def create_server(server_type, name, config):
        if server_type == "web":
            return WebServer(name, config)
        elif server_type == "db":
            return DatabaseServer(name, config)
        raise ValueError("невідомий тип")



def main():
    print("Прототип")
    base_nixos_config = ServerConfig("NixOS", 4, 16)
    db_config = base_nixos_config.clone()
    db_config.ram = 32
    print(base_nixos_config)
    print(db_config)

    factory = ServerFactory()
    web_node = factory.create_server("web", "nix-web-01", base_nixos_config)
    db_node = factory.create_server("db", "nix-db-01", db_config)

    print(f"Created: {web_node.name} | Role: {web_node.get_role()} | Config: [{web_node.config}]")
    print(f"Created: {db_node.name}  | Role: {db_node.get_role()} | Config: [{db_node.config}]")

if __name__ == '__main__':
    main()