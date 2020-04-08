CREATE TABLE permit_condition (
  permit_condition_id                   SERIAL                      PRIMARY KEY          ,
  now_application_id                    integer                     NOT NULL,
  condition_section                     varchar                     NOT NULL,
  condition_text                        varchar                     NOT NULL, 
  condition_start_date                  timestamp with time zone    DEFAULT now() NOT null,
  library_condtion_id                   integer                     ,
  active_ind                            boolean                     DEFAULT true NOT NULL,
  create_user                           varchar                     NOT NULL,
  create_timestamp                      timestamp with time zone    DEFAULT now() NOT null,
  update_user                           varchar                     NOT NULL,
  update_timestamp                      timestamp with time zone    DEFAULT now() NOT null,

  FOREIGN KEY (now_application_id) REFERENCES now_application(now_application_id) DEFERRABLE INITIALLY DEFERRED,
);
ALTER TABLE permit_condition OWNER TO mds;
