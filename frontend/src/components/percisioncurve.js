import React from "react";
import { useEffect, useRef, useState } from "react";
import { select } from "d3-selection";
import { scaleOrdinal, scaleUtc } from "d3-scale";
import { LineData } from "../mockdata/lines";
import { schemeCategory10 } from "d3-scale-chromatic";
import Request from "axios-request-handler";
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCenter
} from "d3-force";

import { drag } from "d3-drag";

import * as d3 from "d3";

export default function PercisionCurve() {
  useEffect(() => {
    var margin = { top: 10, right: 30, bottom: 30, left: 10 },
      width = 360 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;
    var data = Object.assign(
      d3
        .csvParse(
          "date,close\n2007-04-23,93.24\n2007-04-24,95.35\n2007-04-25,98.84\n2007-04-26,99.92",
          d3.autoType
        )
        .map(({ date, close }) => ({ date, value: close })),
      { y: "$ Close" }
    );
    var x = scaleUtc()
      .domain(d3.extent(data, (d) => d.date))
      .range([margin.left, width - margin.right]);
    var y = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.value)])
      .nice()
      .range([height - margin.bottom, margin.top]);
    var xAxis = (g) =>
      g.attr("transform", `translate(0,${height - margin.bottom})`).call(
        d3
          .axisBottom(x)
          .ticks(width / 80)
          .tickSizeOuter(0)
      );
    var yAxis = (g) =>
      g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call((g) => g.select(".domain").remove())
        .call((g) =>
          g
            .select(".tick:last-of-type text")
            .clone()
            .attr("x", 3)
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
            .text(data.y)
        );
    var line = d3
      .line()
      .defined((d) => !isNaN(d.value))
      .x((d) => x(d.date))
      .y((d) => y(d.value));
    // append the svg object to the body of the page
    var svg = select("#percisioncurve")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("g").call(xAxis);

    svg.append("g").call(yAxis);

    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("d", line);
  }, []);
  return <div id="percisioncurve"></div>;
}
