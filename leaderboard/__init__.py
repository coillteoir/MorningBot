"""Class definition for morningbot leaderboard"""

import json
import os
import time


class Leaderboard:
    """Leaderboard containing scores for members of a server"""

    class Member:
        """Individual member of a server, stores score and validation logic"""

        def __init__(self, uuid: int, mornings: int):
            self.uuid = uuid
            self.mornings = mornings
            self.last_morning = time.gmtime(0)

        def inc(self):
            """Increments the score if it has not been incremented already."""
            temp_time = time.localtime()
            if temp_time.tm_yday != self.last_morning.tm_yday:
                self.mornings += 1

        def __lt__(self, other) -> bool:
            """Less than dunder"""
            return self.mornings < other.mornings

        def __str__(self) -> str:
            """Str dunder"""
            return f"{self.uuid}: {self.mornings}"

    def __init__(self, channel: int):
        if channel is None:
            return

        self.channel = channel
        self.path = f"config/leaderboards/{self.channel}-leaderboard.json"
        print(self.path)

        if os.path.isdir("config/leaderboards/") is not True:
            os.mkdir("config/leaderboards/")

        self.members = []
        if os.path.isfile(self.path):
            with open(self.path, encoding="utf-8") as leader_file:
                leader_dict = json.load(leader_file)
            self.channel = leader_dict["channel"]

            for member in leader_dict["members"]:
                self.members.append(self.Member(member["uuid"], member["mornings"]))
        else:
            self.channel = channel

    def return_leaderboard(self):
        """Sorts the leaderboard to be returned"""
        self.members.sort()
        self.members.reverse()
        return self.members

    def add_point(self, uuid: str):
        """Add point to member"""
        for member in self.members:
            if member.uuid == uuid:
                member.inc()
                print("exists", member)
                break
        else:
            self.members.append(self.Member(uuid, 1))
            print(f"Created: {uuid}")

    def dump_data(self):
        """Dumps the data to a json file"""

        member_list = [vars(member) for member in self.members]
        leader_dict = {"channel": self.channel, "members": member_list}
        with open(self.path, "w+", encoding="utf-8") as dump_file:
            json.dump(leader_dict, dump_file)
