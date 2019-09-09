import React from "react";
import PropTypes from "prop-types";
import { Field, reduxForm } from "redux-form";
import { Form, Col, Row } from "antd";
import * as FORM from "@/constants/forms";
import { required, email, number, phoneNumber, maxLength, dateNotInFuture } from "@/utils/Validate";
import { normalizePhone } from "@/utils/helpers";
import { renderConfig } from "@/components/common/config";
import CustomPropTypes from "@/customPropTypes";

const propTypes = {
  initialValues: PropTypes.objectOf(PropTypes.any).isRequired,
  inspectors: CustomPropTypes.groupOptions.isRequired,
};

export const AddIncidentReportingForm = (props) => (
  <div>
    <Form layout="vertical">
      <Row gutter={48}>
        <Col>
          {props.initialValues.mine_incident_id_year && (
            <h4>{`Ministry Incident No. :  ${props.initialValues.mine_incident_report_no}`}</h4>
          )}
          {props.initialValues.mms_inspector_initials ? (
            <span style={{ float: "right" }}>
              {`MMS Inspector Initials: ${props.initialValues.mms_inspector_initials}`}
            </span>
          ) : (
            ""
          )}
          <Form.Item>
            <Field
              id="reported_to_inspector_party_guid"
              name="reported_to_inspector_party_guid"
              label="Incident reported to*:"
              placeholder="Start typing inspector name"
              component={renderConfig.GROUPED_SELECT}
              validate={[required]}
              data={props.inspectors}
            />
          </Form.Item>
          <Form.Item>
            <Field
              id="responsible_inspector_party_guid"
              name="responsible_inspector_party_guid"
              label="Inspector responsible:*"
              component={renderConfig.GROUPED_SELECT}
              placeholder="Start typing inspector name"
              validate={[required]}
              data={props.inspectors}
            />
          </Form.Item>
          <h4>Reporter Details</h4>
          <Form.Item>
            <Field
              id="reported_by_name"
              name="reported_by_name"
              label="Reported by*"
              placeholder="Provide name of reporter"
              component={renderConfig.FIELD}
              validate={[required]}
            />
          </Form.Item>
          <Row gutter={16}>
            <Col md={12} xs={24}>
              <Form.Item>
                <Field
                  id="reported_by_phone_no"
                  name="reported_by_phone_no"
                  label="Phone number"
                  placeholder="xxx-xxx-xxxx"
                  component={renderConfig.FIELD}
                  validate={[phoneNumber, maxLength(12)]}
                  normalize={normalizePhone}
                />
              </Form.Item>
            </Col>
            <Col md={12} xs={24}>
              <Form.Item>
                <Field
                  id="reported_by_phone_ext"
                  name="reported_by_phone_ext"
                  label="Phone extension"
                  placeholder=""
                  component={renderConfig.FIELD}
                  validate={[number, maxLength(4)]}
                />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item>
            <Field
              id="reported_by_email"
              name="reported_by_email"
              label="Email"
              placeholder="example@domain.com"
              component={renderConfig.FIELD}
              validate={[email]}
            />
          </Form.Item>
          <Row gutter={16}>
            <Col md={12} xs={24}>
              <Form.Item>
                <Field
                  id="reported_date"
                  name="reported_date"
                  label="Reported Date*"
                  placeholder="Please select date"
                  component={renderConfig.DATE}
                  validate={[required, dateNotInFuture]}
                />
              </Form.Item>
            </Col>
            <Col md={12} xs={24}>
              <Form.Item>
                <Field
                  id="reported_time"
                  name="reported_time"
                  label="Reported Time*"
                  placeholder="Please select time"
                  component={renderConfig.TIME}
                  validate={[required]}
                  fullWidth
                />
              </Form.Item>
            </Col>
          </Row>
        </Col>
      </Row>
    </Form>
  </div>
);

AddIncidentReportingForm.propTypes = propTypes;

export default reduxForm({
  form: FORM.MINE_INCIDENT,
  destroyOnUnmount: false,
  forceUnregisterOnUnmount: true,
  touchOnBlur: true,
})(AddIncidentReportingForm);
