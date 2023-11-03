from anvil_server.database import UserData
from anvil_server.socket import (
    CreateInstanceRequest,
    CreateInstanceResponse,
    UnixClient,
)
from eth_launchers.launcher import ETH_RPC_URL
from eth_launchers.pwn_launcher import PwnChallengeLauncher
from eth_launchers.team_provider import get_team_provider
from foundry.anvil import LaunchAnvilInstanceArgs


class Challenge(PwnChallengeLauncher):
    def create_instance(self, client: UnixClient) -> CreateInstanceResponse:
        return client.create_instance(
            CreateInstanceRequest(
                id=self.team,
                instances={
                    "main": LaunchAnvilInstanceArgs(
                        balance=1000,
                        fork_url=ETH_RPC_URL,
                    ),
                },
                daemons=[
                    "/home/user/watcher.py",
                ],
            )
        )

    def is_solved(self, user_data: UserData, addr: str) -> bool:
        return user_data.metadata.get("donated", 0) > 100000000000000000000000000 # 26个0


Challenge(
    project_location="project",
    provider=get_team_provider(),
).run()
