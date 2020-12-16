import React from "react";
import { useEffect, useRef, useState } from "react";
import { select } from "d3-selection";
import { scaleOrdinal, scaleUtc, scaleLinear } from "d3-scale";
import { LineData } from "../mockdata/lines";
import { schemeCategory10 } from "d3-scale-chromatic";
import Request from "axios-request-handler";
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCenter
} from "d3-force";
import { ROCData } from "../mockdata/data";
import d3Tip from "d3-tip";

import { drag } from "d3-drag";

import * as d3 from "d3";

export default function ROCCurve() {
  useEffect(() => {
    var margin = { top: 10, right: 30, bottom: 30, left: 30 },
      width = 360 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

    var x = scaleLinear().range([0, width]);
    var y = scaleLinear().range([height, 0]);

    //var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(5);
    var xAxis = (g) =>
      g
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).ticks(5).tickSizeOuter(0));
    //var yAxis = d3.svg.axis().scale(y).orient("left").ticks(5);
    var yAxis = (g) =>
      g
        .attr("transform", `translate(0,0)`)
        .call(d3.axisLeft(y))
        .call((g) => g.select(".domain").remove())
        .call((g) =>
          g
            .select(".tick:last-of-type text")
            .clone()
            .attr("x", 3)
            .attr("text-anchor", "start")
            .attr("font-weight", "bold")
        );
    var valueline = d3
      .line()
      .x(function (d) {
        return x(d.x);
      })
      .y(function (d) {
        return y(d.q);
      })
      .curve(d3.curveBasis);

    var valueline2 = d3
      .line()
      .x(function (d) {
        return x(d.x);
      })
      .y(function (d) {
        return y(d.dq);
      })
      .curve(d3.curveBasis);

    var valueline3 = d3
      .line()
      .x(function (d) {
        return x(d.x);
      })
      .y(function (d) {
        return y(d.tabi);
      })
      .curve(d3.curveBasis);

    var valueline5 = d3
      .line()
      .x(function (d) {
        return x(d.x);
      })
      .y(function (d) {
        return y(d.trivial);
      })
      .curve(d3.curveLinear);

    var tip = d3Tip()
      .attr("class", "d3-tip")
      .style("visibility", "visible")
      .offset([-20, 0])
      .html(function (d) {
        return "Q-Learning";
      });

    var tip2 = d3Tip()
      .attr("class", "d3-tip")
      .style("visibility", "visible")
      .offset([-20, 0])
      .html(function (d) {
        return "Deep Q-Learning";
      });

    var tip3 = d3Tip()
      .attr("class", "d3-tip")
      .style("visibility", "visible")
      .offset([-20, 0])
      .html(function (d) {
        return "Tabi";
      });

    var tip4 = d3Tip()
      .attr("class", "d3-tip")
      .style("visibility", "visible")
      .offset([-20, 0])
      .html(function (d) {
        return "Net Points Won";
      });

    var tip5 = d3Tip()
      .attr("class", "d3-tip")
      .style("visibility", "visible")
      .offset([-20, 0])
      .html(function (d) {
        return "Trivial";
      });
    // append the svg object to the body of the page
    var svg = select("#ROCCurve")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("g").call(xAxis);

    svg.append("g").call(yAxis);
    console.log(ROCData);
    var data = ROCData;
    x.domain([0, 1]);
    y.domain([0, 1]);

    svg.call(tip);
    svg.call(tip2);
    svg.call(tip3);
    svg.call(tip4);
    svg.call(tip5);

    svg
      .append("path")
      .attr("class", "line")
      .attr("d", valueline(data))
      .on("mouseover", tip.show)
      .on("mousemove", function () {
        return tip
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px");
      })
      .on("mouseout", tip.hide);

    svg
      .append("path")
      .style("stroke", "red")
      .attr("d", valueline2(data))
      .on("mouseover", tip2.show)
      .on("mousemove", function () {
        return tip2
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px");
      })
      .on("mouseout", tip2.hide);

    svg
      .append("path")
      .style("stroke", "green")
      .attr("d", valueline3(data))
      .on("mouseover", tip3.show)
      .on("mousemove", function () {
        return tip3
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px");
      })
      .on("mouseout", tip3.hide);

    svg
      .append("path")
      .style("stroke", "black")
      .attr("d", valueline5(data))
      .on("mouseover", tip5.show)
      .on("mousemove", function () {
        return tip5
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px");
      })
      .on("mouseout", tip5.hide);

    svg
      .append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("x", width / 2)
      .attr("y", 40)
      .style("text-anchor", "middle")
      .text("1 - False Negative Rate");

    svg
      .append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 10)
      .attr("x", 0 - height / 1.6)
      .style("font-size", "12px")
      .style("text-anchor", "left")
      .text("True Positive Rate");

    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", 0 - margin.top / 2)
      .attr("text-anchor", "middle")
      .style("font-size", "16px");
  }, []);
  return <div id="ROCCurve"></div>;
}
