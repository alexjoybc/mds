import json
from app.api.mines.tailings.models.tailings import MineTailingsStorageFacility
from app.api.required_documents.models.required_documents import RequiredDocument
from tests.factories import MineFactory, MineTailingsStorageFacilityFactory


# GET
def test_get_mine_tailings_storage_facility_by_mine_guid(test_client, db_session, auth_headers):
    tsf = MineTailingsStorageFacilityFactory()

    get_resp = test_client.get(f'/mines/{tsf.mine_guid}/tailings',
                               headers=auth_headers['full_auth_header'])
    get_data = json.loads(get_resp.data.decode())
    assert get_resp.status_code == 200, get_resp.response
    assert len(get_data['mine_tailings_storage_facilities']) == 1


def test_post_mine_tailings_storage_facility_by_mine_guid(test_client, db_session, auth_headers):
    mine = MineFactory()
    org_mine_tsf_list_len = len(mine.mine_tailings_storage_facilities)

    post_resp = test_client.post(f'/mines/{mine.mine_guid}/tailings',
                                 data={'mine_tailings_storage_facility_name': 'a name'},
                                 headers=auth_headers['full_auth_header'])
    post_data = json.loads(post_resp.data.decode())
    assert post_resp.status_code == 200
    assert len(mine.mine_tailings_storage_facilities) == org_mine_tsf_list_len + 1


def test_post_first_mine_tailings_storage_facility_by_mine_guid(test_client, db_session,
                                                                auth_headers):
    mine = MineFactory(minimal=True)
    assert len(mine.mine_tailings_storage_facilities) == 0
    
    post_resp = test_client.post(f'/mines/{mine.mine_guid}/tailings',
                                 data={'mine_tailings_storage_facility_name': 'a name'},
                                 headers=auth_headers['full_auth_header'])
    assert post_resp.status_code == 200
    post_data = json.loads(post_resp.data.decode())
    assert len(mine.mine_tailings_storage_facilities) == 1
    assert len(mine.mine_expected_documents) == len(
        RequiredDocument.find_by_req_doc_category('TSF', 'INI'))
