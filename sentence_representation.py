# import json

attr_of_node = ['det', 'neg', 'auxpass', 'aux', 'auxpass']

counter_error_example = 0


def from_token_lst_to_span(token_lst):
    idx = 0
    span = ""
    for token in token_lst:
        if idx != 0:
            span += " "
        span += token.text
        idx += 1
    return span


class Node:
    def __init__(self, span):
        span.sort(key=lambda x: x[0].i)
        self.span = [x[0] for x in span]
        self.attr_head = []
        self.bridge_to_head = ""
        self.basic_span = ""
        self.is_amod_type = False
        self.initialize_attr_and_basic_span(span)
        ########
        self.children_to_the_left = []
        self.children_to_the_right = []
        # self.kind = kind

    def initialize_attr_and_basic_span(self, span):
        global counter_error_example
        basic_lst = []
        bridge_to_head_lst = []
        for token in span:
            if token[0].dep_ in attr_of_node and token[1] == 1:
                self.attr_head.append(token[0])
            elif token[1] == 2:
                bridge_to_head_lst.append(token[0])
            else:
                if token[1] == 4:
                    self.is_amod_type = True
                basic_lst.append(token[0])
        self.basic_span = from_token_lst_to_span(basic_lst)
        self.bridge_to_head = from_token_lst_to_span(bridge_to_head_lst)
        if self.basic_span == "":
            counter_error_example += 1

    def add_children(self, child):
        if child.span[-1].i < self.span[-1].i or child.is_amod_type:
            self.children_to_the_left.append(child)
        else:
            self.children_to_the_right.append(child)


def _try(o):
    try:
        return o.__dict__
    except:
        return str(o)


class head_phrase:
    def __init__(self, name):
        self.head_phrase_name = name
        self.head_phrase_child_dict = {}
        self.sentence_and_node_to_head_phrase_child_dict = {}
        self.head_node_lst = []
        self.bridge_to_head_phrase_child_dict = {}
        # self.nodes_lst = []
        # self.sentence_to_child = {}
        # self.kind = kind

    def add_new_node(self, node, sentence):
        self.head_node_lst.append((node.basic_span, hash(sentence)))
        for child in node.children_to_the_right:
            if child.basic_span == "":
                print("error")
            self.head_phrase_child_dict[child.basic_span] = self.head_phrase_child_dict.get(child.basic_span, [])
            self.head_phrase_child_dict[child.basic_span].append(child.basic_span)
            if child.bridge_to_head:
                self.bridge_to_head_phrase_child_dict[child.bridge_to_head] = self.bridge_to_head_phrase_child_dict.get(
                    child.bridge_to_head, [])
                self.bridge_to_head_phrase_child_dict[child.bridge_to_head].append(child.basic_span)
            self.sentence_and_node_to_head_phrase_child_dict[
                (hash(sentence), node.basic_span)] = self.sentence_and_node_to_head_phrase_child_dict.get((hash(sentence), node.basic_span), [])
            self.sentence_and_node_to_head_phrase_child_dict[(hash(sentence), node.basic_span)].append(child.basic_span)

    # def toJSON(self):
    #     return json.dumps(self, default=vars,
    #                       sort_keys=True, indent=4)
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: _try(o), sort_keys=True, indent=0, separators=(',', ':')).replace(
    #         '\n', '')
