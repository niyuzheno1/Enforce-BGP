import React from "react";
import { useEffect, useRef, useState } from "react";
import { select } from "d3-selection";
import { scaleOrdinal } from "d3-scale";
import { schemeCategory10 } from "d3-scale-chromatic";
import Request from "axios-request-handler";
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCenter
} from "d3-force";

import { drag } from "d3-drag";
import { httpaddr } from "../net/net";
export default function NetworkGraph({ nodeid, attackerNodeID }) {
  const node = useRef(null);
  const [hasbuilt, sethasbuilt] = useState(false);
  const [sim, setSim] = useState(null);
  const [nos, setNodes] = useState(null);
  const [Lnk, setLinks] = useState(null);
  var simulation = null;
  var node2 = null;
  var link = null;
  var color = (color = (function () {
    const scale = scaleOrdinal(schemeCategory10);
    return (d) => scale(d.group);
  })());
  const build = (networkdata) => {
    const links = networkdata.links.map((d) => Object.create(d));
    const nodes = networkdata.nodes.map((d) => Object.create(d));
    select("svg").selectAll("*").remove();

    let width = 954,
      height = 600;
    var controldrag = (simulation) => {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }

      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }

      return drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    };
    var svg = select(node.current)
      .attr("width", width)
      .attr("height", height)
      .append("g");

    simulation = forceSimulation(nodes)
      .force(
        "link",
        forceLink(links).id((d) => d.id)
      )
      .force("charge", forceManyBody().strength(-50).distanceMax(100))
      .force("center", forceCenter(width / 3, height / 2));
    link = svg
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", (d) => Math.sqrt(d.value));
    node2 = svg
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", (d) => (d.group === 2 || d.group === 3 ? 10 : 5))
      .attr("fill", color)
      .call(controldrag(simulation));

    node2.append("title").text((d) => d.id);

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node2.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    });
    setSim(simulation);
    setNodes(node2);
    setLinks(link);
  };
  // const update = (networkdata) => {
  //   let width = 954,
  //     height = 600;
  //   // Make a shallow copy to protect against mutation, while
  //   // recycling old nodes to preserve position and velocity.
  //   var nodes = networkdata.nodes;
  //   var links = networkdata.links;
  //   const old = new Map(nos.data().map((d) => [d.id, d]));
  //   const links2 = networkdata.links.map((d) => Object.create(d));
  //   const nodes2 = networkdata.nodes.map((d) => Object.create(d));
  //   console.log(nodes2);
  //   var node2 = nos.data(nodes2, (d) => d.id).join("circle");
  //   var link = Lnk.data(links2).join("line");
  //   simulation = forceSimulation(nodes2)
  //     .force(
  //       "link",
  //       forceLink(links2).id((d) => d.id)
  //     )
  //     .force("charge", forceManyBody().strength(-50).distanceMax(100))
  //     .force("center", forceCenter(width / 3, height / 2));
  //   simulation.on("tick", () => {
  //     link
  //       .attr("x1", (d) => d.source.x)
  //       .attr("y1", (d) => d.source.y)
  //       .attr("x2", (d) => d.target.x)
  //       .attr("y2", (d) => d.target.y);

  //     node2.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  //   });
  //   sim.alpha(1).restart();
  //   setNodes(node2);
  //   setLinks(link);
  //   setSim(simulation);
  // };
  useEffect(() => {
    const graph = new Request(httpaddr + "graph", {
      params: { asn: nodeid, aasn: attackerNodeID }
    });
    graph.get().then((res) => {
      if (!hasbuilt) {
        sethasbuilt(true);
        build(res.data);
        console.log("finished");
      } else {
        console.log(link);
        if (nos !== null) build(res.data);
      }
    });
  }, [nodeid]);
  return (
    <div className="NetworkGraphtwo">
      <svg ref={node}></svg>;
    </div>
  );
}
