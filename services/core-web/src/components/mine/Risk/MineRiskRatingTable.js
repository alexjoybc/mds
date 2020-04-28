import React from "react";
import { Button, Icon } from "antd";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { formatDate } from "@common/utils/helpers";
import * as Strings from "@common/constants/strings";
import NullScreen from "@/components/common/NullScreen";
import CoreTable from "@/components/common/CoreTable";

const propTypes = {
  mineRiskRatingSurveyResponses: PropTypes.objectOf(PropTypes.any),
  openViewMineRiskRatingSurveyResponseModal: PropTypes.func.isRequired,
  isLoaded: PropTypes.bool.isRequired,
};

const defaultProps = { mineRiskRatingSurveyResponses: [] };

const columns = [
  {
    title: "Rating",
    dataIndex: "rating",
    key: "rating",
    render: (text) => <div title="Rating">{text}</div>,
    sorter: (a, b) => a.rating.localeCompare(b.rating),
  },
  {
    title: "Username",
    dataIndex: "username",
    key: "username",
    render: (text) => <div title="Username">{text}</div>,
    sorter: (a, b) => a.username.localeCompare(b.username),
  },
  {
    title: "Date Completed",
    dataIndex: "create_timestamp",
    key: "create_timestamp",
    render: (text) => <div title="Date Completed">{text}</div>,
    sorter: (a, b) => a.create_timestamp.localeCompare(b.create_timestamp),
  },
  {
    key: "operations",
    align: "right",
    render: (text, record) => (
      <Button
        type="primary"
        size="small"
        ghost
        onClick={(event) =>
          record.openViewMineRiskRatingSurveyResponseModal(
            event,
            record.mineRiskRatingSurveyResponse
          )
        }
      >
        <Icon type="eye" className="icon-lg icon-svg-filter" />
      </Button>
    ),
  },
];

const transformRowData = (response, openViewMineRiskRatingSurveyResponseModal) => {
  return {
    key: response.mine_risk_rating_survey_response_id,
    create_timestamp:
      (response.create_timestamp && formatDate(response.create_timestamp)) || Strings.EMPTY_FIELD,
    username: response.username || Strings.EMPTY_FIELD,
    rating: response.rating || Strings.EMPTY_FIELD,
    openViewMineRiskRatingSurveyResponseModal,
    mineRiskRatingSurveyResponse: response,
  };
};

export const MineRiskRatingTable = (props) => {
  const rowData = props.mineRiskRatingSurveyResponses.map((response) =>
    transformRowData(response, props.openViewMineRiskRatingSurveyResponseModal)
  );

  return (
    <CoreTable
      condition={props.isLoaded}
      dataSource={rowData}
      columns={columns}
      tableProps={{
        className: "nested-table",
        rowClassName: "table-row-align-middle pointer fade-in",
        align: "left",
        pagination: false,
        locale: { emptyText: <NullScreen type="risk-rating" /> },
      }}
    />
  );
};

const mapStateToProps = () => ({});

MineRiskRatingTable.propTypes = propTypes;
MineRiskRatingTable.defaultProps = defaultProps;

export default connect(mapStateToProps)(MineRiskRatingTable);
