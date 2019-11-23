from modules.new.BaseModule import BaseModule


class NmapModule(BaseModule):

    def __init__(self):
        super(NmapModule, self).__init__(name="Nmap",
                                         description="Scans the specified IP address for ports",
                                         loot_name="nmap",
                                         multithreaded=False,
                                         intrusive=True,
                                         critical=True)
        self.required_programs = ["nmap"]

    def should_execute(self, service: str, port: int) -> bool:
        # Nmap scan should always execute
        return True

    def execute(self, ip: str, port: int) -> None:
        self.__execute()
