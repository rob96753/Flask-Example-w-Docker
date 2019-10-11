import json
import os


class BloodProducts:
    def __init__(self, productsPath):
        """
        Expects the fill path to the Blood Products data file
        :param productsPath:
        """
        if os.path.exists(productsPath):
            with open(productsPath, "r+") as bpfp:
                bloodProducts = json.load(bpfp)
                self._products = bloodProducts.get('products', dict())
                self._joinedProducts = bloodProducts.get('joinedProducts', dict())

        else:
            raise Exception(f'Exception in BloodProducts {productsPath} Does Not Exist')

    def get_products(self):
        return self._products

    def get_joined_products(self):
        return self._joinedProducts

    def get_product_details(self, products):
        try:
            if products in self.get_joined_products():
                d = dict()
                for product in self._joinedProducts[products]:
                    d[product] = self._products[product]
                return d
            elif products in self.get_products():
                return dict(product=self._products[products])
            else:
                raise Exception(f'Exception in BloodProducts {products} Requested Non-Existing Product')
        except Exception as ex:
            raise Exception(f'Exception in get_product_details {str(ex)}')

