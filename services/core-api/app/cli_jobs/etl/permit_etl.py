import petl as etl
import uuid
from app.extensions import db
from flask import current_app
from datetime import datetime


def permit_etl(connection):
    connection.cursor().execute(r"""
        CREATE TABLE IF NOT EXISTS ETL_PERMIT(
            mine_party_appt_guid   uuid                  ,
            --permit info
            permit_amendment_guid  uuid                  ,
            permit_guid            uuid                  ,
            source                 numeric               ,
            mine_guid              uuid                  ,
            mine_no                character varying(12) ,
            permit_no              character varying(12) ,
            permit_cid             character varying(30) ,
            received_date          date                  ,
            issue_date             date                  ,
            authorization_end_date date                  ,
            permit_status_code     character varying(2)  ,
            --permittee info
            party_guid             uuid                  ,
            party_combo_id         character varying(200),
            first_name             character varying(100),
            party_name             character varying(100),
            party_type             character varying(3)  ,
            phone_no               character varying(12) ,
            email                  character varying(254),
            effective_date         date
        );
        """)
    connection.commit()

    valid_permits = etl.fromdb(
        connection, r"""
        SELECT
            mine_no||permit_no||recv_dt||iss_dt AS combo_id,
            max(cid) permit_cid
        FROM mms.mmspmt permit_info
        WHERE
            (sta_cd ~* 'z'  OR sta_cd ~* 'a')
            AND
            ((permit_no !~ '^ *$' AND  permit_no IS NOT NULL))
        GROUP BY combo_id
        """)
    current_app.logger.info(f'# valid permits {etl.nrows(valid_permits)}')

    permit_details = etl.fromdb(
        connection, f"""
        SELECT
            ETL_MINE.mine_guid                                       ,
            permit_info.mine_no                                      ,
            permit_info.permit_no                                    ,
            permit_info.cid AS permit_cid                            ,
            permit_info.recv_dt AS recv_dt                           ,
            permit_info.iss_dt AS iss_dt                             ,
            (SELECT end_dt
                    FROM mms.mmsnow
                    WHERE mms.mmsnow.cid = permit_info.cid
            ) AS permit_expiry_dt                                    ,
            CASE permit_info.sta_cd
                WHEN 'Z' THEN 'C' --closed
                ELSE 'O' --open
            END AS sta_cd                                            ,
            permit_info.upd_no
        FROM mms.mmspmt permit_info
        INNER JOIN ETL_MINE ON ETL_MINE.mine_no = permit_info.mine_no
        WHERE permit_info.cid IN (
            {','.join([p for p in list(etl.values(valid_permits,'permit_cid'))])}
        )
        """)
    current_app.logger.info(f'# valid_permit_details {etl.nrows(valid_permits)}')

    #STEP 2 of old permit ETL
    ################################################################
    # Update permit records with the newest version in the MMS data
    ################################################################
    db.session.execute(r"""
        UPDATE permit
        SET
            update_user            = 'mms_migration'       ,
            update_timestamp       = now()                 ,
            permit_status_code     = etl.permit_status_code
        FROM ETL_PERMIT etl
        INNER JOIN mine_permit_xref mpx on etl.mine_guid=mpx.mine_guid
        WHERE
            permit.permit_guid = etl.permit_guid
            AND
            issue_date = (select max(issue_date) from ETL_PERMIT where etl.permit_no = ETL_PERMIT.permit_no)
    """)

    ################################################################
    # Update permit amendment records with the newest version in the MMS data
    ################################################################
    db.session.execute(r"""
        UPDATE permit_amendment
        SET
            received_date          = etl.received_date         ,
            issue_date             = etl.issue_date            ,
            update_user            = 'mms_migration'           ,
            update_timestamp       = now()                     ,
            authorization_end_date = etl.authorization_end_date
        FROM ETL_PERMIT etl
        WHERE
            permit_amendment.permit_amendment_guid = etl.permit_amendment_guid
    """)
    #TODO POPULATE ETL PERMIT BEFORE THIS CAN HAPPEND
    # ################################################################
    # # Insert new permits from MMS into MDS
    # ################################################################
    # new_permits = etl.fromdb(
    #     connection, r"""
    #     SELECT DISTINCT mine_guid, permit_no, permit_status_code
    #     FROM ETL_PERMIT etl
    #     WHERE (mine_guid, permit_no) NOT IN (
    #         SELECT mpx.mine_guid, p.permit_no
    #         FROM permit p
    #         INNER JOIN mine_permit_xref mpx on p.permit_id=mpx.permit_id
    #     )
    #     -- Newest notice of work for each mine/permit:
    #     AND issue_date = (select max(issue_date) from ETL_PERMIT where etl.permit_no = ETL_PERMIT.permit_no and etl.mine_guid = ETL_PERMIT.mine_guid)
    #     """)
    # ##TODO SHOWING 0 ETL_PERMIT IS EMPTY AT THIS POINT
    # current_app.logger.info(f'# new_permits {etl.nrows(new_permits)}')

    # new_permits = etl.addfields(new_permits, [('permit_guid', uuid.uuid4()),
    #                                           ('create_user', 'mms_migration'),
    #                                           ('create_timestamp', datetime.utcnow()),
    #                                           ('update_user', 'mms_migration'),
    #                                           ('update_timestamp', datetime.utcnow())])

    # etl.appenddb(etl.cutout(new_permits, 'mine_guid'), connection, 'permit', commit=False)

    # ################################################################
    # # Insert new permits into the mine permit xref
    # ################################################################
    # db.session.execute(f"""
    #     INSERT INTO mine_permit_xref (
    #         mine_guid,
    #         permit_id
    #     )
    #     SELECT etl_p.mine_guid, p.permit_id
    #     from permit p
    #     INNER JOIN ETL_PERMIT etl on p.permit_guid = etl_p.permit_guid
    #     WHERE p.permit_guid in ("test"
    #         {','.join([p for p in list(etl.values(new_permits,'permit_guid'))])}
    #     )
    # """)

    # ################################################################
    # # update ETL_Permit permit_guids from the newly entered permits.
    # ################################################################
    # for permit in new_permits:
    #     db.session.execute(f"""
    #         UPDATE ETL_PERMIT SET permit_guid = {permit['permit_guid']}
    #         WHERE ETL_PERMIT.permit_no =  {permit['permit_no']}
    #         AND ETL_PERMIT.mine_guid = {permit['mine_guid']}
    #         -- Truly new permits do not have any amendments yet:
    #         AND permit_amendment_guid NOT IN (
    #             SELECT permit_amendment_guid
    #             FROM permit_amendment
    #             )
    #         """)

    ################################################################
    # Insert new permit amendment records
    ################################################################
    new_permit_amendments = etl.fromdb(
        connection, r"""
        SELECT
            permit.permit_id				         	,
            ETL_PERMIT.permit_amendment_guid            ,
            ETL_PERMIT.received_date       	            ,
            ETL_PERMIT.issue_date          	            ,
            ETL_PERMIT.authorization_end_date	        ,
            CASE WHEN first_amendment.permit_no IS NOT NULL THEN 'OGP' ELSE 'AMD' END,
            'ACT'										,
            'mms_migration'                				,
            now()                          				,
            'mms_migration'                				,
            now()
        FROM ETL_PERMIT
        INNER JOIN permit ON
            ETL_PERMIT.permit_guid = permit.permit_guid
        -- NOTE: join to first amendment issued to use above to determine if this is the first amendment / original permit
        LEFT JOIN (SELECT
                permit_no, mine_guid, MIN(issue_date) AS min_issue_date
            FROM
                ETL_PERMIT
            GROUP BY
                permit_no, mine_guid) AS first_amendment ON 
            ETL_PERMIT.permit_no = first_amendment.permit_no AND
            ETL_PERMIT.mine_guid = first_amendment.mine_guid AND
            ETL_PERMIT.issue_date = first_amendment.min_issue_date
        WHERE permit_amendment_guid NOT IN (
            SELECT permit_amendment_guid
            FROM permit_amendment
        )
            """)

    current_app.logger.info(f'# new_permit_amendments {etl.nrows(new_permit_amendments)}')
    current_app.logger.info(etl.headers(new_permit_amendments))

    etl.appenddb(new_permit_amendments, connection, 'permit_amendment', commit=False)

    ################################################################
    # Get three sources for Permittees
    ################################################################
    mine_update_screen_permittees = etl.fromdb(
        connection, r"""
            WITH 
            permit_list AS (
                SELECT
                    mine_no||permit_no||recv_dt||iss_dt AS combo_id,
                    max(cid) permit_cid
                FROM mms.mmspmt 
                WHERE
                    (sta_cd ~* 'z'  OR sta_cd ~* 'a')
                    AND
                    ((permit_no !~ '^ *$' AND  permit_no IS NOT NULL))
                GROUP BY combo_id
            )
            SELECT
                permit_info.cid as permit_cid       ,
                CASE
                    WHEN mine_info.entered_date ~ 'XXXX/XX/XX'
                    THEN current_date
                    ELSE to_date(mine_info.entered_date, 'YYYY/MM/DD')
                END AS effective_date,
                mine_info.cmp_nm AS permittee_nm    ,
                mine_info.ctel_no AS tel_no         ,
                mine_info.cemail AS email           ,
                '3'::numeric AS source
            FROM mms.mmspmt permit_info
            INNER JOIN mms.mmsmin mine_info ON
                mine_info.mine_no = permit_info.mine_no
            WHERE permit_info.cid IN (
                SELECT permit_cid
                FROM permit_list
            )
        """)

    current_app.logger.info(
        f'# mine_update_screen_permittees {etl.nrows(mine_update_screen_permittees)}')

    now_company_info_permittees = etl.fromdb(
        connection, r"""
            WITH 
            permit_list AS (
                SELECT
                    mine_no||permit_no||recv_dt||iss_dt AS combo_id,
                    max(cid) permit_cid
                FROM mms.mmspmt 
                WHERE
                    (sta_cd ~* 'z'  OR sta_cd ~* 'a')
                    AND
                    ((permit_no !~ '^ *$' AND  permit_no IS NOT NULL))
                GROUP BY combo_id
            )
            SELECT
                permit_list.permit_cid              ,
                now.str_dt ::date AS effective_date ,
                company.cmp_nm AS permittee_nm      ,
                company.tel_no                      ,
                company.email                       ,
                '2'::numeric AS source
            FROM permit_list_no_attached_permittee permit_list
            INNER JOIN mms.mmsnow now ON
                now.cid=permit_list.permit_cid
            INNER JOIN mms.mmscmp company ON
                company.cmp_cd = now.cmp_cd
            """)

    current_app.logger.info(
        f'# now_company_info_permittees {etl.nrows(now_company_info_permittees)}')

    permit_contacts = etl.fromdb(
        connection, r"""
        WITH 
        permit_list AS (
            SELECT
                mine_no||permit_no||recv_dt||iss_dt AS combo_id,
                max(cid) permit_cid
            FROM mms.mmspmt 
            WHERE
                (sta_cd ~* 'z'  OR sta_cd ~* 'a')
                AND
                ((permit_no !~ '^ *$' AND  permit_no IS NOT NULL))
            GROUP BY combo_id
        ),
        most_recent_permittee AS (
            SELECT
                cid  AS permit_cid  ,
                max(cid_ccn) AS contact_cid
            FROM mms.mmsccc
            WHERE
                SUBSTRING(type_ind, 4, 1)='Y'
            GROUP BY cid
        )
        SELECT
            most_recent_permittee.permit_cid                ,
            contact_info.add_dt ::date AS effective_date    ,
            company_info.cmp_nm  AS permittee_nm            ,
            company_info.tel_no                             ,
            company_info.email                              ,
            '1'::numeric AS source
        FROM most_recent_permittee
        INNER JOIN mms.mmsccn contact_info ON
            most_recent_permittee.contact_cid=contact_info.cid
        INNER JOIN mms.mmscmp company_info ON
            contact_info.cmp_cd=company_info.cmp_cd
    """)
    current_app.logger.info(f'# permit_contacts {etl.nrows(permit_contacts)}')

    ################################################################
    # Determine which source is best and update permittee
    ################################################################

    #STEP 3 of old permit ETL
    ################################################################
    # Update existing Parties
    ################################################################


