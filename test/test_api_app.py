import pdb
from api_app import PyYelpAPI


pyYelpAPI_obj = PyYelpAPI()

# if pytest not able locate module then execute below commands to set root directory for pythonpath.
# export PYTHONPATH=. pytest


def test_insert_api_data_to_table():
    pdb.set_trace()
    assert pyYelpAPI_obj.insert_api_data_to_table(
        pyYelpAPI_obj.get_yelp_api_restaurant_data()) is True
