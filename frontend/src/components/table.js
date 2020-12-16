import React from "react";
import { useEffect, useState } from "react";
import { Table, Button } from "react-bootstrap";
import Request from "axios-request-handler";
import { httpaddr } from "../net/net";
/* parse JSON data into table format */
export default function HijackingTable(saa) {
  function Rescind() {
    alert("Your request has undergone processing");
  }
  const [alerts, setalert] = useState(null);
  useEffect(() => {
    const degreedist = new Request(httpaddr + "getalert");
    degreedist.get().then((res) => {
      setalert(res.data);
    });
  }, []);
  return (
    <>
      <div>We will only record suspected hijacking cases.</div>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Attacker ASN</th>
            <th>Victim ASN</th>
            <th>Attacker IP</th>
            <th>Impersonating IP</th>
            <th>Action 1</th>
            <th>Action 2</th>
          </tr>
        </thead>
        <tbody>
          {alerts !== null
            ? alerts.map((d, i) => {
                return (
                  <tr>
                    <td>{i + 1}</td>
                    <td>{d["Attacker ASN"]}</td>
                    <td>{d["Victim ASN"]}</td>
                    <td>{d["Impersonating IP"]}</td>
                    <td>{d["Attacker IP"]}</td>
                    <td>
                      <Button onClick={Rescind}> Rescind </Button>
                    </td>
                    <td>
                      <Button
                        onClick={() => {
                          saa.saa(
                            d["Victim ASN"],
                            d["Attacker ASN"],
                            d["Impersonating IP"]
                          );
                        }}
                      >
                        {" "}
                        Inspect{" "}
                      </Button>
                    </td>
                  </tr>
                );
              })
            : 0}
        </tbody>
      </Table>
    </>
  );
}
