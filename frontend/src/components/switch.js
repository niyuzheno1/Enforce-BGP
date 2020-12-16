import React from "react";
import "../css/switch.css";

export default function Switch({ id, isOn, handleToggle }) {
  return (
    <>
      <input
        checked={isOn}
        onChange={handleToggle}
        className="react-switch-checkbox"
        id={`react-switch-new` + id}
        type="checkbox"
      />
      <label
        style={{ background: isOn && "#06D6A0" }}
        className="react-switch-label"
        htmlFor={`react-switch-new` + id}
      >
        <span className={`react-switch-button`} />
      </label>
    </>
  );
}
