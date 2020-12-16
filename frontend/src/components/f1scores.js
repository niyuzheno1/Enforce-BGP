import React from "react";
import { useEffect, useRef, useState } from "react";

export default function F1scores() {
  return (
    <div id="F1scores">
      <span> Tabi agent: 0.733 </span>
      <p></p>
      <span> Q-Learning agent: 0.783 </span>
      <p></p>
      <span> Deep Q-Learning agent: 0.814 </span>
    </div>
  );
}
