import json
import os

from py2neo import Graph, Node, Relationship


class Neo4j(object):
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        dir_name = config['SAVE_PATH']
        self.__graph = Graph('http://localhost:7474', username='ziuno', password='1234')
        self.__graph.delete_all()
        root = Node('文件夹', name=dir_name)
        self.__graph.create(root)
        for dir in os.listdir(dir_name):
            if dir.startswith('.'):
                continue
            text = dir
            son = Node('文件夹', name=text)
            belong = Relationship(root, '包含', son)
            self.__graph.create(belong)
            for txt in os.listdir(os.path.join(dir_name, dir)):
                text = txt.split('.')[0]
                grandson = Node('文件', name=text)
                belong = Relationship(son, '包含', grandson)
                self.__graph.create(belong)