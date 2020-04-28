import React from "react";
import PropTypes from "prop-types";
import { Form, Slider } from "antd";

/**
 * @constant RenderSliderOneToTen - Ant Design `Slider` component for redux-form.
 */

const propTypes = {
  id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  input: PropTypes.objectOf(PropTypes.any).isRequired,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  meta: PropTypes.objectOf(PropTypes.any).isRequired,
  inlineLabel: PropTypes.string,
  disabled: PropTypes.bool,
};

const defaultProps = {
  label: "",
  placeholder: "",
  inlineLabel: "",
  disabled: false,
};

const RenderSliderOneToTen = (props) => {
  const marks = { 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10 };
  return (
    <Form.Item
      label={props.label}
      validateStatus={
        props.meta.touched ? (props.meta.error && "error") || (props.meta.warning && "warning") : ""
      }
      help={
        props.meta.touched &&
        ((props.meta.error && <span>{props.meta.error}</span>) ||
          (props.meta.warning && <span>{props.meta.warning}</span>))
      }
    >
      <div>
        {props.inlineLabel && (
          <label
            htmlFor={props.id}
            className="nowrap"
            style={{ paddingRight: "10px", fontSize: "20px" }}
          >
            {props.inlineLabel}
          </label>
        )}
        <Slider
          disabled={props.disabled}
          id={props.id}
          placeholder={props.placeholder}
          step={1}
          marks={marks}
          defaultValue={0}
          min={0}
          max={10}
          {...props.input}
        />
      </div>
    </Form.Item>
  );
};

RenderSliderOneToTen.propTypes = propTypes;
RenderSliderOneToTen.defaultProps = defaultProps;

export default RenderSliderOneToTen;
