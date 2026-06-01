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


class DeployStrategy(ABC):
    @abstractmethod
    def deploy(self, server: ServerNode): pass


class AnsibleDeploy(DeployStrategy):
    def deploy(self, server: ServerNode):
        print(f"[Ansible] Deploy to {server.name}...")


class TerraformDeploy(DeployStrategy):
    def deploy(self, server: ServerNode):
        print(f"[Terraform] Create infra {server.name}...")


class DeploymentContext:
    def __init__(self, strategy: DeployStrategy):
        self.strategy = strategy

    def execute_deploy(self, server: ServerNode):
        self.strategy.deploy(server)


class ServerOperation(ABC):
    @abstractmethod
    def operate(self): pass


class BasicServerOperation(ServerOperation):
    def __init__(self, server: ServerNode):
        self.server = server

    def operate(self):
        return f"[{self.server.name}] Basic operation is working."


class ServerDecorator(ServerOperation):
    def __init__(self, wrapped: ServerOperation):
        self.wrapped = wrapped

    def operate(self):
        return self.wrapped.operate()


class PrometheusExporterDecorator(ServerDecorator):
    def operate(self):
        base_op = self.wrapped.operate()
        return f"{base_op} + Export metric is enabled."


class LegacySyslog:
    def log_message(self, msg):
        print(f"[SYSLOG_LEGACY_DAEMON] {msg}")


class ModernLoggerInterface(ABC):
    @abstractmethod
    def info(self, msg): pass


class SyslogAdapter(ModernLoggerInterface):
    def __init__(self, legacy_logger: LegacySyslog):
        self.legacy_logger = legacy_logger

    def info(self, msg):
        self.legacy_logger.log_message(f"INFO: {msg}")


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

    deployer = DeploymentContext(TerraformDeploy())
    deployer.execute_deploy(web_node)

    deployer.strategy = AnsibleDeploy()
    deployer.execute_deploy(db_node)

    basic_web = BasicServerOperation(web_node)
    monitored_web = PrometheusExporterDecorator(basic_web)
    print(monitored_web.operate())

    legacy_syslog = LegacySyslog()
    logger = SyslogAdapter(legacy_syslog)
    logger.info("Усі конфігурації успішно застосовані.")

if __name__ == '__main__':
    main()
