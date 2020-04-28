/* eslint-disable */

import React, { Component } from "react";
import PropTypes from "prop-types";
import { sum } from "lodash";
import { Divider, Button, Icon } from "antd";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { openModal, closeModal } from "@common/actions/modalActions";
import {
  getMines,
  getMineGuid,
  getMineRiskRatingSurveyResponses,
} from "@common/selectors/mineSelectors";
import { formatDate } from "@common/utils/helpers";
import {
  fetchMineRiskRatingSurveyResponses,
  createMineRiskRatingSurveyResponse,
} from "@common/actionCreators/mineActionCreator";
import { modalConfig } from "@/components/modalContent/config";
import CustomPropTypes from "@/customPropTypes";
import MineRiskRatingTable from "@/components/mine/Risk/MineRiskRatingTable";
import AuthorizationWrapper from "@/components/common/wrappers/AuthorizationWrapper";
import * as Permission from "@/constants/permissions";

const propTypes = {
  mines: PropTypes.objectOf(CustomPropTypes.mine).isRequired,
  mineGuid: PropTypes.string.isRequired,
  mineRiskRatingSurveyResponses: PropTypes.arrayOf(PropTypes.any),
  closeModal: PropTypes.func.isRequired,
  openModal: PropTypes.func.isRequired,
};

const defaultProps = {
  mineRiskRatingSurveyResponses: [],
};

export class MineRiskRatingInfo extends Component {
  state = {
    isLoaded: false,
  };

  componentWillMount = () => {
    const { id } = this.props.match.params;
    this.props.fetchMineRiskRatingSurveyResponses(id).then(() => {
      this.setState({ isLoaded: true });
    });
  };

  handleCompleteMineRiskRatingSurveyResponse = (values, mineRiskRatingSurveyDefinitionId) => {
    const { notes } = values;
    delete values.notes;
    const fieldValues = Object.values(values);
    // NOTE: Temporary " - 1" in calculation due to notes field.
    const rating = (sum(fieldValues) / (fieldValues.length * 10)) * 100;
    console.log("ratnoig", rating);
    const payload = {
      mine_risk_rating_survey_definition_id: mineRiskRatingSurveyDefinitionId,
      mine_guid: this.props.mineGuid,
      survey_response_json: JSON.stringify(values),
      notes,
      username: "",
      rating,
    };

    this.props.createMineRiskRatingSurveyResponse(payload).then(() => {
      this.props.fetchMineRiskRatingSurveyResponses(this.props.mineGuid).then(() => {
        this.props.closeModal();
        this.setState({ isLoaded: true });
      });
    });
  };

  openCompleteMineRiskRatingSurveyResponseModal = (event) => {
    const mine = this.props.mines[this.props.mineGuid];
    event.preventDefault();
    this.props.openModal({
      props: {
        title: `Complete Risk Rating Survey for ${mine.mine_name}`,
        mineGuid: mine.mine_guid,
        onSubmit: this.handleCompleteMineRiskRatingSurveyResponse,
      },
      width: "50vw",
      content: modalConfig.MINE_RISK_RATING_SURVEY,
    });
  };

  openViewMineRiskRatingSurveyResponseModal = (event, mineRiskRatingSurveyResponse) => {
    const mine = this.props.mines[this.props.mineGuid];
    event.preventDefault();
    this.props.openModal({
      props: {
        title: `Risk Rating Survey completed by ${
          mineRiskRatingSurveyResponse.username
        } on ${formatDate(mineRiskRatingSurveyResponse.create_timestamp)}`,
        mineRiskRatingSurveyResponse,
        mineGuid: mine.mine_guid,
        isViewOnly: true,
      },
      width: "50vw",
      content: modalConfig.MINE_RISK_RATING_SURVEY,
    });
  };

  render() {
    const mine = this.props.mines[this.props.mineGuid];
    return (
      <div className="tab__content">
        <div>
          <h2>Mine Risk Rating</h2>
          <br />
          <p>
            The below table displays all of the completed risk rating surveys for this mine. To
            complete a risk rating survey, click the Complete Risk Rating Survey button. A mine is
            considered to have a high risk rating if its rating is close to 100 and has a low risk
            ratiing if its value is close to 0.
          </p>
          <Divider />
        </div>
        <div>
          <div className="inline-flex between">
            <div />
            <div className="inline-flex between">
              <AuthorizationWrapper
                permission={Permission.EDIT_MINES}
                isMajorMine={mine.major_mine_ind}
              >
                <Button
                  type="primary"
                  onClick={(event) => this.openCompleteMineRiskRatingSurveyResponseModal(event)}
                >
                  <Icon type="form" />
                  Complete Risk Rating Survey
                </Button>
              </AuthorizationWrapper>
            </div>
          </div>
        </div>
        <br />
        <MineRiskRatingTable
          isLoaded={this.state.isLoaded}
          mineRiskRatingSurveyResponses={this.props.mineRiskRatingSurveyResponses}
          openViewMineRiskRatingSurveyResponseModal={this.openViewMineRiskRatingSurveyResponseModal}
        />
      </div>
    );
  }
}

MineRiskRatingInfo.propTypes = propTypes;
MineRiskRatingInfo.defaultProps = defaultProps;

const mapStateToProps = (state) => ({
  mines: getMines(state),
  mineGuid: getMineGuid(state),
  mineRiskRatingSurveyResponses: getMineRiskRatingSurveyResponses(state),
});

const mapDispatchToProps = (dispatch) =>
  bindActionCreators(
    {
      fetchMineRiskRatingSurveyResponses,
      createMineRiskRatingSurveyResponse,
      openModal,
      closeModal,
    },
    dispatch
  );

export default connect(mapStateToProps, mapDispatchToProps)(MineRiskRatingInfo);
