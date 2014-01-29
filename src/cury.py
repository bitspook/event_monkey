from __future__ import division
import yaml
import random
from string import capwords


class Cury(object):
    """It builds cury with keywords collected from cury masalas and content given at construction.
    """
    def __init__(self, masalas=None, masala_dir='./cury_masalas', spices=3, ):
        """takes content, and list of masalas to make cury.

        real_content: string of real content
        masalas: list of masalas
        masala_dir: Directory where to find masalas. Defaults to './cury_masalas'
        """
        self.masala_dir = masala_dir
        self.masalas = ['all']

        if masalas:
            if type(masalas) == str:
                masalas = [m.strip() for m in masalas.split(',')]
            self.masalas += masalas


        keywords, search_terms = self.get_data_from_masalas()
        self.keywords, self.search_terms = self.get_percent_items_from_list(keywords, spices), self.get_percent_items_from_list(search_terms, spices)
        self.title = capwords(random.choice(self.search_terms)).replace('"','')[:70]
        self.tags = self.get_percent_items_from_list(self.keywords, 5)

    def get_data_from_masalas(self):
        keywords = []
        search_terms = []
        for masala in self.masalas:
            with open("{}/{}.yml".format(self.masala_dir, masala)) as f:
                temp = yaml.load(f)

                keywords += temp['keywords']
                search_terms += temp['search_terms']

        return keywords, search_terms

    def get_percent_items_from_list(self, lst, percentage):
        percentage = percentage * 10
        n = int(percentage / 100 * len(lst))
        return random.sample(lst, n)
