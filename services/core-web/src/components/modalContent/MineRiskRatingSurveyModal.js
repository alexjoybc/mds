import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { formatDate } from "@common/utils/helpers";
import { Col, Row, Descriptions, Divider } from "antd";
import { getMineRiskRatingSurveyDefinitionOptionsHash } from "@common/selectors/staticContentSelectors";
import CustomPropTypes from "@/customPropTypes";
import MineRiskRatingSurveyForm from "@/components/Forms/MineRiskRatingSurveyForm";

const propTypes = {
  onSubmit: PropTypes.func.isRequired,
  closeModal: PropTypes.func.isRequired,
  title: PropTypes.string.isRequired,
  mineGuid: PropTypes.string.isRequired,
  mineRiskRatingSurveyDefinitionOptionsHash: PropTypes.objectOf(PropTypes.any).isRequired,
  mineRiskRatingSurveyResponse: CustomPropTypes.mineRiskRatingSurveyResponse,
  isViewOnly: PropTypes.bool,
};

const defaultProps = {
  mineRiskRatingSurveyResponse: {},
  isViewOnly: false,
};

export const MineRiskRatingSurveyModal = (props) => {
  let mineRiskRatingSurveyDefinition = {};
  if (props.isViewOnly) {
    mineRiskRatingSurveyDefinition =
      props.mineRiskRatingSurveyDefinitionOptionsHash[
        props.mineRiskRatingSurveyResponse.mine_risk_rating_survey_definition_id
      ];
  } else {
    const mineRiskRatingSurveyDefinitions = Object.values(
      props.mineRiskRatingSurveyDefinitionOptionsHash
    );
    mineRiskRatingSurveyDefinition = mineRiskRatingSurveyDefinitions.find(
      (definition) => definition.is_active_survey
    );
  }

  const handleModalSubmit = (values) =>
    props.isViewOnly
      ? () => {}
      : props.onSubmit(
          values,
          mineRiskRatingSurveyDefinition.mine_risk_rating_survey_definition_id
        );

  return (
    <div>
      {props.isViewOnly && (
        <Row type="flex" justify="start" align="middle">
          <h4>Response Info</h4>
          <Divider />
          <Col>
            <Descriptions colon={false} column={1}>
              <Descriptions.Item label="Completed by">
                {props.mineRiskRatingSurveyResponse.username}
              </Descriptions.Item>
              <Descriptions.Item label="Completed on">
                {formatDate(props.mineRiskRatingSurveyResponse.create_timestamp)}
              </Descriptions.Item>
              <Descriptions.Item label="Rating">
                {props.mineRiskRatingSurveyResponse.rating}
              </Descriptions.Item>
              <Descriptions.Item label="Notes">
                {props.mineRiskRatingSurveyResponse.notes}
              </Descriptions.Item>
            </Descriptions>
          </Col>
        </Row>
      )}
      <Row type="flex" justify="start" align="middle">
        <Col>
          <h4>Questionnaire</h4>
          <Divider />
        </Col>
      </Row>
      <Row type="flex" justify="center" align="middle">
        <Col>
          <MineRiskRatingSurveyForm
            onSubmit={handleModalSubmit}
            closeModal={props.closeModal}
            title={props.title}
            mineRiskRatingSurveyDefinition={mineRiskRatingSurveyDefinition}
            mineRiskRatingSurveyResponse={props.mineRiskRatingSurveyResponse}
            mineGuid={props.mineGuid}
            isViewOnly={props.isViewOnly}
            initialValues={
              props.isViewOnly
                ? JSON.parse(props.mineRiskRatingSurveyResponse.survey_response_json)
                : {}
            }
          />
        </Col>
      </Row>
    </div>
  );
};

MineRiskRatingSurveyModal.propTypes = propTypes;
MineRiskRatingSurveyModal.defaultProps = defaultProps;

const mapStateToProps = (state) => ({
  mineRiskRatingSurveyDefinitionOptionsHash: getMineRiskRatingSurveyDefinitionOptionsHash(state),
});

export default connect(mapStateToProps)(MineRiskRatingSurveyModal);
