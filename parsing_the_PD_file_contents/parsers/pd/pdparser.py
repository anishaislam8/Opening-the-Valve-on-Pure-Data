import os.path
import copy
import json
import sys

class MalformedPureData(Exception):
    def __init__(self, pd_path, e):
        self.path = pd_path
        self.err = e
    def __str__(self):
        return "[Error] Malformed Pure Data file: %s\n\t%s" % (self.path, self.err.__str__())

class PDParser:
    '''
    This class parses pure data files.
    '''

    def __init__(self, pd_f):
        '''
        Parses the pd save file and stores the patch as a class member
        '''

        try:
            self._path = pd_f.name
        except AttributeError:
            pass

        self.objects = []
        self.connections = []

        obj_convert = {
            "obj": "newobj",
            "msg": "message",
            "text": "comment"
        }

        if not hasattr(pd_f, 'readline') and hasattr(pd_f, 'read') and callable(pd_f.read):
            pd_f = pd_f.read().split('\n')
 
        try:
            patch_level = 0
            patch_level_name = 'PD-ROOT'
            previous_patch_level_name_stack = []

            
            previous_graph_level_name_stack = []
            

            
            line = ''
            for l in pd_f:
                if len(line):
                    line += str(" %s" % l).rstrip()
                else:
                    line += str(l).strip()
                

                if line.endswith(';\n') or line.endswith(';'):
                    
                    # we now have all of the word-wrapped line
                    line = line.rstrip('\n')
                    line = line.rstrip(';')
                    line = line.strip()

                    
                    entity_attrs = line.split(' ')
                    #print("Entity attrs: ", entity_attrs)
                    if len(entity_attrs) < 2:
                        line = ''
                        continue
                    chunk_type = entity_attrs[0]
                    entity_type = entity_attrs[1]

                    xdim = ydim = 0

                    if chunk_type == '#N':
                        if entity_type == 'canvas':
                            patch_level += 1

                            if patch_level > 1:
                                obj_entity = {'box': {
                                    "id": f"{'_'.join(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name])}_" + "obj-%d" % self.get_subpatch_max_id(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name]),
                                    "maxclass": 'subpatch',
                                    "fontname": 'Arial',
                                    "numinlets": 0,
                                    "numoutlets": 0,
                                    "text": entity_attrs[6:],
                                    'original_text': entity_attrs,
                                    'object_type': 'canvas'
                                }}
                                
                                self.objects.append(obj_entity)

                            if len(entity_attrs) == 8:
                                previous_patch_level_name_stack.append(patch_level_name)
                                patch_level_name = entity_attrs[6]

                    elif chunk_type == '#X' and entity_type in ['restore', 'pop']:
                        object_type = entity_type
                        if entity_type == 'restore' and len(entity_attrs) == 5:
                            # https://puredata.info/docs/developer/PdFileFormat#r39
                            obj_entity = {'box': {
                                "id": f"{'_'.join(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name])}_" + "obj-%d" % self.get_subpatch_max_id(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name]),
                                "maxclass": 'newobj',
                                "fontname": 'Arial',
                                "fontsize": 10,
                                "text": entity_attrs[4:],
                                "numinlets": 0,
                                "numoutlets": 0,
                                'original_text': entity_attrs,
                                "object_type" : object_type
                            }}
                            self.objects.append(obj_entity)

                        if entity_type == 'restore':
                            patch_level_name = previous_patch_level_name_stack.pop()
                            patch_level -= 1
                        elif entity_type == 'pop':
                            patch_level_name = previous_graph_level_name_stack.pop()
                            
                        
                        
                        

                    elif chunk_type == '#X':
                        if entity_type == "connect":
                            
                            conn_entity = {"patchline": {
                                "destination": [f"{'_'.join(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name])}_" + "obj-%s" % entity_attrs[4], int(entity_attrs[5])],
                                "source": [f"{'_'.join(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name])}_" + "obj-%s" % entity_attrs[2], int(entity_attrs[3])]
                            }}
                            self.connections.append(conn_entity)
                        
                        else:
                            obj_entity = {'box': {
                                "id": f"{'_'.join(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name])}_" + "obj-%d" % self.get_subpatch_max_id(previous_patch_level_name_stack + previous_graph_level_name_stack + [patch_level_name]),
                                "numinlets": 0,
                                "numoutlets": 0,
                                "text": "",
                                "fontname": 'Arial',
                                "fontsize": 10,
                                'object_type': entity_type
                            }}


                            # some objects have preset dimensions, like bangs or toggles
                            if entity_type == "graph":
                                
                                previous_graph_level_name_stack.append(patch_level_name)
                                patch_level_name = entity_attrs[2]
                                
                            if entity_type == "floatatom":
                                obj_entity["box"]["text"] = '0'     # does not store number in file format
                               
                            elif entity_type == "msg" or entity_type == "text":
                                
                                try:
                                    obj_entity["box"]["text"] = ' '.join(entity_attrs[4:])
                                except IndexError:
                                    pass
                            elif entity_type == "scalar":
                                pass
                            elif entity_type == "coords":
                                pass
                            elif entity_type == "obj":
                                if len(entity_attrs) >= 5:
                                    obj_type = entity_attrs[4]
                                else:
                                    obj_type = "unnamed_object"
                                obj_entity["box"]["object_type"] = obj_type

                                if obj_type == "bng" or obj_type == "tgl":
                                    pass
                                elif obj_type == "nbx":
                                    # edited: the 15th part is supposed to be the fontsize, but label can have spaces so, consider the position from the last
                                    obj_entity["box"]["text"] = '0'
                                    
                                elif obj_type == "vsl" or obj_type == "hsl" or obj_type == "vu":
                                    pass
                                elif obj_type == "vradio":
                                    pass
                                elif obj_type == "hradio":
                                    pass
                                elif obj_type == "outlet" or obj_type == "inlet":
                                    obj_entity["box"]["text"] = ' '.join(entity_attrs[4:])
                                else:
                                    # it's some other built in object
                                    obj_entity["box"]["text"] = ' '.join(entity_attrs[4:])


                            # update calculated object dimensions ... some still need to be done on the clientside
                            # depending on the drawing surface dpi
                            #obj_entity["box"]["patching_rect"][2:] = [int(xdim), int(ydim)]

                            # sometimes there are empty message boxes or comments
                            # better to ask forgiveness
                            try:
                                obj_entity["box"]["maxclass"] = obj_convert[entity_type]
                            except KeyError:
                                obj_entity["box"]["maxclass"] = entity_type

                            self.objects.append(obj_entity)
                    line = ''

            # calculate implicit properties of objects that are stated explicitly in max but not pd
            for c in self.connections:
                source_obj_id = c['patchline']['source'][0]
                target_obj_id = c['patchline']['destination'][0]
                
                matched_source = False
                matched_target = False

                for obj in self.objects:
                    
                    if source_obj_id == obj['box']['id']:
                        obj['box']['numoutlets'] += 1
                        matched_source = True

                    if target_obj_id == obj['box']['id']:
                        obj['box']['numinlets'] += 1
                        matched_target = True

                if not matched_source or not matched_target:
                    raise IndexError(f'Unmatched {source_obj_id} {matched_source} {target_obj_id} {matched_target}')

        except (KeyError, ValueError, IndexError) as e:
            raise MalformedPureData(self._path, e)

    def get_subpatch_max_id(self, hierarchy):
        id = 0
        string_map = f"{'_'.join(hierarchy)}_obj-"
        for obj in self.objects:
            if obj['box']['id'].startswith(string_map):
                id+=1
        return id
    

    def get_canvas_dims(self):
        '''
        Retrieves the dimensions of the canvas on which the objects are rendered
        [x, y]
        '''
        return (self.xdim, self.ydim) 

    def get_objects(self):
        '''
        Retrieves all of the objects from the pd patch
        '''
        return self.objects

    def get_connections(self):
        '''
        Retrieves all of the patch cords from the pd patch
        '''
        return self.connections

    def get_comments(self):
        '''
        Retrieves the pd objects that are comments
        '''
        return [o for o in self.objects if o['box']['maxclass'] == "comment"]

