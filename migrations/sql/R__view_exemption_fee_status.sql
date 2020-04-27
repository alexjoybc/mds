DROP VIEW IF EXISTS exemption_fee_status_view;
CREATE OR REPLACE VIEW exemption_fee_status_view
	AS
SELECT m.mine_guid, m.mine_no, m.mine_name, m.exemption_fee_status_code, 
efs.description as exemption_fee_status_description, m.exemption_fee_status_note,
pmt.permit_guid, pmt.permit_no, p.party_name as mine_owner_name, a.address_line_1, a.address_line_2, a.city, a.sub_division_code, a.post_code
FROM mine m 
LEFT JOIN exemption_fee_status efs on m.exemption_fee_status_code = efs.exemption_fee_status_code 
LEFT JOIN permit pmt on m.mine_guid = pmt.mine_guid
LEFT JOIN permit_amendment pmt_a on pmt.permit_id = pmt_a.permit_id AND pmt_a.permit_amendment_type_code = 'OGP'
LEFT JOIN mine_party_appt mpa on m.mine_guid = mpa.mine_guid AND mpa.mine_party_appt_type_code = 'MOW' AND mpa.deleted_ind = false
LEFT JOIN party p on mpa.party_guid = p.party_guid
LEFT JOIN address a on a.party_guid = p.party_guid;

