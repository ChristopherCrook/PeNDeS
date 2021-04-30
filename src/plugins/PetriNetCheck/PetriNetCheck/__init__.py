"""
This is where the implementation of the plugin code goes.
The PetriNetCheck-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('PetriNetCheck')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PetriNetCheck(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        self.namespace = None
        META = self.META
        logger = self.logger

        name = core.get_attribute(active_node, 'name')

        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))
        self.nodes = core.load_sub_tree(active_node
        
        self.places = []
        self.transitions = []
        self.arcs = []
        self.tokens = []
        self.nets = []
        
        self.errorFlag = False
        self.errors = []
        
        for node in self.nodes:
          if core.is_type_of(node, META['place']):
            self.places.append(node)
          if core.is_type_of(node, META['transition']):
            self.transitions.append(node)
          if core.is_type_of(node, META['arc']):
            self.arcs.append(node)
          if core.is_type_of(node, META['token']):
            self.token.append(node)
          if core.is_type_of(node, META['Net']):
            self.nets.append(node)
            
        # First we check the arcs for constraints
        for arc in self.arcs:
          if arc:
            p_list = core.get_valid_pointer_names(arc)
            for p in p_list:
              if p:
                temp = core.get_pointer_path(arc, p)
                if core.is_type_of(temp, META['place']) or core.is_type_of(temp, META['transition']):
                  continue
                else:
                  self.errors.append("Arc points to type other than place or transition")
                  self.errorFlag = True
                        
        # Now we check that tokens are children of places
        for token in self.tokens:
          if token:
            if core.is_type_of(core.get_parent(token), META['place']):
              continue
            else:
              self.errors.append("Token is not child of place")
              self.errorFlag = True
        
        # Now we make sure that a model doesn't begin or end with
        # a transition

        #core.set_attribute(active_node, 'name', 'newName')

        #commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        #logger.info('committed :{0}'.format(commit_info))
