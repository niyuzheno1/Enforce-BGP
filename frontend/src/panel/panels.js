import React from "react";
import DegreeDistributionChart from "../components/degreedistribution";
import AsPathLengthDistribution from "../components/AsPathLengthDistribution";
import ASesIP from "../components/IPbarcharts";
import WithdrawRouteLengthGraph from "../components/withdrawroutelength";
import Multiexitdiscriminator from "../components/Multiexitdiscriminator";
import ROCCurve from "../components/ROCcurve";
import PercisionCurve from "../components/percisioncurve";
import F1scores from "../components/f1scores";
export const panels = [
  { title: "Degree Distribution", show: true },
  { title: "AS Path Length Distribution", show: true },
  { title: "How many ASes announced the IP?", show: true },
  { title: "Withdrawn Routes Length Distribution", show: true },
  { title: "Aggregated Multi-Exit Discriminator vs Time", show: true },
  { title: "ROC Curve of our Model vs benchmarks", show: true },
  //{ title: "Percision Recall Curve vs Benchmarks", show: true },
  { title: "F1-scores", show: true }
];
export const panelsBody = [
  {
    body: (
      <div>
        <DegreeDistributionChart></DegreeDistributionChart>
      </div>
    )
  },
  {
    body: (
      <div>
        <AsPathLengthDistribution></AsPathLengthDistribution>
      </div>
    )
  },
  {
    body: (
      <div>
        <ASesIP></ASesIP>
      </div>
    )
  },
  {
    body: (
      <div>
        <WithdrawRouteLengthGraph></WithdrawRouteLengthGraph>
      </div>
    )
  },
  {
    body: (
      <div>
        <Multiexitdiscriminator></Multiexitdiscriminator>
      </div>
    )
  },
  {
    body: (
      <div>
        <ROCCurve></ROCCurve>
      </div>
    )
  },
  /*{
    body: (
      <div>
        <PercisionCurve></PercisionCurve>
      </div>
    )
  },*/
  {
    body: (
      <div>
        <F1scores></F1scores>
      </div>
    )
  }
];
