import React from "react";
import { PropTypes } from "prop-types";
import { Field } from "redux-form";
import { Row, Col, Table } from "antd";
import RenderField from "@/components/common/RenderField";
import * as Strings from "@/constants/strings";
import RenderAutoSizeField from "@/components/common/RenderAutoSizeField";
import Equipment from "@/components/noticeOfWork/applications/review/activities/Equipment";
import CustomPropTypes from "@/customPropTypes";

const propTypes = {
  isViewMode: PropTypes.bool.isRequired,
  initialValues: CustomPropTypes.defaultActivity,
};
const defaultProps = {
  initialValues: {},
};

export const MechanicalTrenching = (props) => {
  const columns = [
    {
      title: "Activity",
      dataIndex: "activity",
      key: "activity",
      render: (text) => <div title="Activity">{text}</div>,
    },
    {
      title: "Number of Sites",
      dataIndex: "numSites",
      key: "numSites",
      render: (text) => <div title="Number of Sites">{text}</div>,
    },
    {
      title: "Disturbed Area (ha)",
      dataIndex: "disturbedArea",
      key: "disturbedArea",
      render: (text) => <div title="Disturbed Area (ha)">{text}</div>,
    },
    {
      title: "Merchantable timber volume (m3)",
      dataIndex: "timberVolume",
      key: "timberVolume",
      render: (text) => <div title="Merchantable timber volume (m3)">{text}</div>,
    },
  ];

  const transformData = (activities) =>
    activities.map((activity) => ({
      activity: activity.activity_type_description || Strings.EMPTY_FIELD,
      numSites: activity.number_of_sites || Strings.EMPTY_FIELD,
      disturbedArea: activity.disturbed_area || Strings.EMPTY_FIELD,
      timberVolume: activity.timber_volume || Strings.EMPTY_FIELD,
    }));

  return (
    <div>
      <Table
        align="left"
        pagination={false}
        columns={columns}
        dataSource={transformData(props.initialValues.details ? props.initialValues.details : [])}
        locale={{
          emptyText: "No data",
        }}
      />
      <br />
      {props.initialValues.equipment && <Equipment equipment={props.initialValues.equipment} />}
      <h4>Reclamation Program</h4>
      <Row gutter={16}>
        <Col md={12} sm={24}>
          <div className="field-title">
            Proposed reclamation and timing for this specific activity
          </div>
          <Field
            id="reclamation_description"
            name="reclamation_description"
            component={RenderAutoSizeField}
            disabled={props.isViewMode}
          />
        </Col>
        <Col md={12} sm={24}>
          <div className="field-title">
            Estimated Cost of reclamation activities described above
          </div>
          <Field
            id="reclamation_cost"
            name="reclamation_cost"
            component={RenderField}
            disabled={props.isViewMode}
          />
        </Col>
      </Row>
    </div>
  );
};

MechanicalTrenching.propTypes = propTypes;
MechanicalTrenching.defaultProps = defaultProps;

export default MechanicalTrenching;
