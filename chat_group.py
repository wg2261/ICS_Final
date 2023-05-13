# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:58:31 2015

@author: zhengzhang
"""
S_ALONE = 0
S_TALKING = 1
S_INGAME = 2

#==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
#==============================================================================

class Group:

    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0
        self.game_pairs = {}
        self.game_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):
        return name in self.members.keys()
    
    def is_alone(self, name):
        in_game, group_key = self.find_game(name)
        return not in_game

    def leave(self, name):
        self.disconnect(name)
        self.end(name)
        del self.members[name]
        return

    def find_group(self, name):
        found = False
        group_key = 0
        for k in self.chat_grps.keys():
            if name in self.chat_grps[k]:
                return True, k
        return found, group_key
    
    def find_game(self, name):
        found = False
        group_key = 0
        for k in self.game_pairs.keys():
            if name in self.game_pairs[k]:
                return True, k
        return found, group_key

    def connect(self, me, peer):
        peer_in_group = False
        #if peer is in a group, join it
        peer_in_group, group_key = self.find_group(peer)
        if peer_in_group == True:
            print(peer, "is talking already, connect!")
            self.chat_grps[group_key].append(me)
            self.members[me] = S_TALKING
        else:
            # otherwise, create a new group
            print(peer, "is idle as well")
            self.grp_ever += 1
            group_key = self.grp_ever
            self.chat_grps[group_key] = []
            self.chat_grps[group_key].append(me)
            self.chat_grps[group_key].append(peer)
            self.members[me] = S_TALKING
            self.members[peer] = S_TALKING
        print(self.list_me(me))
        return

    def disconnect(self, me):
        # find myself in the group, quit
        in_group, group_key = self.find_group(me)
        if in_group == True:
            self.chat_grps[group_key].remove(me)
            self.members[me] = S_ALONE
            # peer may be the only one left as well...
            if len(self.chat_grps[group_key]) == 1:
                peer = self.chat_grps[group_key].pop()
                self.members[peer] = S_ALONE
                del self.chat_grps[group_key]
        return
    
    def can_game(self, peer):
        if self.members[peer] == S_INGAME:
            print(peer, "is already in a game!")
            return False
        elif self.members[peer] == S_TALKING:
            print(peer, "is busy chatting!")
            return False
        return True
        
    def game(self, me, peer):
        if self.can_game(peer):
            # otherwise, create a new group
            print(peer, "is idle as well")
            self.game_ever += 1
            group_key = self.game_ever
            self.game_pairs[group_key] = []
            self.game_pairs[group_key].append(me)
            self.game_pairs[group_key].append(peer)
            self.members[me] = S_INGAME
            self.members[peer] = S_INGAME
            return

    def end(self, me):
        # find myself in the game, quit
        in_game, group_key = self.find_game(me)
        if in_game == True:
            self.game_pairs[group_key].remove(me)
            self.members[me] = S_ALONE
            peer = self.game_pairs[group_key].pop()
            self.members[peer] = S_ALONE
            del self.game_pairs[group_key]
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        full_list += "Games: -----------" + "\n"
        full_list += str(self.game_pairs) + "\n"
        return full_list

    def list_all2(self, me):
        print("Users: ------------")
        print(self.members)
        print("Groups: -----------")
        print(self.chat_grps, "\n")
        print("Games: -----------")
        print(self.game_pairs, "\n")
        member_list = str(self.members)
        grp_list = str(self.chat_grps)
        game_list = str(self.game_pairs)
        return member_list, grp_list, game_list

    def list_me(self, me):
        # return a list, "me" followed by other peers in my group
        my_list = []
        if me in self.members.keys():
            my_list = [me]
            in_group, group_key = self.find_group(me)
            if in_group == True:
                for member in self.chat_grps[group_key]:
                    if member != me:
                        my_list.append(member)
            else:
                in_game, game_key = self.find_game(me)
                if in_game:
                    for member in self.game_pairs[game_key]:
                        if member != me:
                            my_list.append(member)
        return my_list
    
    def list_loners(self):
        loners = [m for m in self.members if self.members[m] == S_ALONE]
        return str(loners)
    
    def decending_group_sizes(self):
        list = [(len(self.chat_grps[k]), k) for k in self.chat_grps.keys()]
        list.sort(key = lambda i: i[1])
        return [i for length, i in list]
    
    def ascending_group_sizes(self):
        list = self.decending_group_sizes()
        return list[::-1]

if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    print(g.list_all())
    g.list_all2('a')
    g.connect('a', 'b')
    print(g.list_all())
