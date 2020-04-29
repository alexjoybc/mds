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
    notes                                   varchar                                                    ,
    rating                                  numeric(5,2)                                       NOT NULL,
    username                                varchar                                            NOT NULL,
    create_timestamp                        timestamp with time zone DEFAULT now()             NOT NULL,

    FOREIGN KEY (mine_risk_rating_survey_definition_id) REFERENCES mine_risk_rating_survey_definition(mine_risk_rating_survey_definition_id),
    FOREIGN KEY (mine_guid) REFERENCES mine(mine_guid)
);

-- WIP/temporary risk rating survey questions from Aaron #1
INSERT INTO mine_risk_rating_survey_definition (
    survey_definition_json,
    is_active_survey
    )
VALUES
    (
'[
  {
    "id": "q1",
    "label": "What is the likelihood of any geotechnical incidents at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q2",
    "label": "How significant is the consequence of the largest potential geotechnical failure at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q3",
    "label": "What is the likelihood of any environmental incidents at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q4",
    "label": "How significant is the consequence of the largest environmental risks at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q5",
    "label": "What is the likelihood of any health and safety incidents at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q6",
    "label": "What is the likelihood of any geotechnical incidents at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q7",
    "label": "How significant is the consequence of the most potential health and safety incident at this site?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q8",
    "label": "How has this mine performed in compliance in the past (1 being often non-compliant, 10 being continuously in compliance)?",
    "type": "SLIDER_1_TO_10",
    "required": true
  }
]', true)
ON CONFLICT DO NOTHING;

-- WIP/temporary risk rating survey questions from Aaron #2
INSERT INTO mine_risk_rating_survey_definition (
    survey_definition_json,
    is_active_survey
    )
VALUES
    (
'[
  {
    "id": "q1",
    "label": "How complex is the mine plan? (more complex = more risk)",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q2",
    "label": "What is the level of risk based on different types of site activities (e.g., blasting, drilling)?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q3",
    "label": "How close are the nearest year-round dwellings/communities?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q4",
    "label": "What about the nearest emergency response services and/or hospital?",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q5",
    "label": "What is the level of willingness and ability to comply? (per the C&E compliance policy decision matrix)",
    "type": "SLIDER_1_TO_10",
    "required": true
  },
  {
    "id": "q6",
    "label": "What \"delegation level\" was required to sign the permit? This is sometimes used as a proxy for \'complexity\' or \'level of risk profile\'",
    "type": "SLIDER_1_TO_10",
    "required": true
  }
]', false)
ON CONFLICT DO NOTHING;
