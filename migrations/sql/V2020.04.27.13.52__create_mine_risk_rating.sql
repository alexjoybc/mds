CREATE TABLE IF NOT EXISTS mine_risk_rating_survey_definition(
    mine_risk_rating_survey_definition_id                                            SERIAL PRIMARY KEY,
    survey_definition_json                  varchar                                            NOT NULL,
    is_active_survey                        boolean                  DEFAULT false             NOT NULL,
    create_timestamp                        timestamp with time zone DEFAULT now()             NOT NULL
);

CREATE TABLE IF NOT EXISTS  mine_risk_rating_survey_response(
    mine_risk_rating_survey_response_id                                              SERIAL PRIMARY KEY,
    mine_risk_rating_survey_definition_id   integer                                            NOT NULL,
    mine_guid                               uuid                                               NOT NULL,
    survey_response_json                    varchar                                            NOT NULL,
    username                                varchar                                            NOT NULL,
    create_timestamp                        timestamp with time zone DEFAULT now()             NOT NULL,

    FOREIGN KEY (mine_risk_rating_survey_definition_id) REFERENCES mine_risk_rating_survey_definition(mine_risk_rating_survey_definition_id),
    FOREIGN KEY (mine_guid) REFERENCES mine(mine_guid)
);

INSERT INTO mine_risk_rating_survey_definition (
    survey_definition_json,
    is_active_survey
    )
VALUES
    ('[
    {
      "id": "letter_dt",
      "label": "Letter Date",
      "type": "DATE",
      "placeholder": null,
      "required": true
    },
    {
      "id": "mine_no",
      "label": "Mine Number",
      "type": "FIELD",
      "placeholder": "Enter the mine number",
      "required": true,
      "relative-data-path": "mine.mine_no",
      "read-only": true
    },
    {
      "id": "proponent_address",
      "label": "Proponent Address",
      "type": "FIELD",
      "placeholder": "Enter the propnent''s address",
      "required": true
    },
    {
      "id": "proponent_name",
      "label": "Proponent Name",
      "type": "FIELD",
      "placeholder": "Enter the propnent''s name",
      "required": false
    },
    {
      "id": "emailed_to",
      "label": "Emailed to",
      "type": "FIELD",
      "placeholder": "Enter the name of the email recipient",
      "required": false
    },
    {
      "id": "property",
      "label": "Property",
      "type": "FIELD",
      "placeholder": "Enter the property",
      "required": true,
      "relative-data-path": "now_application.property_name",
      "read-only": true
    },
    {
      "id": "application_dt",
      "label": "Application Date",
      "type": "DATE",
      "placeholder": null,
      "required": true,
      "relative-data-path": "now_application.submitted_date"
    },
    {
      "id": "exploration_type",
      "label": "Exploration Type",
      "type": "FIELD",
      "placeholder": "Enter the exploration type",
      "required": true
    },
    {
      "id": "bond_inc_amt",
      "label": "Bond Amount",
      "type": "FIELD",
      "placeholder": "Enter the bond amount",
      "required": true
    },
    {
      "id": "inspector",
      "label": "Inspector",
      "type": "FIELD",
      "placeholder": "Enter the inspector''s name",
      "required": true,
      "relative-data-path": "now_application.lead_inspector.name"
    }
  ]', true)
ON CONFLICT DO NOTHING;
