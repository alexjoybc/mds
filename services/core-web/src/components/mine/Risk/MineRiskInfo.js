/* eslint-disable */

import React, { Component } from "react";
import PropTypes from "prop-types";
import { Divider } from "antd";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import { openModal, closeModal } from "@common/actions/modalActions";
import { getMines, getMineGuid } from "@common/selectors/mineSelectors";
import CustomPropTypes from "@/customPropTypes";

const propTypes = {
  mines: PropTypes.objectOf(CustomPropTypes.mine).isRequired,
  mineGuid: PropTypes.string.isRequired,
  closeModal: PropTypes.func.isRequired,
  openModal: PropTypes.func.isRequired,
  fetchMineRecordById: PropTypes.func.isRequired,
};

export class MineRiskInfo extends Component {
  render() {
    const mine = this.props.mines[this.props.mineGuid];
    return (
      <div className="tab__content">
        <div>
          <h2>Risk</h2>
          <Divider />
          Content!
        </div>
      </div>
    );
  }
}

MineRiskInfo.propTypes = propTypes;
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

export default connect(mapStateToProps, mapDispatchToProps)(MineRiskInfo);
