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
import IpContext from "../context/IPcontext";
import * as d3 from "d3";

export default function ASesIP({ id, ipaddr }) {
  console.log(ipaddr);
  const value = React.useContext(IpContext);
  console.log(value);
  useEffect(() => {
    var margin = { top: 10, right: 30, bottom: 30, left: 30 },
      width = 360 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

    var data = Object.assign(
      d3
        .csvParse(
          value,

          ({ AS, frequency }) => ({ name: AS, value: +frequency })
        )
        .sort((a, b) => d3.descending(a.value, b.value)),
      { format: "%", y: "↑ Frequency" }
    );
    var color = "steelblue";
    // append the svg object to the body of the page
    select("#my_dataviz_aspath_ASes_IP" + id)
      .selectAll("*")
      .remove();
    var svg = select("#my_dataviz_aspath_ASes_IP" + id)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    var x = d3
      .scaleBand()
      .domain(d3.range(data.length))
      .range([margin.left, width - margin.right])
      .padding(0.1);
    var y = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.value)])
      .nice()
      .range([height - margin.bottom, margin.top]);
    var xAxis = (g) =>
      g.attr("transform", `translate(0,${height - margin.bottom})`).call(
        d3
          .axisBottom(x)
          .tickFormat((i) => data[i].name)
          .tickSizeOuter(0)
      );
    var yAxis = (g) =>
      g
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(null, data.format))
        .call((g) => g.select(".domain").remove())
        .call((g) =>
          g
            .append("text")
            .attr("x", -margin.left)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text(data.y)
        );
    svg
      .append("g")
      .attr("fill", color)
      .selectAll("rect")
      .data(data)
      .join("rect")
      .attr("x", (d, i) => x(i))
      .attr("y", (d) => y(d.value))
      .attr("height", (d) => y(0) - y(d.value))
      .attr("width", x.bandwidth());

    svg.append("g").call(xAxis);

    svg.append("g").call(yAxis);
  }, [value]);
  return (
    <div>
      <div id={"my_dataviz_aspath_ASes_IP" + id}> </div>
    </div>
  );
}
