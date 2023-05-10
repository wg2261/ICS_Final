# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle
import string

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)
 
    def indexing(self, m, l):
        words = m.lower().split()
        words = [w.strip() for w in words]
        self.total_words += len(words)

        if len(words) == 1:
            self.index[words[0]] = [l]
            return

        for w in words:
            w = w.translate(str.maketrans('', '', string.punctuation))
            if l not in self.index.get(w, [-1]):
                self.index[w] = self.index.get(w, []) + [l]
                                     
    def search(self, term):
        msgs = []
        words = term.lower().split()
        if len(words) > 0:
            lines = [i for i in self.index.get(words[0], [])]
            msgs = [(i, self.msgs[i]) for i in lines if term in self.msgs[i]]
        return msgs

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # load poems
    def load_poems(self):
        lines = open(self.name, 'r').readlines()
        for l in lines:
            self.add_msg_and_index(l.rstrip())
    
    def get_poem(self, p):
        start = self.search(self.int2roman[p] + ".")
        if start == []:
            return []
        end = self.search(self.int2roman[p + 1] + ".")
        if end == []:
            end = self.get_total_msgs()
        else:
            end = end[0][0]
        return self.msgs[start[0][0] : end]
    
if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