def generate_intermediate(pp):

    intermediate_format = dict()

    keys = ['maxclass', 'numinlets', 'numoutlets', 'text']

    
    for o in pp.get_objects():
        o_type = list(o.keys())[0]
        contents = copy.deepcopy(o[o_type])
        
        id = copy.deepcopy(contents['id'])
        del contents['id']

        for k in copy.deepcopy(list(contents.keys())):
            if k not in keys:
                del contents[k]

        contents['type'] = o_type

        if id not in intermediate_format.keys():
            intermediate_format[id] = dict()
            intermediate_format[id]['serialized_contents'] = contents
            intermediate_format[id]['connections'] = []

        else:
            raise ValueError(f"{id} has already been created before")

    for c in pp.get_connections():
        c_type = list(c.keys())[0]
        contents = copy.deepcopy(c[c_type])
        contents['type'] = c_type

        intermediate_format[contents['source'][0]]['connections'].append(contents)
    
    
    
    objects = pp.get_objects()
    connections = pp.get_connections()

    # get the objects without maxclass 'subpatch' (I am considering subpatch and graph to be a patch, not a node when I count objects)
    # nodes = [o for o in objects if o['box']['maxclass'] not in ['subpatch', 'graph']]

    nodes = [o for o in objects]

    # get the list of 'object_type' keys in nodes
    object_types = [o['box']['object_type'] for o in nodes if 'object_type' in o['box'].keys()]
    
    # get how many of each object type there are
    object_type_counts = {o: object_types.count(o) for o in object_types}


    output = {
        "edges" : len(connections),
        "nodes" : len(nodes),
        "node_types" : object_type_counts,
        "all_objects" : objects, # this is a list of all objects including graphs and subpatches generated by the original code
        "connections" : connections,
    }

    #json_output = json.dumps(output, indent=4)
    #print(json_output)

    return output
    
def main(filename: str):
    if os.path.isfile(filename):
        with open(filename) as f:
            pp = PDParser(f)
            return generate_intermediate(pp)
            
    else:
        raise ValueError('File does not exist')

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)

