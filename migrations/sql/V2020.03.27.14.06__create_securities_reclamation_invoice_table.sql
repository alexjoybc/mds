CREATE TABLE IF NOT EXISTS reclamation_invoice (
    reclamation_invoice_id                                           SERIAL PRIMARY KEY,
    reclamation_invoice_guid         uuid DEFAULT gen_random_uuid()     UNIQUE NOT NULL,
    permit_id                        integer                                   NOT NULL,
    invoice_number                   varchar                                   NOT NULL,
    amount                           numeric(14,2)                             NOT NULL,
    vendor                           varchar                                   NOT NULL,
    create_user                      varchar                                   NOT NULL,
    create_timestamp                 timestamp with time zone DEFAULT now()    NOT NULL,
    update_user                      varchar                                   NOT NULL,
    update_timestamp                 timestamp with time zone DEFAULT now()    NOT NULL,

    FOREIGN KEY (permit_id) REFERENCES permit(permit_id) DEFERRABLE INITIALLY DEFERRED
);

ALTER TABLE reclamation_invoice OWNER TO mds;

-- TODO: Write a comment for this table.
COMMENT ON TABLE reclamation_invoice IS '';

ALTER TABLE mine_document ADD COLUMN reclamation_invoice_id integer;
ALTER TABLE mine_document ADD CONSTRAINT reclamation_invoice_id_fk FOREIGN KEY (reclamation_invoice_id) REFERENCES reclamation_invoice(reclamation_invoice_id);
