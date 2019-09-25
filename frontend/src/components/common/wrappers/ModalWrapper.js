import React, { Component } from "react";
import { bindActionCreators } from "redux";
import LoadingBar from "react-redux-loading-bar";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Modal, Icon, Button, Popconfirm } from "antd";
import * as Styles from "@/constants/styles";
import { closeModal } from "@/actions/modalActions";
import {
  getIsModalOpen,
  getProps,
  getContent,
  getClearOnSubmit,
  getWidthSize,
  getIsViewOnly,
} from "@/selectors/modalSelectors";
import AddPartyComponentWrapper from "./AddPartyComponentWrapper";

const propTypes = {
  closeModal: PropTypes.func.isRequired,
  isModalOpen: PropTypes.bool.isRequired,
  content: PropTypes.objectOf(PropTypes.any),
  props: PropTypes.objectOf(PropTypes.any),
  clearOnSubmit: PropTypes.bool.isRequired,
  widthSize: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
  isViewOnly: PropTypes.bool.isRequired,
};

const defaultProps = {
  props: {
    title: "",
    onSubmit: () => {},
  },
  content: () => {},
};

export class ModalWrapper extends Component {
  constructor(props) {
    super(props);
    // listens for browser back || forward button click and invokes function to close the modal,
    window.onpopstate = this.onBrowserButtonEvent;
  }

  onBrowserButtonEvent = () => {
    this.props.closeModal();
  };

  closeModal = (event) => {
    event.preventDefault();
    this.props.closeModal();
    this.props.props.afterClose();
  };

  render() {
    return (
      <Modal
        width={this.props.widthSize}
        title={this.props.props.title}
        visible={this.props.isModalOpen}
        closable={false}
        footer={null}
      >
        {this.props.isViewOnly ? (
          <Button ghost className="modal__close" onClick={(event) => this.closeModal(event)}>
            <Icon type="close" />
          </Button>
        ) : (
          <Popconfirm
            placement="bottomRight"
            title="Are you sure you want to cancel?"
            okText="Yes"
            cancelText="No"
            onConfirm={(event) => this.closeModal(event)}
          >
            <Button ghost className="modal__close">
              <Icon type="close" />
            </Button>
          </Popconfirm>
        )}
        <LoadingBar
          scope="modal"
          style={{
            position: "absolute",
            top: "50px",
            left: 0,
            backgroundColor: Styles.COLOR.violet,
            width: "100%",
            height: "8px",
            zIndex: 100,
          }}
        />
        {this.props.content && (
          <AddPartyComponentWrapper
            closeModal={this.props.closeModal}
            clearOnSubmit={this.props.clearOnSubmit}
            content={this.props.content}
            childProps={this.props.props}
          />
        )}
      </Modal>
    );
  }
}

const mapStateToProps = (state) => ({
  widthSize: getWidthSize(state),
  isModalOpen: getIsModalOpen(state),
  props: getProps(state),
  content: getContent(state),
  clearOnSubmit: getClearOnSubmit(state),
  isViewOnly: getIsViewOnly(state),
});

const mapDispatchToProps = (dispatch) =>
  bindActionCreators(
    {
      closeModal,
    },
    dispatch
  );

ModalWrapper.propTypes = propTypes;
ModalWrapper.defaultProps = defaultProps;

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ModalWrapper);
