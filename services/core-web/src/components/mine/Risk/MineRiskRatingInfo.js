/* eslint-disable */

import React, { Component } from "react";
import PropTypes from "prop-types";
import { Divider, Button } from "antd";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { openModal, closeModal } from "@common/actions/modalActions";
import { getMines, getMineGuid } from "@common/selectors/mineSelectors";
import CustomPropTypes from "@/customPropTypes";
import MineRiskRatingTable from "@/components/mine/Risk/MineRiskRatingTable";
import AuthorizationWrapper from "@/components/common/wrappers/AuthorizationWrapper";
import * as Permission from "@/constants/permissions";

const propTypes = {
  mines: PropTypes.objectOf(CustomPropTypes.mine).isRequired,
  mineGuid: PropTypes.string.isRequired,
  mineRiskRatingSurveyResponses: PropTypes.objectOf(PropTypes.any),
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
    // this.props.fetchPermits(id).then(() => {
    //   this.setState({ isLoaded: true });
    // });
  };

  openViewMineRiskRatingSurveyResponseModal = () => {};

  render() {
    const mine = this.props.mines[this.props.mineGuid];
    return (
      <div className="tab__content">
        <div>
          <h2>Risk Rating</h2>
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
                  onClick={(event) =>
                    this.openAddPermitModal(
                      event,
                      this.handleAddPermit,
                      `Complete risk rating survey for ${mine.mine_name}`
                    )
                  }
                >
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
});

const mapDispatchToProps = (dispatch) =>
  bindActionCreators(
    {
      openModal,
      closeModal,
    },
    dispatch
  );

export default connect(mapStateToProps, mapDispatchToProps)(MineRiskRatingInfo);
