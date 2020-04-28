/* eslint-disable */

import React from "react";
import PropTypes from "prop-types";
import { Field, reduxForm, focus } from "redux-form";

import { Form, Button, Col, Row, Popconfirm } from "antd";
import { resetForm } from "@common/utils/helpers";
import { renderConfig } from "@/components/common/config";
import * as FORM from "@/constants/forms";
import { getGenerateDocumentFormField } from "@/components/common/GenerateDocumentFormField";

const propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  closeModal: PropTypes.func.isRequired,
  submitting: PropTypes.bool.isRequired,
  mineRiskRatingSurveyDefinition: PropTypes.objectOf(PropTypes.any),
  mineRiskRatingSurveyResponse: PropTypes.objectOf(PropTypes.any),
  isViewOnly: PropTypes.bool.isRequired,
};

export const MineRiskRatingForm = (props) => {
  const createSurvey = (mineRiskRatingSurveyDefinition) => {
    const fields = JSON.parse(mineRiskRatingSurveyDefinition.survey_definition_json);

    if (props.isViewOnly) {
      fields.forEach((field) => (field.disabled = true));
    }

    return (
      <div>
        {fields &&
          fields.length > 0 &&
          fields.map((field, i) => (
            <Row key={field.id}>
              <Col span={4}>
                <h4>Question {i + 1}</h4>
              </Col>
              <Col span={20}>
                <Form.Item>{getGenerateDocumentFormField(field)}</Form.Item>
              </Col>
            </Row>
          ))}
      </div>
    );
  };

  return (
    <Form layout="vertical" onSubmit={props.handleSubmit}>
      <Row>
        <Col>
          {createSurvey(props.mineRiskRatingSurveyDefinition)}
          {!props.isViewOnly && (
            <Form.Item>
              <Field
                id="notes"
                name="notes"
                label="Notes"
                placeholder="Enter any notes for this mine risk rating survey response"
                component={renderConfig.AUTO_SIZE_FIELD}
              />
            </Form.Item>
          )}
        </Col>
      </Row>
      {!props.isViewOnly && (
        <div className="right center-mobile">
          <Popconfirm
            placement="topRight"
            title="Are you sure you want to cancel?"
            onConfirm={props.closeModal}
            okText="Yes"
            cancelText="No"
          >
            <Button className="full-mobile" type="secondary">
              Cancel
            </Button>
          </Popconfirm>
          <Button
            className="full-mobile"
            type="primary"
            htmlType="submit"
            disabled={props.submitting}
          >
            Complete Survey
          </Button>
        </div>
      )}
    </Form>
  );
};

MineRiskRatingForm.propTypes = propTypes;

export default reduxForm({
  form: FORM.MINE_RISK_RATING_SURVEY,
  touchOnBlur: false,
  onSubmitSuccess: resetForm(FORM.MINE_RISK_RATING_SURVEY),
  onSubmitFail: (errors, dispatch) =>
    dispatch(focus(FORM.MINE_RISK_RATING_SURVEY, Object.keys(errors)[0])),
})(MineRiskRatingForm);