"""
all permit info

Columns:
    #PERMIT#
        mine_party_appt_guid - gen_random_guid()
        permit_guid - gen_random_guid()
        permit_amendment_guid - gen_random_guid()
        Source - Set when the permitee info is collected and is a 1, 2, or 3
        mine_guid - ETL_MINE.mine_guid find by matching ETL_MINE.mine_no = mms.mmspmt.mine_no
        mine_no - mms.mmspmt.mine_no
        permit_no - mms.mmspmt.permit_no
        permit_cid - mms.mmspmt.cid
        received_date - mms.mmspmt.recv_dt
        issue_date - mms.mmspmt.iss_dt
        authorization_end_date - mms.mmsnow.end_dt where mms.mmsnow.cid = mms.mmspmt.cid
        permit_status_code - mms.mmspmt.sta_cd ("Z" THEN "C" ELSE "O")
    #PERMITEE#
        party_guid - gen_random_uuid()
        party_combo_id - 
        first_name
        party_name
        party_type
        phone_no
        email
        effective_date

    CASE
        WHEN permit_info.permit_cid NOT IN (
            SELECT ETL_PERMIT.permit_cid
            FROM ETL_PERMIT
        )
        THEN TRUE
        ELSE FALSE
    END AS new_permit           ,
    CASE
        WHEN permittee_wContact.party_combo_id NOT IN (
            SELECT ETL_PERMIT.party_combo_id
            FROM ETL_PERMIT
        )
        THEN TRUE
        ELSE FALSE
    END AS new_permittee
"""