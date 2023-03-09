import re
from typing import Optional


class RawHTTPParser:
    method_and_url_pattern = re.compile(
        br'(?P<method>\w+?)\s(?P<url>\w+:\/\/[\d|\.]+:\d+\/)'
    )
    host_and_port_pattern = re.compile(
        r'http://(?P<host>.+):(?P<port>\d+)'
    )
    user_agent_pattern = re.compile(
        br'(?P<user_agent>User-Agent.+?)\r'
    )
    netscape_pattern = re.compile(
        r'Netscape'
    )
    host: str = None
    port: int = None
    method: str = None
    user_agent: str = None
    is_parse_error: bool = False

    def __init__(self, raw: bytes):
        try:
            match_method_url = self.method_and_url_pattern.search(raw)
            match_user_agent = self.user_agent_pattern.search(raw)
            if not match_method_url or not match_user_agent:
                raise ValueError
            self.user_agent = self.to_str(match_user_agent.group('user_agent'))
            self.method = self.to_str(match_method_url.group('method'))
            host_and_port = self.host_and_port_pattern.search(self.to_str(match_method_url.group('url')))
            if not host_and_port:
                raise ValueError
            self.host = host_and_port.group('host')
            self.port = int(host_and_port.group('port'))
        except ValueError:
            self.is_parse_error = True

    @staticmethod
    def to_str(item: Optional[bytes]) -> Optional[str]:
        if item:
            return item.decode('charmap')

    @property
    def check_user_agent(self):
        netscape_search_res = self.netscape_pattern.search(self.user_agent)
        if netscape_search_res:
            return True
        return False

    def __str__(self):
        return str(dict(METHOD=self.method, USER_AGENT=self.user_agent, HOST=self.host, PORT=self.port))
