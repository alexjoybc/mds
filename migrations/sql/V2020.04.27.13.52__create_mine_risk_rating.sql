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
    (
'[
  {
    "id": "geo_q1",
    "question": "What is the likelihood of any geotechnical incidents at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "How significant is the consequence of the largest potential geotechnical failure at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "What is the likelihood of any environmental incidents at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "How significant is the consequence of the largest environmental risks at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "What is the likelihood of any health and safety incidents at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "What is the likelihood of any geotechnical incidents at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "How significant is the consequence of the most potential health and safety incident at this site?",
    "type": "RANGE_10"
  },
  {
    "id": "geo_q1",
    "question": "How has this mine performed in compliance in the past (1 being often non-compliant, 10 being continuously in compliance)?",
    "type": "RANGE_10"
  }
]', true)
ON CONFLICT DO NOTHING;
