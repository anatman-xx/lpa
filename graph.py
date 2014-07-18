#coding=utf8

class Vertex():
    def __init__(self, vid, lable = None):
        self.edge = {}

        self.vid = vid

        if lable is None:
            self.lable = vid

class Edge():
    def __init__(self, weight = 0.0):
        self.weight = weight

class Graph():
    def __init__(self, vertex = {}):
        self.vertex = vertex

    def __repr__(self):
        repr_str = ''

        for vid, vertex in self.vertex.items():
            for vid2, edge in vertex.edge.items():
                repr_str += 'vertex(id:%s) vertex(id:%s) weight:%d\n' % (vertex.vid, edge.vertex.vid, edge.weight)

        return repr_str

    @staticmethod
    def load_from_file(file_path):
        graph = Graph()
        
        with file(file_path, 'r') as data_file:
            index = 0

            for line in data_file:
                index += 1

                splited_data = line.split() # 格式 '节点1  节点2   相似度（权重）'

                vid = splited_data[0]
                vid2 = splited_data[1]
                weight = float(splited_data[2])

                graph.vertex.setdefault(vid, Vertex(vid)).edge[vid2]\
                    = graph.vertex.setdefault(vid2, Vertex(vid2)

        return graph

if __name__ == '__main__':
    test_model = Graph.load_from_file('test.data')
    print repr(test_model)
    print test_model.vertex
